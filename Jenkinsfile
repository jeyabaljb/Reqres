pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['qa', 'uat'],
            description: 'Choose the environment to run tests against'
        )
    }

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install --upgrade pip
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests with environment config') {
            steps {
                script {
                    def envFileId = params.ENVIRONMENT == 'uat' ? 'uat-env-file' : 'qa-env-file'

                    withCredentials([file(credentialsId: envFileId, variable: 'ENV_FILE')]) {
                        sh '''
                            echo "Using environment: ${ENVIRONMENT}"
                            echo "Sourcing $ENV_FILE"

                            # Source env vars from the secret .env file
                            set -a
                            source "$ENV_FILE"
                            set +a

                            echo "Running in environment: $ENV"
                            venv/bin/python -m pytest
                        '''
                    }
                }
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
        }
    }
}
