@echo off

echo ### Starting docker compose
docker-compose up -d

echo ### Downloading ollama model to container... (This may take a while)
docker exec ollama ollama pull qwen2.5:14b

echo ### Setup complete!
echo ### You can now run the summarizer using: docker exec summarizer python /usr/src/app/main.py
