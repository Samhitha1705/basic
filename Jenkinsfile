pipeline {
    agent any

    environment {
        IMAGE_NAME = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-container-new" // no v2, just new
        HOST_PORT = "5002"
        CONTAINER_PORT = "5000"
    }

    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'github-fine-grained-pat',
                        url: 'https://github.com/Samhitha1705/basic.git'
                    ]]
                ])
            }
        }

        stage('Checkout Code') {
            steps {
                echo '📌 Checking out source code'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🚀 Building Docker image'
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Stop & Remove Old Container (new only)') {
            steps {
                echo '🧹 Cleaning old container if exists'
                bat "docker stop ${CONTAINER_NAME} || echo Not running"
                bat "docker rm ${CONTAINER_NAME} || echo Not present"
            }
        }

        stage('Run New Container') {
            steps {
                echo '🏃 Running new container'
                bat "docker run -d -p ${HOST_PORT}:${CONTAINER_PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}"
            }
        }

        stage('Health Check') {
            steps {
                echo '💡 Checking container health'
                bat "docker ps -a | findstr ${CONTAINER_NAME}"
            }
        }
    }

    post {
        success {
            echo '✅ Jenkins Pipeline completed successfully'
        }
        failure {
            echo '❌ Jenkins Pipeline FAILED'
        }
    }
}
