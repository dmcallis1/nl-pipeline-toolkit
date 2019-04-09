import logging
import argparse
import os
import sys
import requests
from time import sleep
from akamai.edgegrid import EdgeGridAuth, EdgeRc


# Setup logging
logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# Argparse will help manage command line arguments
parser = argparse.ArgumentParser(description='Network List Activator',
                                 epilog='Built for Akamai GSS Technical Enablement - 2019',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# Let's add a positional argument
parser.add_argument('name', metavar='list-name', type=str, help='The name of our network list.')
parser.add_argument('--network', action="store", required=True, default='staging', help="Activation network: production or staging")
parser.add_argument('--email', action="store", required=True, help="Comma delimited e-mail list, for activation e-mail notifications.")
parser.add_argument('--comment', action="store", default="None.", help="Activation comments.")

# Let's add edgerc options for flexibility
parser.add_argument('--config', action="store", default=os.environ['HOME'] + "/.edgerc", help="Full or relative path to .edgerc file")
parser.add_argument('--section', action="store", default="default", help="The section of the edgerc file with the proper {OPEN} API credentials.")
args = parser.parse_args()

log.info('Activating network list \'' + args.name + '\' on ' + args.network.upper() + ' network.')

try:
    edgerc = EdgeRc(args.config)
    baseurl = 'https://%s' % edgerc.get(args.section, 'host')
    session = requests.Session()
    session.auth = EdgeGridAuth.from_edgerc(edgerc, args.section)
    log.debug('API Base URL: ' + baseurl)

except Exception as e:
    log.error('Error authenticating Akamai {OPEN} API client.')
    log.error(e)

# Find our list, using the 'name' argument and obtain the Network List ID
endpoint = baseurl + '/network-list/v2/network-lists?search=' + args.name
result = session.get(endpoint).json()

# Check that the list exists, and there is no ambiguity (more than 1 list)
if len(result['networkLists']) != 1:
    log.error('Network list \'' + args.name + '\' not found. Exiting.')
    sys.exit(1)

# Initialize the listID as a variable
listId = result['networkLists'][0]['uniqueId']

def checkStatus(listId, network):
    endpoint = baseurl + '/network-list/v2/network-lists/' + listId + '/environments/' + network.upper() + '/status'
    result = session.get(endpoint).json()

    return result

result = checkStatus(listId, args.network)
if result['activationStatus'] == 'ACTIVE':
    log.error('Network List \'' + args.name + '\' is already active. Exiting.')
    print(result)
    sys.exit(1)

log.info('Creating activation payload.')
emailList = args.email.split(",")
endpoint = baseurl + '/network-list/v2/network-lists/' + listId + '/environments/' + args.network.upper() + '/activate'
payload = { "comments": args.comment, "notificationRecipients": emailList}
result = session.post(endpoint, json=payload, headers={'Content-Type': 'application/json'}).json()

if not result['activationId']:
    log.error('Error requesting activation. Exiting.')
    sys.exit(1)

log.info('Activation request on network: ' + args.network + ' complete. Activation Id: ' + str(result['activationId']))
result = checkStatus(listId, args.network)

while result['activationStatus'] != 'ACTIVE':
    log.info('Activation status on ' + args.network.upper() + ': ' + result['activationStatus'])
    result = checkStatus(listId, args.network)
    sleep(10)

log.info('Activation complete in network: ' + args.network + '. Status: ' + result['activationStatus'])