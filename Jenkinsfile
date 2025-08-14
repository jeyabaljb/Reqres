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
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                echo 'Running tests with pytest and generating HTML report'
                sh '''
                   source venv/bin/activate
            pytest --html=report.html
                '''
            }
        }
    }


    post {
    always {
        echo 'Pipeline completed.'
        archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
        publishHTML(target: [
            reportName: 'Test Report',
            reportDir: '.',
            reportFiles: 'report.html',
            keepAll: true,
            alwaysLinkToLastBuild: true
        ])
    }
    failure {
        echo 'Build failed.'
    }
    success {
        echo 'Build succeeded.'
    }
}
}
