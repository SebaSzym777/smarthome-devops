pipeline {
    agent any

    environment {
        BACKEND_IMAGE = 'smarthome-backend:latest'
        FRONTEND_IMAGE = 'smarthome-frontend:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }   
        stage('Clean') {
            steps {
                // Zatrzymaj i usuń wszystkie kontenery oprócz tych zawierających "jenkins" w nazwie lub obrazie
                sh '''
                echo "Stopping and removing all containers except Jenkins..."

                # Pobierz listę kontenerów, filtrując te, które NIE zawierają słowa "jenkins"
                containers_to_remove=$(docker ps -aq --filter "name!=jenkins")

                if [ -n "$containers_to_remove" ]; then
                    docker stop $containers_to_remove
                    docker rm $containers_to_remove
                else
                    echo "No containers to remove"
                fi
                '''
            }
        }

        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'docker build -t $BACKEND_IMAGE .'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'docker build -t $FRONTEND_IMAGE .'
                }
            }
        }

        stage('Restart Stack (backend + frontend + db)') {
            steps {
                // Wymusza restart z nowo zbudowanych obrazów
                sh 'docker compose up -d --build backend frontend db'
            }
        }

        stage('Success') {
            steps {
                echo '✅ Cały system uruchomiony poprawnie (backend + frontend + baza danych)!'
            }
        }
    }
}
