#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static.

if ! command -v nginx &> /dev/null
then
	sudo apt-get update
	sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

echo "<html><head></head><body>Holberton School</body></html>" > /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/server {/a \ \ \ \ location \/hbnb_static {\n\ \ \ \ \ \ \ \ alias \/data\/web_static\/current;}' /etc/nginx/sites-available/default

sudo service nginx restart
