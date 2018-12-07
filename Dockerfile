# Dev environment
#
# Makes a virtualenv at /venv which might need updating but should
# have a good base of dependencies.
#
# e.g.
#
# docker run --rm -t -i -v $PWD:$PWD jbothma/giz-projects:docker-dev-env bin/bash
# root@079d0a9aae0d:/# cd /home/jdb/proj/code4sa/giz-projects/django-app/
# root@079d0a9aae0d:/home/jdb/proj/code4sa/giz-projects/django-app# source /venv/bin/activate
# root@079d0a9aae0d:/home/jdb/proj/code4sa/giz-projects/django-app# export DATABASE_URL=postgres://giz@172.17.0.1/giz_projects
# root@079d0a9aae0d:/home/jdb/proj/code4sa/giz-projects/django-app# python manage.py runserver 0.0.0.0:8000



FROM ubuntu:trusty

ADD requirements.txt /requirements.txt

RUN apt-get update -y && \
    apt-get install -y software-properties-common && \
    apt-add-repository -y ppa:ubuntugis/ubuntugis-unstable && \
    apt-get update -y && \
    apt-get install -y  libgdal-dev=1.11* \
                        python-pip \
                        git \
                        python-gdal \
                        libgdal1-dev \
                        libncurses5-dev \
                        python-psycopg2 \
                        python-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    ln -snf /bin/bash /bin/sh

RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal && \
    export export C_INCLUDE_PATH=/usr/include/gdal && \
    pip install -r /requirements.txt

CMD ["/bin/bash"]
