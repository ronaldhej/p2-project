echo "starting on display ${DISPLAY}..."
sudo Xvfb $DISPLAY -screen 0 1024x768x24
echo "display setup complete"
uvicorn server:app --host 0.0.0.0 --port 8000