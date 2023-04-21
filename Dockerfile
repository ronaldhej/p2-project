FROM python:3.10

# Install Mesa Utils for OpenGL support
RUN apt-get update && apt-get install -y mesa-utils

# Install Node.js and npm
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install http-server
RUN npm install -g http-server

# Set the working directory
WORKDIR /the/workdir/path

# Copy the backend code and install requirements
COPY App.API/requirements.txt .
RUN pip install -r requirements.txt
COPY App.API .

# Copy the frontend code
COPY App.Web/webapp ./webapp

# Install frontend dependencies and build the app
WORKDIR /the/workdir/path/webapp
RUN npm install
RUN npm run build

# Copy the built frontend to the static folder
WORKDIR /the/workdir/path
RUN mkdir -p ./static && cp -R ./webapp/dist/* ./static

# Expose the ports
EXPOSE 8000
EXPOSE 3000

# Start the backend and frontend servers
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port 8000 & http-server ./static -p 3000"] 
