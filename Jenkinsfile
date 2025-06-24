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

        stage('Success') {
            steps {
                echo 'Build zakończony pomyślnie!'
            }
        }
    }
}
