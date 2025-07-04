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
