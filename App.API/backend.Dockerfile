# Python version used
FROM python:3.10

# Set up virtual display
ENV DISPLAY=:99

# Install Xvfb and other dependencies
RUN apt-get update && \
    apt-get install -y xvfb libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Start Xvfb and server
CMD ["bash", "-c", "Xvfb $DISPLAY -screen 0 1024x768x24 > /dev/null 2>&1 & \
                     sleep 1 && \
                     source venv/bin/activate && \
                     exec uvicorn server:app --host 0.0.0.0 --port 8000"]
