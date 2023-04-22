# Node version used
FROM node:18-alpine

# Specify node environment
ENV NODE_ENV=development

# Create a directory for the app
WORKDIR /app

# Copy the frontend code
COPY ../webapp .

# Install frontend dependencies
RUN npm install

# Set the working directory for the app
WORKDIR /app/webapp

# Start the frontend server
CMD [ "npm", "run", "dev" ]
