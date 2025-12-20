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
                echo "📦 Checking out source code from Git"
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
                echo "🛑 Stopping old container if exists"
                script {
                    bat "docker rm -f ${CONTAINER_NAME} || echo 'No container to remove'"
                }
            }
        }

        stage('Run New Container') {
            steps {
                echo "▶️ Running new container"
                script {
                    // Check if host port is free
                    def portCheck = bat(script: "netstat -ano | findstr :${HOST_PORT}", returnStatus: true)
                    if (portCheck == 0) {
                        echo "⚠️ Host port ${HOST_PORT} is in use. Choose a different port!"
                        error("Port ${HOST_PORT} already in use")
                    } else {
                        bat "docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE_NAME}"
                    }
                }
            }
        }

        stage('Health Check') {
            steps {
                echo "🔍 Performing health check"
                // Simple curl check for Flask app
                script {
                    def status = bat(script: "curl http://localhost:${HOST_PORT}/ -I", returnStatus: true)
                    if (status != 0) {
                        error("Health check failed!")
                    } else {
                        echo "✅ Application is up and running"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "🎉 Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs above!"
        }
    }
}
