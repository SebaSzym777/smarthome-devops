pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "smarthome-backend"
        FRONTEND_IMAGE = "smarthome-frontend"
    }

    stages {
        stage('Build Backend') {
            steps {
                dir('backend') {
                    script {
                        echo "📦 Budowanie backendu..."
                        sh 'docker build -t $BACKEND_IMAGE .'
                    }
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    script {
                        echo "🎨 Budowanie frontendu..."
                        sh 'docker build -t $FRONTEND_IMAGE .'
                    }
                }
            }
        }

        stage('Success') {
            steps {
                echo '✅ Backend i frontend zostały zbudowane pomyślnie!'
            }
        }
    }
}
