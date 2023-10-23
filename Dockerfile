# FROM ubuntu:22.04
FROM ubuntu:latest

# RUN DEBIAN_FRONTEND=noninteractive \
#   apt-get update \
#   && apt-get install -y software-properties-common \
#   && add-apt-repository ppa:deadsnakes/ppa \
#   && apt-get update \
#   && apt-get install -y python3.9 \
#   && apt-get install -y git \
#   && rm -rf /var/lib/apt/lists/*

RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && apt-get install -y python3 \
  && apt-get install -y git \
  && rm -rf /var/lib/apt/lists/*

# # set a directory for the app
WORKDIR /usr/src/app

RUN mkdir ~/.ssh
ARG ssh_prv_key
ARG ssh_pub_key

RUN echo "$ssh_prv_key" > /root/.ssh/id_ed25519 && \
    echo "$ssh_pub_key" > /root/.ssh/id_ed25519.pub && \
    chmod 600 /root/.ssh/id_ed25519 && \
    chmod 600 /root/.ssh/id_ed25519.pub && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts && \
    git clone git@github.com:payanaapp/TravelFont.git && \
    rm /root/.ssh/id_ed25519*

# install PIP and virtualenv
RUN apt-get update && apt-get install -y python3-pip

# Set TravelFont home variable
ARG travelfont_home_arg_value=default_value
ENV travelfont_home=$travelfont_home_arg_value

# Set GOOGLE_APPLICATION_CREDENTIALS home variable
ARG GOOGLE_APPLICATION_CREDENTIALS=default_value
ENV GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS

# Set GOOGLE_MAIL_SERVICE_CREDENTIALS home variable
ARG GOOGLE_MAIL_SERVICE_CREDENTIALS=default_value
ENV GOOGLE_MAIL_SERVICE_CREDENTIALS=$GOOGLE_MAIL_SERVICE_CREDENTIALS

# Execute starter scripts
RUN pip3 install -r $travelfont_home/payana/payana_bl/requirements.txt
RUN pip3 install -r $travelfont_home/payana/payana_service/requirements.txt
RUN pip3 install -r $travelfont_home/payana/payana_core/requirements.txt
# install the below package separately as it fails if installed from requirements.xt
RUN pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

WORKDIR $travelfont_home 
RUN python3 $travelfont_home/setup.py build && python3 $travelfont_home/setup.py install

# payana bigtable init -  one time run
# payana_cloud_storage_init GCS - one time run

ENTRYPOINT [ "python3", "payana_service_start.py"]