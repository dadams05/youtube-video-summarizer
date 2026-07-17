import os
import time
import ollama
import subprocess
from datetime import datetime


URL = "https://www.youtube.com/watch?v=uy6GFMwFDVs" # url of the youtube video to download 
OUT_DIR = "./out/" # directory for outputted files; subdirectories will be made for each video

OLLAMA_MODEL = "qwen2.5:14b" # ollama model to use
OLLAMA_HOST = os.getenv("OLLAMA_HOST", None) # used to see if in docker container or not

if OLLAMA_HOST: # these are paths in the docker container
    WHISPER = "./whisper-bin-ubuntu-x64/whisper-cli"
    WHISPER_MODEL = "./ggml-base.en.bin"
    YTDLP = "./yt-dlp"
else: # these are local paths; if not using docker, change these
    WHISPER = "./deps/whisper-cli.exe"
    WHISPER_MODEL = "./deps/ggml-base.en.bin"
    YTDLP = "./deps/yt-dlp.exe"

# prompt to give to the ollama model
PROMPT = """ 
Act as a technical scribe. Your goal is to create a complete, exhaustive summary of the provided transcript.
Do not omit any technical information, formulas, or logical steps. Structure your response as follows:
1. High-Level Scope: A brief summary of the video"s domain and objective.
2. Master Vocabulary & Definitions: A comprehensive glossary of every technical term, variable, or concept defined in the transcript.
3. Mathematical & Logical Framework: Extract every formula, theorem, or logic chain mentioned. Present all equations using clear LaTeX notation (e.g., $E = mc^2$). If the video presents a derivation, summarize the logical steps clearly.
4. Detailed Technical Breakdown: A section-by-section breakdown of the content. Include every core argument, procedure, or principle discussed. Ensure that no technical details or "rules of thumb" mentioned by the speaker are missing.
5. References & Constraints: List any specific tools, prerequisites, hardware, or external resources mentioned.
Instructions:
- Maintain maximum technical fidelity.
- If a concept is complex, explain it as it was explained in the transcript.
- Do not simplify or "dumb down" the material.
- If the speaker provides examples, summarize those examples to illustrate the theory.
- Include as much information from the transcript as possible.
Transcript Content:\n
"""


def log(msg: str) -> None:
    print(f"[{datetime.now()}] {msg}")


############################################################################################################

log("Starting...")
os.makedirs(OUT_DIR, exist_ok=True)
start_time = time.perf_counter()

# 1. get the name of the youtube video
video_name_result = subprocess.run(
    [YTDLP, "-o", "%(title)s.%(ext)s", "--print", "filename", URL], 
    capture_output=True, 
    text=True, 
    check=True
)
video_name = video_name_result.stdout.strip()[:-5]
os.makedirs(os.path.join(OUT_DIR, video_name), exist_ok=True)
VIDEO_DIR = os.path.join(OUT_DIR, video_name)

# 2. download the audio file from the youtube video url
log(f"Downloading audio from YouTube video: {video_name}")
start_download = time.perf_counter()
subprocess.run([YTDLP, "-x", "-o", os.path.join(VIDEO_DIR, "%(title)s.%(ext)s"), "--audio-format", "mp3", "--audio-quality", "0", URL])
end_download = time.perf_counter()
log(f"Finished downloading YouTube audio file ({(end_download - start_download):.5f} sec)")

# 3. extract the dialogue from the audio file
log("Extracting transcript from audio file")
start_whisper = time.perf_counter()
subprocess.run([WHISPER, "-m", WHISPER_MODEL, "-f", os.path.join(VIDEO_DIR, video_name+".mp3"), "--output-txt"])
end_whisper = time.perf_counter()
log(f"Finished extracting transcript ({(end_whisper - start_whisper):.5f} sec)")

# 4. load the transcript text into memory
with open(os.path.join(VIDEO_DIR, video_name+".mp3.txt"), "r", encoding="utf-8") as file:
    transcript = file.read()

# 5. summarize/analyze the transcript using ollama
log("Summarizing/analyzing transcript file")
start_ollama = time.perf_counter()
if OLLAMA_HOST:
    response = ollama.Client(host=OLLAMA_HOST).generate(model=OLLAMA_MODEL, prompt=PROMPT+transcript)
else:
    response = ollama.generate(model=OLLAMA_MODEL, prompt=PROMPT+transcript)
end_ollama = time.perf_counter()
log(f"Finished summarizing/analyzing transcript file ({(end_ollama - start_ollama):.5f} sec)")

# 6. save to output file
markdown_file = video_name+".md"
log(f"Saving summary/analysis to file: {markdown_file}")
with open(os.path.join(VIDEO_DIR, markdown_file), "w", encoding="utf-8") as f:
    f.write(response["response"])

# 7. output total time taken
end_time = time.perf_counter()
log(f"Total time: {(end_time - start_time):.5f} sec")
