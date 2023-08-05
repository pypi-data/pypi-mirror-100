import os
import sys
import cv2
import numpy as np
import imutils
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from imutils import paths
from os.path import dirname

rootDir = dirname(__file__)
os.environ["FACE_MODEL_PATH"] = os.path.join(rootDir, "models")


class FaceUtil:
    def __init__(self):
        protoPath = os.path.sep.join([os.environ["FACE_MODEL_PATH"], "deploy.prototxt"])
        modelPath = os.path.sep.join([os.environ["FACE_MODEL_PATH"], "res10_300x300_ssd_iter_140000.caffemodel"])
        self.detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

        self.embedder = cv2.dnn.readNetFromTorch(os.path.sep.join([os.environ["FACE_MODEL_PATH"], "openface_nn4.small2.v1.t7"]))

    def __del__(self):
        pass

    def detect(self, image, thresh = 0.8):
        (h, w) = image.shape[:2]

        imageBlob = cv2.dnn.blobFromImage(
	        cv2.resize(image, (300, 300)), 1.0, (300, 300),
	        (104.0, 177.0, 123.0), swapRB=False, crop=False)

        self.detector.setInput(imageBlob)
        detections = self.detector.forward()

        roiList = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > thresh:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                #(startX, startY, endX, endY) = box.astype("int")
                roi = box.astype("int")
                roiList.append(roi)

        return roiList

    def extract(self, dataSetPath, thresh = 0.8):
        imagePaths = list(paths.list_images(dataSetPath))
        knownEmbeddings = []
        knownNames = []

        total = 0
        for (i, imagePath) in enumerate(imagePaths):
            print("[INFO] processing image {}/{}".format(i + 1,	len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]

            image = cv2.imread(imagePath)
            image = imutils.resize(image, width=600)
            
            faceRoiList = self.detect(image, thresh)

            if len(faceRoiList) > 0:
                (startX, startY, endX, endY) = faceRoiList[0]

                face = image[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                #너무 작은 얼굴이라면
                if fW < 20 or fH < 20:
                    continue

                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                    (96, 96), (0, 0, 0), swapRB=True, crop=False)
                self.embedder.setInput(faceBlob)
                vec = self.embedder.forward()

                knownNames.append(name)
                knownEmbeddings.append(vec.flatten())
                total += 1

        print("[INFO] serializing {} encodings...".format(total))
        data = {"embeddings": knownEmbeddings, "names": knownNames}
        return data


    def train(self, dataSetPath, thresh = 0.8):
        data = self.extract(dataSetPath, thresh)
        emb = data["embeddings"]

        self.le = LabelEncoder()
        labels = self.le.fit_transform(data["names"])
        
        print("[INFO] training model...")
        self.recognizer = SVC(C=1.0, kernel="linear", probability=True)
        self.recognizer.fit(emb, labels)
        print("[INFO] train end")

    def save(self, savePath):
        f = open(os.path.join(savePath, "recognizer"), "wb")
        f.write(pickle.dumps(self.recognizer))
        f.close()

        f = open(os.path.join(savePath, "le"), "wb")
        f.write(pickle.dumps(self.le))
        f.close()


    def load(self, loadPath):
        self.recognizer = pickle.loads(open(os.path.join(loadPath, "recognizer"), "rb").read())
        self.le = pickle.loads(open(os.path.join(loadPath, "le"), "rb").read())

    def maskInit(self):
        from tensorflow.keras.models import load_model
        self.model = load_model(os.path.sep.join([os.environ["FACE_MODEL_PATH"], "mask_detector.model"]))

    def maskDetect(self, image, thresh):
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        from tensorflow.keras.preprocessing.image import img_to_array
        
        roiList = self.detect(image, thresh)

        maskList = []
        for startX, startY, endX, endY in roiList:
            face = image[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            face = np.expand_dims(face, axis=0)

            (mask, withoutMask) = self.model.predict(face)[0]
            mask_use = True if mask > withoutMask else False
            proba = mask if mask > withoutMask else withoutMask
            maskList.append({"roi" : (startX, startY, endX, endY), "mask" : mask_use, "proba" : proba})

        return maskList


    def recognize(self, image, thresh = 0.8):
        height, width = image.shape[:2]

        image = imutils.resize(image, width=600)
        new_height, new_width = image.shape[:2]

        roiList = self.detect(image, thresh)

        faceList = []
        for startX, startY, endX, endY  in roiList:
            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
	            (0, 0, 0), swapRB=True, crop=False)
            self.embedder.setInput(faceBlob)
            vec = self.embedder.forward()

            preds = self.recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = self.le.classes_[j]

            startX = int(width * startX / new_width)
            startY = int(height * startY / new_height)
            endX = int(width * endX / new_width)
            endY = int(height * endY / new_height)
            faceList.append({"roi" : (startX, startY, endX, endY), "name" : name, "proba" : proba})

        return faceList

    def draw(self, image, rect, name, proba, color = (0, 0, 255)):
        startX, startY, endX, endY = rect
        text = "{}: {:.2f}%".format(name, proba * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
        cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)


def demo_maskDetectCam():
    face = FaceUtil()

    #마스크 분류기 준비
    face.maskInit()

    #테스트 이미지의 경로를 가져옴
    imagePathList = glob(os.path.sep.join(["test", "*.*"]))

    for imagePath in imagePathList:
        #이미지 읽어옴
        image = cv2.imread(imagePath)

        #마스크 착용여부 체크
        infoList = face.maskDetect(image, 0.5)

        for info in infoList:
            print(info)
            #이미지에 그림
            face.draw(image, info["roi"], info["mask"], info["proba"]
                      , (0, 255, 0) if info["mask"] else (0, 0, 255))


        cv2.imshow("view", image)
        cv2.waitKey()
        cv2.destroyAllWindows()

def demo_cam(modelFolderPath):
    face = FaceUtil()
    face.load(modelFolderPath)

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        infoList = face.recognize(frame, 0.5)
        for info in infoList:
            face.draw(image, info["roi"], info["name"], info["proba"])

        cv2.imshow("view", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pass
