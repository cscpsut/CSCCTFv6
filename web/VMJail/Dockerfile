FROM node:12.22.12

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY ./source/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY ./source .

# Expose the port your app runs on
EXPOSE 3000

# Add flag to dir
RUN echo $FLAG > /app/flag.txt
COPY source/entrypoint.sh /entrypoint.sh
# Command to start the application
ENTRYPOINT [ "/entrypoint.sh" ]
