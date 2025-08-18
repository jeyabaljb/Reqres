pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python environment') {
            steps {
                echo 'Creating virtual environment and installing dependencies'
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install --upgrade pip
                    venv/bin/pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                echo 'Running tests with pytest'
                sh '''
                    venv/bin/python -m pytest
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true

            publishHTML(target: [
                reportName: 'Test Report',
                reportDir: 'reports',
                reportFiles: 'report.html',
                keepAll: true,
                alwaysLinkToLastBuild: true
            ])

            echo 'Pipeline completed.'
        }
        failure {
            echo 'Build failed.'
        }
        success {
            echo 'Build succeeded.'
        }
    }
}
