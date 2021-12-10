## Usage

docker run -d \
    --name gerrit-watcher \
    --restart always \
    --pull=always \
    -e PYTHONUNBUFFERED=1 \
    -e GERRIT_URL="URL_HERE" \
    -e TELEGRAM_CHAT_ID="TELEGRAM_CHAT_ID_HERE" \
    -e TELEGRAM_TOKEN="TELEGRAM_TOKEN" \
    -e GERRIT_STATUS_TO_LISTEN="open;merged;abandoned" \
    -v LOCAL_DATA_PATH:/app/data \
    gitlab.pixelexperience.org:5050/infra/docker/gerrit-watcher:latest