
# Akamai Network List Pipeline Toolkit

This project is used for Akamai Network List management automation, using the [Akamai Network List API V2](https://developer.akamai.com/api/cloud_security/network_lists/v2.html)


The scripts and Jenkinsfile contained in this project perform the following functions within a simple CI process:

1. Update existing Network List from source CSV file
2. Activate the Network List on either production or staging networks



## Installation

All package dependencies are maintained in the requirements.txt file. Use pip to install:

```
pip install -r requirements.txt
```

## Runtime Environment

Each script was developed and tested using a python 3 (3.6.2) interpeter.

It should also be noted that the scripts assume the runtime environment will be a Linux/Unix OS. Some scripts expect Linux specific directory structures.


## Python Artifacts

### updateNetworkList.py

Used to append or overwrite a network list, using a source CSV file.

```
usage: updateNetworkList.py [-h] [--file FILE] [--delimiter DELIMITER]
                            [--action ACTION] [--config CONFIG]
                            [--section SECTION]
                            list-name

Network List Updater

positional arguments:
  list-name             The name of our network list.

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           Path to CSV file with IPs for our network list.
                        (default: $HOME/list.csv)
  --delimiter DELIMITER
                        CSV delimiter used, if not ',' (default: ,)
  --action ACTION       The action to take on the network list. Supported
                        options are: append or overwrite.' (default: append)
  --config CONFIG       Full or relative path to .edgerc file (default:
                        $HOME/.edgerc)
  --section SECTION     The section of the edgerc file with the proper Akamai
                        API credentials. (default: default)
```

### activateNetworkList.py

Activate the updated network list on either the production or staging network.

```
usage: activateNetworkList.py [-h] --network NETWORK --email EMAIL
                              [--comment COMMENT] [--config CONFIG]
                              [--section SECTION]
                              list-name

Network List Activator

positional arguments:
  list-name          The name of our network list.

optional arguments:
  -h, --help         show this help message and exit
  --network NETWORK  Activation network: production or staging (default:
                     staging)
  --email EMAIL      Comma delimited e-mail list, for activation e-mail
                     notifications. (default: None)
  --comment COMMENT  Activation comments. (default: None.)
  --config CONFIG    Full or relative path to .edgerc file (default:
                     $HOME/.edgerc)
  --section SECTION  The section of the edgerc file with the proper Akamai API
                     credentials. (default: default)
```

## Jenkins Pipeline

The included Jenkinsfile implements a declarative Pipeline to orchestrate the update and activation of the network list, given the source CSV file.

Assumes that the Slack Notifier plugin is installed and properly configured.

Edit the environment variables prior to executing the Pipeline build.