pipeline {
    agent any

    environment {
        IMAGE_NAME     = "fullstack-sqlite:latest"
        CONTAINER_NAME = "fullstack_sqlite_app"
        APP_PORT       = "5002"
    }

    stages {

        stage("Checkout Code") {
            steps {
                echo "📥 Checking out source code"
                checkout scm
            }
        }

        stage("Build Docker Image") {
            steps {
                echo "🐳 Building Docker image"
                sh """
                docker build -t ${IMAGE_NAME} .
                """
            }
        }

        stage("Stop & Remove Old Container") {
            steps {
                echo "🧹 Cleaning old container (if exists)"
                sh """
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                """
            }
        }

        stage("Run New Container") {
            steps {
                echo "🚀 Starting application container on port ${APP_PORT}"
                sh """
                docker run -d \
                  --name ${CONTAINER_NAME} \
                  -p ${APP_PORT}:${APP_PORT} \
                  -v \$(pwd)/data:/app/data \
                  ${IMAGE_NAME}
                """
            }
        }

        stage("Health Check") {
            steps {
                echo "❤️ Running health check"
                sh """
                sleep 5
                curl --fail http://localhost:${APP_PORT}
                """
            }
        }
    }

    post {
        success {
            echo "✅ Jenkins Pipeline SUCCESS – App running on port ${APP_PORT}"
        }
        failure {
            echo "❌ Jenkins Pipeline FAILED"
        }
        always {
            echo "📦 Pipeline execution completed"
        }
    }
}
