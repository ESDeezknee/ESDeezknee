FROM php:8.2.4-cli
COPY . /usr/src/app
# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        unzip \
        libzip-dev

# Enable required PHP extensions
RUN docker-php-ext-install pdo_mysql zip

# Copy Laravel files
WORKDIR /usr/src/app/icebreakers

# Set environment variables
ENV DB_CONNECTION=mysql
ENV DB_HOST=host.docker.internal
ENV DB_PORT=3306
ENV DB_DATABASE=icebreakers
ENV DB_USERNAME=root
ENV DB_PASSWORD=root
RUN chmod +x /usr/src/app/icebreakers
# Expose port 6109
EXPOSE 6109

# Start the API server
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=6109"]


