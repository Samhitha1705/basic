pipeline {
    agent any

    environment {
        IMAGE_NAME = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-app-container"
        HOST_PORT = "5002"
        CONTAINER_PORT = "5002"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "📖 Checking out source code from Git"
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🛠️ Building Docker image"
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                echo "🛑 Stopping old container if exists"
                bat """
                docker stop ${CONTAINER_NAME} || echo 'No container running'
                docker rm ${CONTAINER_NAME} || echo 'No container to remove'
                """
            }
        }

        stage('Run New Container') {
            steps {
                echo "▶️ Running new container"
                bat "docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE_NAME}"
            }
        }

        stage('Health Check') {
            steps {
                echo "🔍 Checking if container is running"
                bat "docker ps -a | findstr ${CONTAINER_NAME}"
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline FAILED!"
        }
    }
}
