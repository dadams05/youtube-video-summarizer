mkdir deps
cd deps

curl -LO https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
tar -xvf ffmpeg-release-essentials.zip
for /f "delims=" %%i in ('dir "ffmpeg-*" /ad /b /s') do set "FFMPEG_FOLDER=%%i"
move %FFMPEG_FOLDER%\bin\ffmpeg.exe .

rmdir /s /q %FFMPEG_FOLDER%
del ffmpeg-release-essentials.zip

curl -LO https://github.com/ggml-org/whisper.cpp/releases/download/v1.9.1/whisper-bin-x64.zip
tar -xvf whisper-bin-x64.zip
move Release\*.dll .
move Release\whisper-cli.exe .
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin

rmdir /s /q Release
del whisper-bin-x64.zip

curl -LO https://github.com/yt-dlp/yt-dlp/releases/download/2026.07.04/yt-dlp.exe

cd ..

py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install --upgrade pip
