# image-hub
Image processing with opencv

Opencv + Flask image proxy.
Handels rectification, streaming, measurement, ....

```
docker build -t image-hub .

docker run -it --rm -v ${PWD}/app:/app -p 5000:5000 -e CAM_RIGHT_URL="" -e CAM_LEFT_URL="" image-hub /bin/bash

docker run --rm -d --restart always --name=image-hub -v ${PWD}/app:/app -p 5000:5000 -e CAM_RIGHT_URL="" -e CAM_LEFT_URL="" image-hub

```
