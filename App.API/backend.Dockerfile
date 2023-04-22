FROM python:3.10

# Install mesa-utils
RUN apt-get update && \
    apt-get install -y mesa-utils

# Set the working directory
WORKDIR /the/workdir/path

# Copy the backend code and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Expose the ports
#EXPOSE 8000

# Start the backend server
CMD ["uvicorn", "server:app"] 
