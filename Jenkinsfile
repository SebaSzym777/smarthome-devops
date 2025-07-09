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

        stage('Stop all containers (except Jenkins)') {
            steps {
                script {
                    // Zatrzymaj wszystkie kontenery oprócz Jenkinsa
                    sh '''
                    echo "Stopping all containers (except Jenkins)..."
                    for container in $(docker ps -q); do
                        name=$(docker inspect --format='{{.Name}}' $container | sed 's/\\///g')
                        if [[ "$name" != *"jenkins"* ]]; then
                            echo "Stopping container: $name"
                            docker stop $container || true
                        fi
                    done
                    '''
                }
            }
        }

        stage('Remove old containers (except Jenkins)') {
            steps {
                script {
                    // Usuń wszystkie zatrzymane kontenery oprócz Jenkinsa
                    sh '''
                    echo "Removing all stopped containers (except Jenkins)..."
                    for container in $(docker ps -aq); do
                        name=$(docker inspect --format='{{.Name}}' $container | sed 's/\\///g')
                        if [[ "$name" != *"jenkins"* ]]; then
                            echo "Removing container: $name"
                            docker rm $container || true
                        fi
                    done
                    '''
                }
            }
        }

        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'docker build --no-cache -t $BACKEND_IMAGE .'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'docker build --no-cache -t $FRONTEND_IMAGE .'
                }
            }
        }

        stage('Start containers') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Success') {
            steps {
                echo '✅ System uruchomiony: backend + frontend + baza danych!'
            }
        }
    }
}
