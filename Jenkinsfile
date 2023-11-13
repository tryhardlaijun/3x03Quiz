pipeline {
    agent none
    stages {
        stage('Build Docker Image') {
            agent any // This specifies that Jenkins can use any available agent.
            steps {
                script {
                    // This builds a Docker image using the Dockerfile in the current directory
                    // and tags it as 'my-python-app'.
                    docker.build("my-python-app")
                }
            }
        }

		stage('OWASP DependencyCheck') {
            agent any
            steps {
            dependencyCheck additionalArguments: ''' 
                    --enableExperimental
                    -o './'
                    -s './'
                    -f 'ALL'
                    --prettyPrint''', odcInstallation: 'Default'
            dependencyCheckPublisher pattern: 'dependency-check-report-*.xml'
        
                }
        }

        stage('Unit Test') {
            agent {
                docker {
                    image 'my-python-app' // This specifies to use the image built in the previous stage.
                }
            }
            steps {
                sh 'python -m unittest app_test.py'
            }
        }
        

        stage('Run Tests') {
        parallel {
                stage('Deploy') {
                    agent any
                    steps {
                        sh './deploy.sh'
						input message: 'Finished using the web site? (Click "Proceed" to continue)'
						sh './kill.sh'    }
                }
                stage('Selenium Tests') {
                    agent {
                        docker {
                            image 'infologistix/docker-selenium-python' // or another image with Selenium and required browsers/drivers
                            args '-v .:/tests --network host' // Mount the tests directory
                        }
                    }
                    steps {
                        sh 'python selenium_test.py' // Run the Selenium tests
                    }
                }
            }
        }

        stage('Code Quality Check via SonarQube') {
            agent any
            steps {
                script {
                    def scannerHome = tool 'SonarQube'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=test -Dsonar.sources=."
                    }
                }
            }
        }

        stage('Post Actions') {
            agent any // Specify an agent for post actions
            steps {
                script {
                    recordIssues enabledForFailure: true, tool: sonarQube()
                    dependencyCheckPublisher pattern: 'dependency-check-report.xml'
                }
            }
        }
    }
}

