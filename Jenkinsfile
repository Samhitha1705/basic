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

        stage('Stop Container Using Port 5002 (SAFE)') {
            steps {
                echo '🛑 Stopping any container using port 5002'
                bat '''
                FOR /F %%C IN ('docker ps -q --filter "publish=5002"') DO (
                    docker stop %%C
                )
                '''
            }
        }

        stage('Remove Old Container (SAFE)') {
            steps {
                echo '🧹 Removing old container if exists'
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
                echo '🔍 Health check'
                bat '''
                timeout /t 5
                curl http://localhost:5002 || exit 1
                '''
            }
        }
    }

    post {
        success {
            echo '✅ PIPELINE SUCCESS — App running on http://localhost:5002'
        }
        failure {
            echo '❌ PIPELINE FAILED — Check logs'
        }
    }
}
