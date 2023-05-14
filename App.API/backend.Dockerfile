# Python version used
FROM python:3.10

ENV ARCADE_HEADLESS=1
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


#Setup virtual display


COPY . .


RUN chmod +x startup.sh

# Expose port 8000 for incoming traffic
EXPOSE 8000


CMD ["bash", "-c", "./startup.sh"]