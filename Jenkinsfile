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
                echo "📂 Checking out source code from Git"
                checkout([$class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    userRemoteConfigs: [[
                        url: 'https://github.com/Samhitha1705/basic.git', 
                        credentialsId: 'github-fine-grained-pat'
                    ]]
                ])
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
                script {
                    echo "🛑 Stopping old container if exists..."
                    try {
                        bat "docker rm -f ${CONTAINER_NAME}"
                        echo "Old container removed successfully."
                    } catch (err) {
                        echo "No old container to remove. Continuing..."
                    }
                }
            }
        }

        stage('Ensure Port is Free') {
            steps {
                script {
                    def portInUse = bat(script: "netstat -ano | findstr :${HOST_PORT}", returnStatus: true)
                    if (portInUse == 0) {
                        echo "⚠️ Host port ${HOST_PORT} is in use. Attempting to free it..."
                        // Stop any container that might be using this port
                        bat """
                        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :${HOST_PORT} ^| findstr LISTENING') do (
                            docker stop %%a
                        )
                        """
                    } else {
                        echo "Port ${HOST_PORT} is free."
                    }
                }
            }
        }

        stage('Run New Container') {
            steps {
                echo "▶️ Running new container on port ${HOST_PORT}:${CONTAINER_PORT}..."
                bat "docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE_NAME}"
            }
        }

        stage('Health Check') {
            steps {
                script {
                    echo "🔍 Checking if Flask app is running..."
                    sleep 5 // wait for the container to start
                    def status = bat(script: "curl -s -o nul -w \"%{http_code}\" http://localhost:${HOST_PORT}/", returnStdout: true).trim()
                    if (status == "200") {
                        echo "✅ Flask app is running on port ${HOST_PORT}"
                    } else {
                        error "❌ Flask app failed to start! HTTP status: ${status}"
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "❌ Pipeline failed. Check the logs above."
        }
        success {
            echo "🎉 Pipeline completed successfully!"
        }
    }
}
