# Pull base image
FROM centos:latest

# Contributors
MAINTAINER Kyler Witting <kyler.witting@target.com>

USER root
ENV HOME /opt/webbreaker
WORKDIR /opt/webbreaker

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

CMD ["bash"]

# Create & setup venv
# install dep for python2.7
# Install dep for python3.6
RUN pip install --upgrade pip \
	virtualenv \ 
&& virtualenv -p python2.7 /root/venv27 \
&& virtualenv -p python3.6 /root/venv36	\
<<<<<<< HEAD
&& echo 'source /root/venv27/bin/activate' >> ~/.bashrc \
&& echo 'alias venv27="source /root/venv27/bin/activate"' >> ~/.bashrc \
&& echo 'alias venv36="source /root/venv36/bin/activate"' >> ~/.bashrc \
&& echo 'export LC_ALL="en_US.UTF-8"' >> ~/.bashrc \
&& echo 'export LANG="en_US.UTF-8"' >> ~/.bashrc \
&& source /root/venv27/bin/activate \
&& pip install \
	cryptography \
	detox \
	click \
	'configparser>=3.5.0' \
        'dpath>=1.4.0' \
        'fortifyapi>=1.0.6' \
        gitpython \
        httplib2 \
        mock \
        ndg-httpsclient \
        pyasn1 \
        'pyfiglet>=0.7.5' \
        pyOpenSSL \
        pytest-runner \
        requests \
        testfixtures \
        validators \
        'webinspectapi>=1.0.15' \
&& source /root/venv36/bin/activate \
&& pip install \
	cryptography \
	detox \
	click \
	'configparser>=3.5.0' \
        'dpath>=1.4.0' \
        'fortifyapi>=1.0.6' \
        gitpython \
        httplib2 \
        mock \
        ndg-httpsclient \
        pyasn1 \
        'pyfiglet>=0.7.5' \
        pyOpenSSL \
        pytest-runner \
        requests \
        testfixtures \
        validators \
        'webinspectapi>=1.0.15'

# Add webbreaker code
ADD . /opt/webbreaker

# Install webbreaker for both venv
RUN source /root/venv27/bin/activate \
&& python setup.py install 
#&& source /root/venv36/bin/activate \
#&& python setup.py install

ONBUILD venv27

