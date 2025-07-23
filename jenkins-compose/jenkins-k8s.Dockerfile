FROM jenkins/jenkins:lts

USER root

# Zainstaluj Docker CLI i curl
RUN apt-get update && \
    apt-get install -y docker.io curl

# Zainstaluj konkretną wersję kubectl
ARG KUBECTL_VERSION=v1.30.1
RUN curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

USER jenkins
