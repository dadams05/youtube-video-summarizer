# builds an image with the Python 3.15 image
FROM python:3.15-rc-slim-trixie

# sets the working directory to `/usr/src/app`
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# get whisper and model
RUN curl -LO https://github.com/ggml-org/whisper.cpp/releases/download/v1.9.1/whisper-bin-ubuntu-x64.tar.gz && \
    tar -xvf whisper-bin-ubuntu-x64.tar.gz && \
    chmod +x ./whisper-bin-ubuntu-x64/whisper-cli
RUN curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin -o ggml-base.en.bin

# get ytdlp
RUN curl -LO https://github.com/yt-dlp/yt-dlp/releases/download/2026.07.04/yt-dlp && \
    chmod +x ./yt-dlp
 
# copies `requirements.txt` into docker image
COPY requirements.txt ./
# installs the Python dependencies
RUN pip install -r requirements.txt
