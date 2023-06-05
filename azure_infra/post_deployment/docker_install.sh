#! /bin/bash
# run as sudo

apt-get update -y &&\
apt-get install ca-certificates curl gnupg -y &&\
install -m 0755 -d /etc/apt/keyrings &&\
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null &&\

apt-get update -y &&\
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y &&\
chmod 777 /var/run/docker.sock &&\
apt install docker-compose -y
