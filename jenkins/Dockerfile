FROM jenkins/jenkins:lts

USER root

# Sprawdźmy, czy grupa o GID 1000 już istnieje, jeśli tak to ją wykorzystaj, jeśli nie to utwórz
RUN if ! getent group 1000; then \
      groupadd -g 1000 docker; \
    else \
      echo "Grupa o GID 1000 już istnieje"; \
    fi

# Dodajemy użytkownika jenkins do grupy o GID 1000 (nazwa może być inna, więc pobierzemy ją dynamicznie)
RUN usermod -aG $(getent group 1000 | cut -d: -f1) jenkins

USER jenkins
