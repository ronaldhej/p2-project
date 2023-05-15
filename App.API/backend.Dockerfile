# Python version used
FROM python:3.10

ENV SLEEP_TIME_SETUP=5
ENV ARCADE_HEADLESS=True
ENV DISPLAY=:99

# Install Xvfb and other dependencies
RUN apt-get update && \
    apt-get install -y x11vnc xvfb fluxbox libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

#setup startup script
#remove '\r' characters, in case script was edited on windows machine
RUN sed -i 's/\r//g' startup.sh
RUN chmod +x startup.sh

# Expose port 8000 for incoming traffic
EXPOSE 8000

CMD [ "/bin/bash", "-c", "./startup.sh" ]