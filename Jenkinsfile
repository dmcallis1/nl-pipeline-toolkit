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

        // Todo add path to executables
    }
    parameters {
        choice(name: 'NETWORK', choices: ['staging', 'production'], description: 'The network to activate the network list.')
    }
    stages {
     stage('Clone NL project') {
            steps {
                // git 'git@github.com:dmcallis1/gcs-au-demo.git'
                git "${env.NLSCM}"

                // archiveArtifacts 'list.csv'
                archiveArtifacts "${env.NLFILE}"

                // slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Pulling updated network list from SCM", color: '#1E90FF', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
                slackSend(botUser: true, message: "${env.JOB_NAME} - Pulling updated network list from SCM", color: '#1E90FF')
            }
        }
        stage('Update Network List') {
            steps {
                step([  $class: 'CopyArtifact',
                        filter: 'list.csv',
                        fingerprintArtifacts: true,
                        projectName: '${JOB_NAME}',
                        selector: [$class: 'SpecificBuildSelector', buildNumber: '${BUILD_NUMBER}']
                ])
                withEnv(["PATH+EXTRA=$PROJ"]) {
                    sh 'python3 /var/lib/jenkins/gcs-au-demo/updateNetworkList.py gss-ta-nw-list --file list.csv --action overwrite'
                }
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Updating network list ${env.NLNAME}", color: '#1E90FF', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
            }
        }
        stage('Activate Network List'){
            steps {
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Activating network list on ${env.NETWORK}", color: '#1E90FF', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
                withEnv(["PATH+EXTRA=$PROJ"]) {
                    sh 'python3 /var/lib/jenkins/gcs-au-demo/activateNetworkList.py gss-ta-nw-list --network ${NETWORK} --email dmcallis@akamai.com'
                }
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Network list activated!", color: '#1E90FF', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
            }
        }
    }
    post {
        success {
            slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Network List updated successfully.", color: '#008000', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
        }
        failure {
            slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Network List update failed!", color: '#FF0000', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
        }
    }
}