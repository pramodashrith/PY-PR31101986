pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                script {
                    // Clone the repository to a specific path
                    checkout([$class: 'GitSCM', 
                              branches: [[name: 'test']],
                              doGenerateSubmoduleConfigurations: false, 
                              extensions: [], 
                              submoduleCfg: [], 
                              userRemoteConfigs: [[url: 'https://github.com/pramodashrith/PY-PR31101986.git']]])
                }
            }
        }
        stage()
    }
}
