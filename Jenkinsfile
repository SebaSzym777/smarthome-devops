pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'sebaszym77'
        BACKEND_IMAGE = "${DOCKERHUB_USER}/smarthome-backend:latest"
        FRONTEND_IMAGE = "${DOCKERHUB_USER}/smarthome-frontend:latest"
        KUBECONFIG_CREDENTIALS_ID = 'KUBECONFIG'
    }

    stages {
        stage('Build Backend') {
            steps {
                dir('smarthome-app/backend') {
                    sh "docker build -t ${BACKEND_IMAGE} ."
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir('smarthome-app/frontend') {
                    sh "docker build -t ${FRONTEND_IMAGE} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                        echo "$PASS" | docker login -u "$USER" --password-stdin
                        docker push ${BACKEND_IMAGE}
                        docker push ${FRONTEND_IMAGE}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: env.KUBECONFIG_CREDENTIALS_ID, variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl set image deployment/backend backend=${BACKEND_IMAGE} -n smarthome
                        kubectl set image deployment/frontend frontend=${FRONTEND_IMAGE} -n smarthome
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment zakończony sukcesem!'
        }
        failure {
            echo '❌ Błąd podczas wdrażania!'
        }
    }
}
