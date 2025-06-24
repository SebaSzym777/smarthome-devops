FROM jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*

# Zmień GID grupy jenkins z 1000 na 2000 (lub inny wolny numer)
RUN groupmod -g 2000 jenkins

# Zmień GID grupy docker na 1000 (pasujący do hosta)
RUN groupmod -g 1000 docker

# Dodaj użytkownika jenkins do grupy docker
RUN usermod -aG docker jenkins

USER jenkins
