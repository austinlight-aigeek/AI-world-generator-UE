# Use a lightweight Node.js image
FROM node:18-slim

# Set working directory
WORKDIR /app

# Copy package.json first (to leverage Docker caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the entire project
COPY . .

# Build the project
RUN npm run build

# Expose port for development
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
