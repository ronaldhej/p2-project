FROM python:3.10

# Install Mesa Utils for OpenGL support
RUN apt-get update && apt-get install -y mesa-utils

# Install Node.js and npm
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /the/workdir/path

# Copy the backend code and install requirements
COPY App.API/requirements.txt .
RUN pip install -r requirements.txt
COPY App.API .

# Copy the frontend code
COPY App.Web/webapp .

# Install frontend dependencies and build the app
WORKDIR /the/workdir/path/App.Web/webapp
COPY App.Web/webapp/package*.json ./
RUN npm install
COPY App.Web/webapp/. ./
#RUN npm run dev

# Copy the built frontend to the static folder
WORKDIR /the/workdir/path
RUN mkdir -p ./static && cp -R ./App.Web/webapp/* ./static

# Expose the port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
