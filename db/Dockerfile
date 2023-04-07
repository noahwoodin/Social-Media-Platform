# Use the official MongoDB image as the base image
FROM mongo:latest

COPY db/db-init.js /docker-entrypoint-initdb.d/

# Expose the default MongoDB port
EXPOSE 27017
