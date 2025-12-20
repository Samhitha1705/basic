pipeline {
    agent any

    environment {
        IMAGE_NAME = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-container"
        APP_PORT = "5002"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "📂 Checking out source code from Git"
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🚀 Building Docker image"
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                echo "🧹 Cleaning old container if exists"
                script {
                    bat """
                    docker stop ${CONTAINER_NAME} || echo Container not running, continuing...
                    docker rm ${CONTAINER_NAME} || echo Container not present, continuing...
                    """
                }
            }
        }

        stage('Run New Container') {
            steps {
                echo "🏃 Running new container on port ${APP_PORT}"
                bat "docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${IMAGE_NAME}"
            }
        }

        stage('Health Check') {
            steps {
                echo "💓 Health Check stage skipped (optional to implement later)"
            }
        }
    }

    post {
        success {
            echo "✅ Jenkins Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline FAILED!"
        }
    }
}
