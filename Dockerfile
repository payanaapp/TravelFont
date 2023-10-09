FROM ubuntu:22.04
# FROM ubuntu:latest

RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && apt-get install -y python3 \
  && apt-get install -y git \
  && rm -rf /var/lib/apt/lists/*

# RUN useradd -ms /bin/bash payana
# USER payana

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
