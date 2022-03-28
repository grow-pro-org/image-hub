FROM balenalib/raspberry-pi-python:build

RUN apt-get update &&\
    apt-get install gcc ffmpeg libsm6 libxext6 cmake -y

RUN pip install --upgrade pip setuptools wheel &&\
    pip install numpy flask opencv-python-headless

WORKDIR /app

CMD ["python", "app.py"] 
