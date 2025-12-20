pipeline {
    agent any

    environment {
        IMAGE_NAME = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-app-container"
        PORT = "5002"
        DATA_DIR = "data"
        DB_FILE = "users.db"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo "📦 Checking out source code"
                checkout scm
            }
        }

        stage('Verify Docker Running') {
            steps {
                echo "🐳 Verifying Docker daemon"
                bat "docker info"
            }
        }

        stage('Prepare Data Folder') {
            steps {
                echo "🗂 Ensuring data folder exists"
                bat """
                if not exist ${DATA_DIR} mkdir ${DATA_DIR}
                if not exist ${DATA_DIR}\\${DB_FILE} type nul 1> ${DATA_DIR}\\${DB_FILE}
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image"
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Remove Old Container (SAFE)') {
            steps {
                echo "🧹 Removing old container if exists"
                bat """
                docker ps -a -q -f name=${CONTAINER_NAME} > temp.txt
                set /p CID= < temp.txt
                if NOT "%CID%" == "" docker rm -f ${CONTAINER_NAME}
                del temp.txt
                """
            }
        }

        stage('Run New Container') {
            steps {
                echo "🚀 Running new container on port ${PORT}"
                bat """
                docker run -d ^
                    --name ${CONTAINER_NAME} ^
                    -p ${PORT}:${PORT} ^
                    -v %CD%\\${DATA_DIR}:/app/data ^
                    ${IMAGE_NAME}
                """
            }
        }

        stage('Health Check') {
            steps {
                echo "❤️ Waiting for app to start"
                // Windows-safe wait
                bat "ping 127.0.0.1 -n 6 > nul"
            }
        }
    }

    post {
        failure {
            echo "❌ PIPELINE FAILED — Check Docker Desktop & logs"
        }
    }
}
