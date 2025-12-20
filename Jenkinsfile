pipeline {
    agent any

    environment {
        IMAGE_NAME = "login-sqlite-app"      // Updated image name
        CONTAINER_NAME = "login-sqlite-container" // Updated container name
        APP_PORT = "5002"                     // Your Flask app port
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Checkout Code') {
            steps {
                echo "📡 Checking out source code"
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🛠 Building Docker image"
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Stop & Remove Old Container (same name only)') {
            steps {
                echo "🧹 Cleaning old container if exists"
                bat "docker stop %CONTAINER_NAME% || echo Not running"
                bat "docker rm %CONTAINER_NAME% || echo Not present"
            }
        }

        stage('Run New Container') {
            steps {
                echo "🚀 Running container on port %APP_PORT%"
                // Single-line run command is safest on Windows Jenkins
                bat "docker run -d --name %CONTAINER_NAME% -p %APP_PORT%:%APP_PORT% %IMAGE_NAME%"
            }
        }

        stage('Health Check') {
            steps {
                echo "🔍 Checking container status"
                bat "docker ps -a | findstr %CONTAINER_NAME%"
            }
        }
    }

    post {
        success {
            echo "✅ Jenkins Pipeline completed successfully!"
        }
        failure {
            echo "❌ Jenkins Pipeline FAILED"
        }
    }
}
