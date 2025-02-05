# Use official Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy frontend code
COPY . .

# Install dependencies
RUN npm install

# Build project
RUN npm run build

# Expose port
EXPOSE 3000

# Start frontend
CMD ["npm", "start"]
