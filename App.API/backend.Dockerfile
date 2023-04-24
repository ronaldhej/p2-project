FROM python:3.10

# Install mesa-utils
RUN apt-get update && \
    apt-get install -y mesa-utils

# Set the working directory
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port and start the application
EXPOSE 8000
CMD ["bash", "-c", "source venv/bin/activate && exec uvicorn server:app --host 0.0.0.0 --port 8000"]

