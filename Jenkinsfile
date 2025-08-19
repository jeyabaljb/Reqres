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
                        sh """
                            set -ex

                            echo "Using environment: ${params.ENVIRONMENT}"
                            echo "Loading env file: \$ENV_FILE"

                            if [ ! -f "\$ENV_FILE" ]; then
                                echo "ERROR: Environment file not found!"
                                exit 1
                            fi

                            set -a
                            . "\$ENV_FILE"
                            set +a

                            echo "BASE_URL is: \$BASE_URL"

                            mkdir -p reports
                            venv/bin/python -m pytest
                        """
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

        failure {
            echo 'Build failed! Sending email...'
            mail to: 'bimo.mohan@gmail.com',
                 subject: "Jenkins Job Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: """\
Hi Team,

The Jenkins job '${env.JOB_NAME}' has failed at build #${env.BUILD_NUMBER}.

Check console output here: ${env.BUILD_URL}

Regards,
Jenkins
"""
        }

        success {
            echo 'Build passed. Sending success email...'
            mail to: 'bimo.mohan@gmail.com',
                 subject: "Jenkins Job Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: """\
Hi Team,

The Jenkins job '${env.JOB_NAME}' completed successfully at build #${env.BUILD_NUMBER}.

You can view the report here: ${env.BUILD_URL}Test_20Report/

Regards,
Jenkins
"""
        }
    }
}
