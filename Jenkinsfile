pipeline { 
    agent any 
    options {
        skipStagesAfterUnstable()
    }
    stages {
     stage('Clone project') {
            steps {
                git 'git@github.com:dmcallis1/gcs-au-demo.git'
                archiveArtifacts 'list.csv'
            }
        }
        stage('Update Network List') {
            steps {
                copyArtifacts filter: 'list.csv', fingerprintArtifacts: true, projectName: 'Update Network List', selector: lastSuccessful(), target: '.'
                sh 'python3 /var/lib/jenkins/gcs-au-demo/updateNetworkList.py gss-ta-nw-list --file list.csv'
            }
        }
        stage('Activate Network List'){
            steps {
                sh 'python3 /var/lib/jenkins/gcs-au-demo/activateNetworkList gss-ta-nw-list --network PRODUCTION --email dmcallis@akamai.com'
            }
        }
    }
}