pipeline {
    agent any

    environment {
        IMAGE_NAME = "login-sqlite-app"
        CONTAINER_NAME = "login-sqlite-container"
        HOST_DATA_DIR = "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\updated jenkins\\data"
        PORT = "5002"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo "🔄 Checking out source code from Git"
                checkout([$class: 'GitSCM', 
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
                echo "🛠 Building Docker image"
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                echo "🧹 Cleaning old container if exists"
                bat """
                    docker stop ${CONTAINER_NAME} || echo Container not running
                    docker rm ${CONTAINER_NAME} || echo Container not present
                """
            }
        }

        stage('Run New Container') {
            steps {
                echo "🚀 Running new container"
                bat """
                    docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 -v ${HOST_DATA_DIR}:/app/data ${IMAGE_NAME}
                """
            }
        }

        stage('Health Check') {
            steps {
                echo "✅ Performing health check"
                bat """
                    REM Replace below with actual health check if needed
                    docker ps | findstr ${CONTAINER_NAME}
                """
            }
        }
    }

    post {
        always {
            echo "📌 Jenkins Pipeline completed"
        }
        success {
            echo "🎉 Pipeline succeeded!"
        }
        failure {
            echo "❌ Pipeline FAILED!"
        }
    }
}
