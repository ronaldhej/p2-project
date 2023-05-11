CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"
echo "startup"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"
    echo "starting on display ${DISPLAY}..."
    Xvfb "${DISPLAY}" -screen 0 1024x768x16
    sleep 1
else
    echo "-- Not first container startup --"
fi

uvicorn server:app --host 0.0.0.0 --port 8000