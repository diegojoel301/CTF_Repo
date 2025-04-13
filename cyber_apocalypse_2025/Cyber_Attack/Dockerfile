FROM php:7.4-apache

# Install necessary extensions and tools
RUN apt-get update && apt-get install -y \
    supervisor \
    unzip 

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Enable Apache modules
RUN a2enmod rewrite cgi proxy proxy_fcgi proxy_http

# Set working directory
WORKDIR /var/www/html

# Copy source files
COPY src/ /var/www/html/

# Copy Supervisor configuration
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy Apache configuration
COPY apache/apache2.conf /etc/apache2/conf-available/servername.conf
RUN a2enconf servername

# Move CGI script to the correct location
RUN mv /var/www/html/cgi-bin/ /usr/lib/ && chmod -R +x /usr/lib/cgi-bin/

# Copy flag
COPY flag.txt /flag.txt

# Copy entry script
COPY entry.sh entry.sh
RUN chmod +x entry.sh

# Expose port 80 for Apache
EXPOSE 80

# Command to run entry script
CMD ["./entry.sh"]