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
                    set -ex
                    which python3
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
                        sh '''#!/bin/bash
                            set -ex

                            echo "Using environment: ${ENVIRONMENT}"
                            echo "Loading env file: $ENV_FILE"

                            if [ ! -f "$ENV_FILE" ]; then
                                echo "ERROR: Environment file not found!"
                                exit 1
                            fi

                            set -a
                            . "$ENV_FILE"
                            set +a

                            echo "BASE_URL is: $BASE_URL"

                            mkdir -p reports

                            venv/bin/python -m pytest \
                                --metadata Environment ${ENVIRONMENT} \
                                --capture=tee-sys
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            publishHTML(target: [
                reportName: 'Test Report',
                reportDir: 'reports',
                reportFiles: 'report.html',
                keepAll: true,
                alwaysLinkToLastBuild: true
            ])

            script {
                def subject = "${currentBuild.fullDisplayName} - ${currentBuild.currentResult}"
                def body = """
                    Build URL: ${env.BUILD_URL}
                    Check the attached report or view in Jenkins.
                """

                emailext(
                    to: 'jeyabalt36@gmail.com','bimo.mohan@gmail.com',
                    subject: subject,
                    body: body
                )
            }
        }

        success {
            echo 'Build passed! Sending success email...'
            emailext(
                to: 'jeyabalt36@gmail.com',
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Good news! Build ${env.JOB_NAME} #${env.BUILD_NUMBER} passed.\nCheck details at: ${env.BUILD_URL}"
            )
        }

        failure {
            echo 'Build failed! Sending failure email...'
            emailext(
                to: 'jeyabalt36@gmail.com',
                subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Oops! Build ${env.JOB_NAME} #${env.BUILD_NUMBER} failed.\nCheck details at: ${env.BUILD_URL}"
            )
        }
    }
}
