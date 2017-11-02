#
# CentOS 7 Dockerfile
#

# Pull base image
FROM centos:latest

# Contributors
MAINTAINER Kyler Witting <kyler.witting@target.com>

USER root
ENV HOME /opt/webbreaker
WORKDIR /root

# Update CentOS 7 & Install packages & Clean CentOS 7
RUN yum update -y && yum install -y \
	unzip \
	wget \ 
	curl \ 
	git \
	epel-release \
	https://centos7.iuscommunity.org/ius-release.rpm \ 
&& yum install -y \
	python-pip \
	python36u \ 
&& yum clean all 

# Default command
CMD ["bash"]

RUN pip install --upgrade pip \
	virtualenv \ 
&& virtualenv -p python2.7 /root/venv27 \
&& virtualenv -p python3.6 /root/venv36	\
&& echo 'alias venv27="source /root/venv27/bin/activate"' >> ~/.bashrc \
&& echo 'alias venv36="source /root/venv36/bin/activate"' >> ~/.bashrc
