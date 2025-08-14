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
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                echo 'Running tests with pytest'
                sh '''
                    source venv/bin/activate
                    pytest
                '''
            }
        }
    }

    post {
        always {
            // Archive all HTML reports inside the reports directory
            archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true

            // Publish HTML reports from the reports directory
            publishHTML(target: [
                reportName: 'Test Report',
                reportDir: 'reports',
                reportFiles: '*.html',
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
