# base OS or another image that is based on os
FROM Ubuntu

RUN apt-get update && apt-get -y install python

RUN pip install flask flask -mysql

# copy source code from the current folder to the location
COPY . /opt/source-code

ENTRYPOINT FLASK_APP=/opt/source-code/app.py flask run