# Use the specific Playwright image version as a parent image
FROM mcr.microsoft.com/playwright:v1.47.2-focal

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Install wait-on 
RUN npm install -g wait-on

# Copy the rest of the code
COPY . .

# Expose port 5173
EXPOSE 5173

# Run the application
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]