pipeline {
    agent any

    environment {
        IMAGE_NAME = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-app-container"
        PORT = "5002"
        HOST_DATA_DIR = "C:/Users/1016/jenkins-data"  // safe folder outside OneDrive
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
                echo "🛠 Verifying Docker daemon"
                bat 'docker info'
            }
        }

        stage('Prepare Data Folder') {
            steps {
                echo "📂 Ensuring data folder exists"
                bat """
                if not exist "${HOST_DATA_DIR}" mkdir "${HOST_DATA_DIR}"
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
                    -v "${HOST_DATA_DIR}:/app/data" ^
                    ${IMAGE_NAME}
                """
            }
        }

        stage('Verify DB Creation') {
            steps {
                echo "🔍 Checking if users.db is created in ${HOST_DATA_DIR}"
                bat """
                if exist "${HOST_DATA_DIR}\\users.db" (
                    echo ✅ users.db exists
                ) else (
                    echo ❌ users.db NOT found
                )
                """
            }
        }
    }

    post {
        failure {
            echo "❌ PIPELINE FAILED — Check Docker Desktop & logs"
        }
        success {
            echo "🎉 PIPELINE SUCCESSFUL — users.db is now in ${HOST_DATA_DIR}"
        }
    }
}
