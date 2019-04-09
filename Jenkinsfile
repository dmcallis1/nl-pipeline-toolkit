pipeline { 
    agent any 
    options {
        skipStagesAfterUnstable()
    }
    stages {
     stage('Clone NL project') {
            steps {
                git 'git@github.com:dmcallis1/gcs-au-demo.git'
                archiveArtifacts 'list.csv'
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: 'Pulling updated network list from SCM', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
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
                sh 'python3 /var/lib/jenkins/gcs-au-demo/updateNetworkList.py gss-ta-nw-list --file list.csv'
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: 'Updating network list', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
            }
        }
        stage('Activate Network List'){
            steps {
                sh 'python3 /var/lib/jenkins/gcs-au-demo/activateNetworkList gss-ta-nw-list --network PRODUCTION --email dmcallis@akamai.com'
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: 'Activating network list', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
            }
        }
    }
}