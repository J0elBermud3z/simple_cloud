FROM debian:bookworm

RUN apt-get update && \
    apt-get install -y apache2 apache2-utils && \
    a2enmod proxy proxy_http proxy_wstunnel rewrite && \
    apt-get clean

COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

EXPOSE 80

CMD ["apache2ctl", "-D", "FOREGROUND"]
