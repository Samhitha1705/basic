pipeline {
    agent any

    environment {
        IMAGE_NAME = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-app-container"
        PORT = "5002"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo '📦 Checking out source code'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image'
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Free Port 5002 (Windows)') {
            steps {
                echo '🧹 Freeing port 5002 if already in use'
                bat '''
                FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :5002') DO (
                    taskkill /PID %%P /F
                )
                '''
            }
        }

        stage('Remove Old Container (Safe)') {
            steps {
                echo '🧽 Removing old container if exists'
                bat "docker rm -f %CONTAINER_NAME% || echo Container not found"
            }
        }

        stage('Run New Container') {
            steps {
                echo '🚀 Starting new container on port 5002'
                bat """
                docker run -d ^
                --name %CONTAINER_NAME% ^
                -p %PORT%:%PORT% ^
                %IMAGE_NAME%
                """
            }
        }

        stage('Health Check') {
            steps {
                echo '🔍 Checking application health'
                bat '''
                timeout /t 5
                curl http://localhost:5002 || exit 1
                '''
            }
        }
    }

    post {
        success {
            echo '✅ PIPELINE SUCCESS — Application running on http://localhost:5002'
        }
        failure {
            echo '❌ PIPELINE FAILED — Check logs above'
        }
    }
}
