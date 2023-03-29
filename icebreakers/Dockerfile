FROM php:8.2.4-cli
WORKDIR /usr/src/app
RUN docker-php-ext-install mysqli
COPY icebreakers/icebreakers.php ./
EXPOSE 6109
CMD ["php","./icebreakers.php"]