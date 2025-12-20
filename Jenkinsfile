pipeline {
    agent any

    environment {
        IMAGE_NAME = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-container"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo "🔍 Checking out source code from Git"
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Samhitha1705/basic.git',
                        credentialsId: 'github-fine-grained-pat'
                    ]]
                ])
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
                echo "🧹 Cleaning old container if exists"
                script {
                    def stopStatus = bat(script: "docker stop ${CONTAINER_NAME}", returnStatus: true)
                    if (stopStatus != 0) echo "Container not running, continuing..."

                    def rmStatus = bat(script: "docker rm ${CONTAINER_NAME}", returnStatus: true)
                    if (rmStatus != 0) echo "Container not present, continuing..."
                }
            }
        }

        stage('Run New Container') {
            steps {
                echo "🏃 Running new container"
                bat """
                    docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}
                """
            }
        }

        stage('Health Check') {
            steps {
                echo "✅ Checking container health"
                // Simple check: docker ps to see if container is running
                bat "docker ps | findstr ${CONTAINER_NAME}"
            }
        }
    }

    post {
        success {
            echo "🎉 Jenkins Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline FAILED!"
        }
    }
}
