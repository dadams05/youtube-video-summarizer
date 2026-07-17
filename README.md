# Local Video Summarizer

A private tool for summarizing video content locally using Ollama. This project can be run natively on Windows or fully containerized via Docker. I have not tested this project on Linux so this guide will not include instructions for Linux users (sorry, but the Docker section and files should be a good reference).

## System Prerequisites: NVIDIA GPU

No matter which installation path you choose below, an NVIDIA GPU is highly recommended.

1. **Check Driver Version**
Run the following command in your terminal:
```bash
nvidia-smi
```

Look for the **Driver Version** and **CUDA Version** in the top-right corner. It should read `550.x` or higher. If it is outdated, download and update your driver directly from the NVIDIA Drivers page.

2. **Verify Ollama GPU Detection**
If your driver is up-to-date, Ollama should automatically detect it. You can verify the model is loaded into VRAM by running the following command while a model is active:
```bash
ollama ps
```

If it successfully uses your GPU, you will see a device listed (e.g., `gpu` or `cuda`). If it says `cpu`, Ollama is silently falling back to processing on your processor, which will be significantly slower.

---

## Option 1: Native Windows Setup

*Best for users who prefer working directly on their host machine without Docker.*

**Requirements:**

* **Python 3.10+** installed and added to PATH.
* **Ollama** installed and running on your machine.
* Your desired model must be downloaded in Ollama (e.g., `ollama pull qwen2.5:14b`).

**Installation & Execution:**

1. Run the Windows setup script to download dependencies (FFmpeg, Whisper, yt-dlp) and configure the environment:
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

*Processed files and summaries will be saved to the `out/<video_name>/` directory.*

---

## Option 2: Docker Setup

*Best for a consistent environment, automated dependency management, and keeping your host machine clean.*

**Requirements:**

* **Docker Desktop** installed and running.
* A little patience during the initial image build.

**1. Verify Docker GPU Access**
Before building the project, ensure Docker can communicate with your NVIDIA GPU by running:

```bash
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```

*(If this fails, you may need to check your Docker Desktop settings to ensure GPU virtualization is enabled).*

**2. Setup and Run**
Once verified, simply run the setup script whenever you want to start the project. This script will boot the containers and pull the necessary models:
```cmd
docker_setup.cmd
```

### Docker Development Cheat Sheet

If you are developing or modifying the code, use these commands to manage the container lifecycle:

| Task | Command |
| --- | --- |
| **Start Project** | `docker-compose up -d` |
| **Restart (Code Changes)** | `docker-compose up -d --force-recreate summarizer` |
| **Rebuild (Dependency Changes)** | `docker-compose up -d --build` |
| **Stop Project** | `docker-compose down` |

> **Workflow Tip:** When editing `main.py`, you don't need to do a full rebuild. Just run the **Restart** command to spin up a fresh container with your new code.

---

## Changing the LLM Model

If you want to use a different model for summarization, you must update the code **and** download the model to your environment.

1. Open `main.py` and update the model variable to your desired model name.
2. Manually pull the new model:
* **If using Windows Native:** Run `ollama pull <model_name>` in your standard command prompt.
* **If using Docker:** Run `docker exec ollama ollama pull <model_name>` to download it directly into the running container.

---

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
