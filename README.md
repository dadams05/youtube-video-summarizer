# Local Video Summarizer

A private, local tool for summarizing YouTube videos and local video files using Ollama. This project can be run natively on Windows or fully containerized via Docker.

> **Important Notes**
> * This project was developed and tested on Windows 11 with an NVIDIA GPU. If your system specs differ significantly, it may require additional configuration.
> * This guide does not include explicit instructions for Linux users; however, the provided Docker files and instructions are a good reference for running the project on Linux.
> * This tool can summarize local video files on your hard drive, not just YouTube videos.

## System Prerequisites: Nvidia GPU

Regardless of which installation path you choose, an **Nvidia GPU is highly recommended** for better performance.

### 1. Check Driver Version

Open your terminal or Command Prompt and run:

```bash
nvidia-smi
```

Look for the **Driver Version** and **CUDA Version** in the top-right corner. It should read `550.x` or higher. If your drivers are outdated, download and install the latest version from the [Nvidia Drivers page](https://www.nvidia.com/en-us/drivers/).

### 2. Verify Ollama GPU Detection

If your driver is up-to-date, Ollama should detect your GPU automatically. You can verify that your model is loaded into VRAM by running the following command while a model is active:

```bash
ollama ps
```

If Ollama is successfully using your GPU, you will see a device listed (e.g., `gpu` or `cuda`). If it says `cpu`, Ollama is silently falling back to your processor, which will significantly slow down generation.

## Setup Instructions

Choose the setup path that best fits your current environment. If you already have Docker or Ollama installed, I recommend choosing the corresponding option below.

### Option 1: Native Windows Setup

*Best for if you prefer working directly on your host machine without Docker.*

**Requirements:**

* **Python 3.10+** installed and added to your system PATH.
* **[Ollama](https://ollama.com/)** installed and running on your machine.
* Your desired model must be downloaded in Ollama (e.g., `ollama pull <model name>`, this project uses `qwen2.5:14b` by default).

**Installation & Execution:**

1. Run the Windows setup script to download dependencies (FFmpeg, Whisper, yt-dlp) and configure the virtual environment:
```cmd
windows_setup.cmd
```

2. Activate the Python virtual environment:
```cmd
.venv\Scripts\activate
```

3. Run the summarizer:
```cmd
python main.py
```

*(Processed files and summaries will be saved to the `out/<video_name>/` directory.)*

### Option 2: Docker Setup

*Best for a consistent environment, automated dependency management, and keeping your host machine clean.*

**Requirements:**

* **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** installed and running.
* A little patience during the initial image build.

**1. Verify Docker GPU Access**
Before building the project, ensure Docker can communicate with your NVIDIA GPU by running:

```bash
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```

*(If this command fails, check your Docker Desktop settings to ensure GPU virtualization is enabled).*

**2. Setup and Run**
Once verified, run the setup script to boot the containers and pull the necessary models. After loading, the Docker container should be ready for use. Refer to the Cheat Sheet below for the commands to use to run the python script:

```cmd
docker_setup.cmd
```

#### Docker Development Cheat Sheet

If you are developing or modifying the code, use these commands to manage the container lifecycle:

| Task | Command |
| --- | --- |
| **Start Project** | `docker-compose up -d` |
| **Restart (Code Changes)** | `docker-compose up -d --force-recreate summarizer` |
| **Rebuild (Dependency Changes)** | `docker-compose up -d --build` |
| **Stop Project** | `docker-compose down` |

> When editing `main.py`, you don't need to do a full rebuild. Just run the **Restart** command to spin up a fresh container with your new code.

## Changing the LLM Model

If you want to use a different model for summarization, you must update the code **and** download the model to your environment.

1. Open `main.py` and update the `OLLAMA_MODEL` variable to your desired model name.
2. Manually pull the new model:
   * **If using Windows Native:** Run `ollama pull <model_name>` in your standard command prompt.
   * **If using Docker:** Run `docker exec ollama ollama pull <model_name>` to download it directly into the running container.

## Troubleshooting

* **Container Build Errors or "Stuck" States:**
If the Docker build fails, or you've heavily modified the `requirements.txt` or `Dockerfile` and things are acting strange, force a clean build from scratch:
```bash
docker-compose up -d --build
```
* **Storage Cleanup:**
If Docker is taking up too much disk space, you can wipe all unused data, stopped containers, and dangling images.
*Warning: Use with caution. This will remove unused data for ALL your Docker projects, not just this one.*
```bash
docker system prune -a
```
