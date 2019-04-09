
# Akamai Network List Pipeline Toolkit

This project is used for Akamai Network List management automation.

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