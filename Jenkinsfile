pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Pull code from your GitHub repo
                git branch: 'main',
                    url: 'https://github.com/jeyabaljb/Reqres.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
                // Change this command if your project is not Maven-based
                sh 'pytest'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'pytest'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                // Add your deployment commands here if needed
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
