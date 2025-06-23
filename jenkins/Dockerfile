FROM jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*

ARG DOCKER_GID=1000

# Jeśli istnieje grupa z GID=1000, to dodaj jenkinsa do niej, w przeciwnym razie zmień GID grupy docker
RUN existing_group=$(getent group ${DOCKER_GID} | cut -d: -f1) && \
    if [ -n "$existing_group" ]; then \
        usermod -aG $existing_group jenkins; \
    else \
        groupmod -g ${DOCKER_GID} docker && usermod -aG docker jenkins; \
    fi

USER jenkins
