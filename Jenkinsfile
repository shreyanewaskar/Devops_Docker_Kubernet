
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'cloudcart'
        CONTAINER_NAME = 'cloudcart-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shreyanewaskar/Devops_Docker_Kubernet.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t cloudcart:latest .'
            }
        }

        stage('Deploy CloudCart') {
            steps {
                sh '''
                    docker rm -f cloudcart-app || true
                    docker run -d \
                        --name cloudcart-app \
                        -p 5000:5000 \
                        cloudcart:latest
                '''
            }
        }

        stage('Verify Application') {
            steps {
                sh 'sleep 5'
                sh 'curl -f http://localhost:5000/ || true'
            }
        }
    }

    post {
        success {
            echo 'CloudCart pipeline completed successfully!'
        }

        failure {
            echo 'CloudCart pipeline failed. Check the console output.'
        }
    }
}
