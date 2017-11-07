# Pull base image
FROM centos:latest

# Contributors
MAINTAINER Kyler Witting <kyler.witting@target.com>

USER root
ENV HOME /opt/webbreaker
WORKDIR /opt/webbreaker

# Update centos 7 & install packages & clean centos 7
RUN yum update -y && yum install -y \
	epel-release \
	https://centos7.iuscommunity.org/ius-release.rpm \ 
&& yum install -y \
	git \
	python-pip \
	python36u \ 
&& yum clean all 

CMD ["bash"]

# Setup env
ADD requirements.txt /root/
RUN pip install --upgrade pip \
	virtualenv \ 
&& virtualenv -p python2.7 /root/venv27 \
&& virtualenv -p python3.6 /root/venv36	\
&& echo 'source /root/venv27/bin/activate' >> ~/.bashrc \
&& echo 'alias venv27="source /root/venv27/bin/activate"' >> ~/.bashrc \
&& echo 'alias venv36="source /root/venv36/bin/activate"' >> ~/.bashrc \
&& echo 'export LC_ALL="en_US.UTF-8"' >> ~/.bashrc \
&& echo 'export LANG="en_US.UTF-8"' >> ~/.bashrc \
&& source /root/venv27/bin/activate \
&& pip install -r /root/requirements.txt \
&& source /root/venv36/bin/activate \
&& pip install -r /root/requirements.txt 

# Add webbreaker code
ADD . /opt/webbreaker

# Install webbreaker for both venv
RUN source /root/venv27/bin/activate \
&& python setup.py install \
&& source /root/venv36/bin/activate \		
&& python setup.py install

ONBUILD venv36

