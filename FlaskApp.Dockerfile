############################################################
# Dockerfile to build Your Flask backend APIs
############################################################
FROM ubuntu:20.04

# Avoid tz data prompts
ENV TZ=America/New_York

############################################################
# INSTALLS
############################################################
# Get sudo set up
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install sudo

# Apache is web server software, redis is a database used to save messages in job queues, supervisor runs processes
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 libapache2-mod-wsgi-py3 supervisor openssl cron \
&& sudo apt install -y python3.8 && sudo mkdir /var/www/html/your-website \
&& sudo apt install snapd && sudo snap install curl && sudo apt install pip && sudo mkdir /var/www/Canonical-flask-app \
&& sudo mkdir /var/www/Canonical-flask-app/logs && sudo mkdir /var/www/Canonical-flask-app/static \
&& sudo mkdir /var/www/Canonical-flask-app/templates

#Config firewall to allow Apache access
RUN sudo ufw allow 'Apache' && sudo ufw enable

#want to copy over all required files and change dir
COPY ./ /var/www/Canonical-flask-app/
WORKDIR "/var/www/Canonical-flask-app/"

#install pipenv
RUN sudo apt install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

#change ownership within /var/www
RUN sudo addgroup webmasters && sudo adduser $USER webmasters && sudo chown -R root:webmasters /var/www \
&& sudo find /var/www -type d -exec chmod 775 {} \; && sudo find /var/www -type d -exec chmod g+s {} \;

RUN sudo find /var/www -type f -exec chmod 664 {} \;

#make venv directory, then populate the veng directory
RUN sudo mkdir /var/www/Canonical-flask-app/.venv/
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

#copy over apache configs for the flask app and enable the config
COPY ./apache2/sites-available/ /etc/apache2/sites-available/
RUN sudo a2ensite Canonical-flask-app.conf
RUN sudo systemctl reload apache2

#expose port that flask runs on (5000)
EXPOSE 5000

#run the Flask server
CMD ['python3','app.py']

