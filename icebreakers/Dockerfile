FROM php:8.2.4-cli
COPY . /usr/src/app
# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        git 


# Install required extensions
RUN docker-php-ext-install pdo_mysql

# Install composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer


# Copy Laravel files
WORKDIR /usr/src/app/icebreakers

RUN composer install --no-interaction --no-plugins --no-scripts
RUN chown -R www-data:www-data storage bootstrap/cache && chmod -R 775 storage bootstrap/cache
# Set environment variables
ENV DB_CONNECTION=mysql
ENV DB_HOST=host.docker.internal
ENV DB_PORT=3306
ENV DB_DATABASE=icebreakers
ENV DB_USERNAME=root
ENV DB_PASSWORD=root
RUN chmod +x /usr/src/app/icebreakers
# Expose port 6101
EXPOSE 6101

# Start the API server
# CMD ["php", "artisan" ,"db:seed", "--class=IcebreakersSeeder"]
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=6101"]


