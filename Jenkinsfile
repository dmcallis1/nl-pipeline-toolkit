pipeline { 
    agent any 
    options {
        skipStagesAfterUnstable()
        disableConcurrentBuilds()
    }
    environment {
        /*
            Change these environment variables based on your specific project
        */

        // Assumes you have defined a Jenkins environment variable 'PATH+EXTRA'
        PROJ = "/bin:/usr/local/bin:/usr/bin"

        // Name of CSV file containing network list
        NLFILE = "list.csv"

        // Name of network list to update
        NLNAME = "gss-ta-nw-list"

        // Link to VCS project containing network list
        NLSCM = "git@github.com:dmcallis1/gcs-au-demo.git"

        // Comma-seperated e-mail list
        NLEMAIL = "dmcallis@akamai.com"

        // Todo add path to executables
    }
    parameters {
        choice(name: 'NETWORK', choices: ['staging', 'production'], description: 'The network to activate the network list.')
        choice(name: 'ACTION', choices: ['append', 'overwrite'], description: 'Append to or overwrite the target list based on the supplied file contents.')
    }
    stages {
     stage('Clone NL project') {
            steps {
                git "${env.NLSCM}"

                archiveArtifacts "${env.NLFILE}"

                slackSend(botUser: true, message: "${env.JOB_NAME} - Pulling updated network list from SCM. List Name: ${env.NLNAME}", color: '#1E90FF')
            }
        }
        stage('Update Network List') {
            steps {
                step([  $class: 'CopyArtifact',
                        filter: '*.csv',
                        fingerprintArtifacts: true,
                        projectName: '${JOB_NAME}',
                        selector: [$class: 'SpecificBuildSelector', buildNumber: '${BUILD_NUMBER}']
                ])
                withEnv(["PATH+EXTRA=$PROJ"]) {
                    sh 'python3 /var/lib/jenkins/gcs-au-demo/updateNetworkList.py $NLNAME --file $NLFILE --action ${ACTION}'
                }
                slackSend(botUser: true, message: "${env.JOB_NAME} - Updating network list ${env.NLNAME}", color: '#1E90FF')
            }
        }
        stage('Activate Network List'){
            steps {
                slackSend(botUser: true, message: "${env.JOB_NAME} - Activating network list on ${env.NETWORK}", color: '#1E90FF')
                withEnv(["PATH+EXTRA=$PROJ"]) {
                    sh 'python3 /var/lib/jenkins/gcs-au-demo/activateNetworkList.py $NLNAME --network ${NETWORK} --email $NLEMAIL'
                }
                slackSend(botUser: true, message: "${env.JOB_NAME} - Network list activated!", color: '#1E90FF')
            }
        }
    }
    post {
        success {
            slackSend(botUser: true, message: "${env.JOB_NAME} - Network List updated successfully.", color: '#008000')
        }
        failure {
            slackSend(botUser: true, message: "${env.JOB_NAME} - Network List update failed!", color: '#FF0000')
        }
    }
}