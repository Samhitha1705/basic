pipeline {
    agent any

    environment {
        IMAGE_NAME     = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-container"
        APP_PORT       = "5002"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "📥 Checking out source code"
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image"
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Stop & Remove Old Container (same name only)') {
            steps {
                echo "🛑 Cleaning old container if exists"
                bat """
                docker stop %CONTAINER_NAME% || echo Not running
                docker rm %CONTAINER_NAME% || echo Not present
                """
            }
        }

        stage('Run New Container') {
            steps {
                echo "🚀 Running container on port 5002"
                bat """
                docker run -d ^
                --name %CONTAINER_NAME% ^
                -p %APP_PORT%:%APP_PORT% ^
                %IMAGE_NAME%
                """
            }
        }

        stage('Health Check') {
            steps {
                echo "❤️ Verifying running containers"
                bat "docker ps"
            }
        }
    }

    post {
        success {
            echo "✅ Jenkins Pipeline SUCCESSFUL"
        }
        failure {
            echo "❌ Jenkins Pipeline FAILED"
        }
        always {
            echo "📦 Pipeline execution completed"
        }
    }
}
