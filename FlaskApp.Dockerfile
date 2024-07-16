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
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 libapache2-mod-wsgi-py3 \
&& sudo apt install -y python3.8 && sudo apt install -y snapd \
&& sudo apt install -y curl && sudo apt install -y pip && sudo mkdir /var/www/Canonical-flask-app \
&& sudo mkdir /var/www/Canonical-flask-app/logs && sudo mkdir /var/www/Canonical-flask-app/static \
&& sudo mkdir /var/www/Canonical-flask-app/templates

#Config firewall to allow Apache access
#RUN sudo ufw allow 'Apache' && sudo ufw enable

#want to copy over all required files and change dir
COPY ./api/* /var/www/Canonical-flask-app/api/
COPY ./ssl_certs/* /var/www/Canonical-flask-app/ssl_certs/
COPY ./tests/* /var/www/Canonical-flask-app/tests/
COPY .flake8 /var/www/Canonical-flask-app/.flake8
COPY .pylintrc /var/www/Canonical-flask-app/.pylintrc
COPY * /var/www/Canonical-flask-app/
WORKDIR "/var/www/Canonical-flask-app/"
#RUN echo ls -laRt

#install pipenv
RUN sudo apt install -y pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

#change ownership within /var/www
RUN sudo addgroup webmasters
#RUN sudo adduser $USER webmasters
RUN sudo chown -R root:webmasters /var/www
RUN sudo find /var/www -type d -exec chmod 775 {} \;
RUN sudo find /var/www -type d -exec chmod g+s {} \;

RUN sudo find /var/www -type f -exec chmod 664 {} \;

#make venv directory, then populate the veng directory
RUN sudo mkdir /var/www/Canonical-flask-app/.venv/
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

#copy over apache configs for the flask app and enable the config
COPY ./apache2/sites-available/ /etc/apache2/sites-available/
RUN sudo a2ensite Canonical-flask-app.conf
#need this because systemctl doesnt exist in containers
RUN sudo service apache2 start
CMD ["/usr/sbin/apachectl", "-D", "FOREGROUND"]
#RUN sudo service apache2 reload
RUN chmod 777 -R /var/www/

#expose port that flask runs on (5000)
EXPOSE 443

#remove unpacked ssl certs, app.py, util and wsgi files from api and ssl certs folder
RUN sudo rm -f -- *.py *.wsgi *.csr *.crt *.key *.org *.md CACHEDIR.TAG
RUN sudo rm -rf .pytest_cache v

WORKDIR "/var/www/Canonical-flask-app/api/"
ENV PATH="/var/www/Canonical-flask-app/.venv/bin:$PATH"

#run the Flask server
CMD ["python3","app.py"]
