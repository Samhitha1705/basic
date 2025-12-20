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
                echo "📦 Checking out source code"
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
                echo "🐳 Building Docker image"
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Remove Old Container (SAFE)') {
            steps {
                echo "🧹 Removing old container if exists"
                bat """
                docker rm -f %CONTAINER_NAME% || echo Container not found
                """
            }
        }

        stage('Run New Container') {
            steps {
                echo "🚀 Starting new container on port 5002"
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
                echo "🔍 Checking app health"
                sleep 5
                bat "curl http://localhost:%PORT%"
            }
        }
    }

    post {
        success {
            echo "✅ DEPLOYMENT SUCCESSFUL!"
            echo "🌐 App running at http://localhost:5002"
        }
        failure {
            echo "❌ PIPELINE FAILED"
        }
    }
}
