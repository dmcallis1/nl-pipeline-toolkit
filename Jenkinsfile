pipeline { 
    agent any 
    options {
        skipStagesAfterUnstable()
    }
    stages {
     stage('Clone NL project') {
            steps {
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: 'Pulling updated network list from SCM', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
                git 'git@github.com:dmcallis1/gcs-au-demo.git'
                archiveArtifacts 'list.csv'
            }
        }
        stage('Update Network List') {
            steps {
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: 'Updating network list', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
                copyArtifacts filter: 'list.csv', fingerprintArtifacts: true, projectName: 'Clone project', selector: lastSuccessful(), target: '.'
                sh 'python3 /var/lib/jenkins/gcs-au-demo/updateNetworkList.py gss-ta-nw-list --file list.csv'
            }
        }
        stage('Activate Network List'){
            steps {
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: 'Activating network list', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
                sh 'python3 /var/lib/jenkins/gcs-au-demo/activateNetworkList gss-ta-nw-list --network PRODUCTION --email dmcallis@akamai.com'
            }
        }
    }
}