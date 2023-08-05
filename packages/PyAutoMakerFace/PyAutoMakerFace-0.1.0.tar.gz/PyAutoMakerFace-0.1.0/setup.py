import setuptools
import os
import sys
from os.path import dirname
from glob import glob

with open("README.md", "rt") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyAutoMakerFace", # Replace with your own username
    version="0.1.0",
    author="WDW",
    author_email="boa3465@gmail.com",
    description="얼굴 인식을 위한 패키지",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://boa9448.tistory.com",
    project_urls={
        "Bug Tracker": "https://boa9448.tistory.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["PyAutoMakerFace"],
    #data_files=[("lib\\site-packages\\PyAutoMakerFace\\models", [file for file in glob("PyAutoMakerFace\\models\\*.*")])],
    data_files=[(os.path.sep.join(["lib", "site-packages", "PyAutoMakerFace", "models"])
                 , [file for file in glob("PyAutoMakerFace\\models\\*.*")])],
    install_requires = ["opencv-contrib-python", "numpy", "imutils"
                        , "scikit-learn", "tensorflow==2.3.0", "waitress", "flask"],
    python_requires=">=3.6",
)