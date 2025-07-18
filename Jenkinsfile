pipeline {
  agent any

  environment {
    PROJECT_DIR = 'smarthome-app'
    BACKEND_IMAGE = 'smarthome-backend'
    FRONTEND_IMAGE = 'smarthome-frontend'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Backend') {
      steps {
        dir("${PROJECT_DIR}/backend") {
          echo '📦 Buduję backend...'
          sh 'docker build -t ${BACKEND_IMAGE} .'
        }
      }
    }

    stage('Build Frontend') {
      steps {
        dir("${PROJECT_DIR}/frontend") {
          echo '🎨 Buduję frontend...'
          sh 'docker build -t ${FRONTEND_IMAGE} .'
        }
      }
    }

    stage('Start Stack') {
      steps {
        dir("${PROJECT_DIR}") {
          echo '🚀 Uruchamiam backend + frontend + db + nginx...'
          sh 'docker compose up -d'
        }
      }
    }

    stage('Success') {
      steps {
        echo '✅ Aplikacja Smart Home została zbudowana i uruchomiona!'
      }
    }
  }

  post {
    failure {
      echo '❌ Błąd w pipeline!'
    }
  }
}
