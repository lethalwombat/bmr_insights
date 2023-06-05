#! /bin/bash

# ssh keys
scp -i ~/.ssh/id_rsa ~/.ssh/id_rsa azureuser@$1:/home/azureuser/.ssh/ &&\
scp -i ~/.ssh/id_rsa ~/.ssh/id_rsa.pub azureuser@$1:/home/azureuser/.ssh/ &&\

# docker installation script
scp -i ~/.ssh/id_rsa docker_install.sh azureuser@$1:/home/azureuser &&\

# repo clone script
scp -i ~/.ssh/id_rsa repo_clone.sh azureuser@$1:/home/azureuser

# ssh into the vm
ssh -i ~/.ssh/id_rsa azureuser@$1 &&\
