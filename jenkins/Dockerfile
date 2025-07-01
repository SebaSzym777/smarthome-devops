FROM jenkins/jenkins:lts

USER root

# Instalacja Docker CLI w Debianie (bazowym obrazie Jenkins)
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

USER jenkins
