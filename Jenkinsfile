pipeline { 
    agent any 
    options {
        skipStagesAfterUnstable()
        disableConcurrentBuilds()
    }
    environment {
        PROJ = "/bin:/usr/local/bin:/usr/bin"
    }
    parameters {
        choice(name: 'NETWORK', choices: ['staging', 'production'], description: 'The network to activate the network list.')
    }
    stages {
     stage('Clone NL project') {
            steps {
                git 'git@github.com:dmcallis1/gcs-au-demo.git'
                archiveArtifacts 'list.csv'
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Pulling updated network list from SCM", color: '#1E90FF', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
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
                    sh 'python3 /var/lib/jenkins/gcs-au-demo/updateNetworkList.py gss-ta-nw-list --file list.csv'
                }
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Updating network list", color: '#1E90FF', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
            }
        }
        stage('Activate Network List'){
            steps {
                def startDate = new Date().parse('dd/MM/yyyy HH:mm:ss',f.text)

                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Activating network list on ${env.NETWORK}", color: '#1E90FF', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
                withEnv(["PATH+EXTRA=$PROJ"]) {
                    sh 'python3 /var/lib/jenkins/gcs-au-demo/activateNetworkList.py gss-ta-nw-list --network ${NETWORK} --email dmcallis@akamai.com'
                }
                def endDate = new Date()
                def tookTime = groovy.time.TimeCategory.minus(endDate,startDate).toString()
                slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Network list activated! Time: ${tookTime}", color: '#1E90FF', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
            }
        }
    }
    post {
        success {
            slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Network List updated successfully.", color: '#008000', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
        }
        failure {
            slackSend baseUrl: 'https://akamaiwebteam.slack.com/services/hooks/jenkins-ci/', botUser: true, channel: 'gcs-chatops', message: "${env.JOB_NAME} - Network List updated successfully.", color: '#FF0000', teamDomain: 'akamaiwebteam', token: 'A9dlq96QplhZuTnuNhXIDmx6'
        }
    }
}