FROM node:20.9-bullseye-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./nextjs /app/

# Copy package.json and yarn.lock
COPY ./nextjs/package.json ./nextjs/yarn.lock /app/

# Install dependencies
RUN yarn install

RUN npm run build

# Expose port 5173 to access the server
EXPOSE 80

CMD ["npm", "run", "start", "--", "-p", "80"]

