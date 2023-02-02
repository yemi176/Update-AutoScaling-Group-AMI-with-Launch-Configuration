#!/bin/bash

# this script be used for Mac M1
# run jenkins
mkdir -p /var/jenkins_home
chown -R 1000:1000 /var/jenkins_home
# docker network create jenkins
#docker run -p 8080:8080 -p 50000:50000 -v /var/jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -d --name jenkins-server loantran176/jenkins-image

docker run \
  --name jenkins-docker \
  --rm \
  --detach \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind \
  --storage-driver overlay2

# show endpoint
echo 'Jenkins installed'
echo 'You should now be able to access jenkins at: http://'$(curl -s ifconfig.co)':2376'