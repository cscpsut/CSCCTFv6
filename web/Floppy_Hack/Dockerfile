# Use an official PHP image with Apache
FROM php:8.1-apache

# # Enable Apache mod_rewrite (optional but common for many PHP apps)
# RUN a2enmod rewrite

# Set the working directory inside the container
WORKDIR /var/www/html

# Copy the local PHP application files into the container
COPY ./source /var/www/html/

RUN mkdir -p /var/www/html/uploads && chmod -R 777 /var/www/html/uploads
# Expose the port Apache is running on
EXPOSE 80
COPY entrypoint.sh /entrypoint.sh
# Start the Apache service when the container runs
ENTRYPOINT [ "/entrypoint.sh" ]