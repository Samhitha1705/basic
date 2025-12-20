pipeline {
    agent any

    environment {
        IMAGE_NAME     = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-app-container"
        PORT           = "5002"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo '📦 Checking out source code'
                checkout scm
            }
        }

        stage('Verify Docker Running') {
            steps {
                echo '🐳 Verifying Docker daemon'
                bat 'docker info'
            }
        }

        stage('Prepare Data Folder') {
            steps {
                echo '🗂 Ensuring data folder exists'
                bat '''
                if not exist data mkdir data
                if not exist data\\users.db echo Creating empty users.db
                type nul > data\\users.db
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image'
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Remove Old Container (SAFE)') {
            steps {
                echo '🧹 Removing old container if exists'
                bat '''
                docker ps -a -q -f name=%CONTAINER_NAME% > temp.txt
                set /p CID=<temp.txt
                if NOT "%CID%"=="" docker rm -f %CONTAINER_NAME%
                del temp.txt
                '''
            }
        }

        stage('Run New Container') {
            steps {
                echo '🚀 Running new container on port %PORT%'
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
                echo '❤️ Waiting for app'
                bat 'timeout /t 5'
            }
        }
    }

    post {
        success {
            echo '✅ DEPLOYMENT SUCCESSFUL'
            echo '🌐 App running at: http://localhost:%PORT%'
        }
        failure {
            echo '❌ PIPELINE FAILED — Check Docker Desktop & logs'
        }
    }
}
