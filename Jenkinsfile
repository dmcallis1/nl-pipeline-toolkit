pipeline { 
    agent any 
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Update Network List') {
            steps { 
                sh 'python3 /var/lib/jenkins/gss-au-python/updateNetworkList.py gss-ta-nw-list --file list.csv'
            }
        }
        stage('Activate Network List'){
            steps {
                sh 'python3 /var/lib/jenkins/gss-au-python/activateNetworkList gss-ta-nw-list --network PRODUCTION --email dmcallis@akamai.com'
            }
        }
    }
}
