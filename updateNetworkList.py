'''

    Step 1: Get the existing Network List from Akamai (list ID and contents).
    Step 2: Read our input list and validate its contents.
    Step 3: Modify the Network list (either append or overwrite)

'''

import logging
import argparse
import os
import sys
import re
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc

# Setup logging
logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# Argparse will help manage command line arguments
parser = argparse.ArgumentParser(description='Network List Updater',
                                 epilog='Built for Akamai GSS Technical Enablement - 2019',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# Let's add a positional argument
parser.add_argument('name', metavar='list-name', type=str, help='The name of our network list.')

# Let's add optional arguments
parser.add_argument('--file', action="store", default=os.getcwd() + "/list.csv", help="Path to CSV file with IPs for our network list.")
parser.add_argument('--delimiter', action="store", default=',', help="CSV delimiter used, if not \',\'")
parser.add_argument('--action', action="store", default='append', help="The action to take on the network list. Supported options are: append or overwrite.'")


# Let's add edgerc options for flexibility
parser.add_argument('--config', action="store", default=os.environ['HOME'] + "/.edgerc", help="Full or relative path to .edgerc file")
parser.add_argument('--section', action="store", default="default", help="The section of the edgerc file with the proper {OPEN} API credentials.")
args = parser.parse_args()

log.info('Updating network list \'' + args.name + '\'. Action: ' + args.action)

# Edgegrid auth
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

# Get the list details
endpoint = baseurl + '/network-list/v2/network-lists/' + listId
result = session.get(endpoint).json()

# Ensure that the file exists
if not os.path.isfile(args.file):
    log.error('No input file was found or provided. Exiting.')
    parser.print_help()
    sys.exit(1)

# Open the file
try:
    with open(args.file, 'r') as csvfile:
        # Read in file contents as a list
        ips = csvfile.read().split(args.delimiter)
except Exception as e:
    log.error('Error encountered opening CSV file: ' + args.file)
    log.error(e)

log.info('Reading input file: ' + args.file + '. Size (bytes): ' + str(os.stat(args.file).st_size))

# We'll use this list to hold our IPs
sanitizedIps = []

# Let's check the contents of the file
for ip in ips:
    # Use regex to test that all lines are IPs
    if not re.match(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.(\d{1,3}|\d{1}\/\d{1,2})\b', ip):
        # The item was not an IP, discard it.
        pass
    else:
        # The item was an IP, add it to the list.
        sanitizedIps.append(ip.rstrip('\n'))

log.info('Found ' + str(len(sanitizedIps)) + ' IP addresses in the list. Network List \'' + args.name + '\' previously had ' + str(result['elementCount']) + ' items.')

# Let's generate our payload using python Dict operations
log.info('Generating JSON payload for Network Lists API...')
result['list'] = sanitizedIps


log.info('Updating network list: ' + args.name)
endpoint = baseurl + '/network-list/v2/network-lists/' + listId

# Update the list based on the supplied action (overwrite or append)
if args.action == 'append':
    endpoint = endpoint  + '/append'
    # Append requires simplified payload
    result = {"list": sanitizedIps}
    # Append requires POST method
    method = 'POST'
else:
    # Overwrite (update) requires PUT method
    method = 'PUT'


result = session.request(method, endpoint, json=result, headers={'Content-Type': 'application/json'})
log.info('Update complete. Status Code: ' + str(result.status_code))