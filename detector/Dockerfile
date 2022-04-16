FROM python:3.8-slim-buster

FROM continuumio/miniconda3

SHELL ["/bin/bash", "--login", "-c"]


RUN apt-get update
RUN apt-get -y install gcc

RUN apt-get -y install libgl1-mesa-glx


WORKDIR /app
COPY environment.yml .

RUN conda env create -f environment.yml

RUN conda init bash
RUN conda activate exe

RUN conda install loguru

RUN pip install pyyaml==5.1
RUN pip3 install pycocotools
RUN pip install torch==1.8.0+cu101 torchvision==0.9.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html 
RUN pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.8/index.html
RUN pip install opencv-python

WORKDIR /app
COPY . /app


ENTRYPOINT ["python", "__main__.py"]
