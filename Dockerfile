FROM balenalib/raspberrypi3-python:3.7-buster-build


RUN apt update

RUN apt install cmake make ninja-build libzmq5 libvorbisenc2 libavformat58 libva-drm2 libpangoft2-1.0-0 libvdpau1 libatlas3-base libgfortran5 libxvidcore4 libgme0 libgraphite2-3 libwebpmux3 libchromaprint1 libopus0 libshine3 libcairo2 libvorbis0a libpango-1.0-0 libdatrie1 libbluray2 libmpg123-0 libsoxr0 libsnappy1v5 libdrm2 libva-x11-2 libcairo-gobject2 libavutil56 libxfixes3 libvorbisfile3 librabbitmq4 libthai0 libopenjp2-7 libxrender1 libaom0 libspeex1 libva2 libsodium23 libswscale5 libopenmpt0 libpangocairo-1.0-0 libharfbuzz0b libmp3lame0 libzvbi0 libtheora0 libgsm1 libtwolame0 ocl-icd-libopencl1 libswresample3 libxcb-shm0 libavcodec58 libnorm1 librsvg2-2 libssh-gcrypt-4 libxcb-render0 libpixman-1-0 libwavpack1 libogg0


RUN pip install --upgrade pip setuptools wheel
RUN pip install --extra-index-url https://www.piwheels.org/simple opencv-python-headless 
RUN pip install flask flask-cors

WORKDIR /app

CMD ["python", "app.py"] 
