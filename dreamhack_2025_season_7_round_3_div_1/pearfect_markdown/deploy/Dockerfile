FROM php:7.4-apache

RUN a2enmod rewrite

COPY . /var/www/html/

RUN RANDOM_STR=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32) && \
    mv /var/www/html/flag /${RANDOM_STR}_flag

RUN chmod -R 777 /var/www/html/uploads

EXPOSE 80
