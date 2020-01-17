import logging
import sys
import time
from flask import abort
from googleapiclient import discovery

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

DEFAULT_PROJECT = 'vino9org'
DEFAULT_ZONE = 'us-west1-b'
compute = discovery.build('compute', 'v1', cache_discovery=False)


def vm_action(request):
    if request.method != 'GET':
        return abort(405)

    token = request.args.get('token')
    if token == None:
        return abort(405)

    action = request.args.get('action')
    if action == None or action not in ['start', 'stop']:
        return 'invalid action'

    logging.info(f'action={action}, token={token}')
    return handle_vm(action, token)


def handle_vm(action, token):
    message = ''
    for vm in get_vms_by_token(token):
        name, status = vm['name'], vm['status']
        logging.info(f"vm {name} is {status}, action ={action}")

        if action == 'stop' and status == 'RUNNING':
            message += f'stopping {name}\n'
            stop_gce_vm(name)
        elif action == 'start' and status == 'TERMINATED':
            message += f'starting {name}\n'
            start_gce_vm(name)

    if message == '':
        message = 'nothing to do'

    return message


def get_vms_by_token(token, project=DEFAULT_PROJECT, zone=DEFAULT_ZONE):
    result = compute.instances().list(
        project=project,
        zone=zone,
        filter=f'labels.token={token}').execute()
    return result['items'] if 'items' in result else {}


def start_gce_vm(name, project=DEFAULT_PROJECT, zone=DEFAULT_ZONE):
    logging.info('starting {name}')
    compute.instances().start(
        project=project,
        zone=zone,
        instance=name).execute()


def stop_gce_vm(name, project=DEFAULT_PROJECT, zone=DEFAULT_ZONE):
    logging.info('stopping {name}')
    compute.instances().stop(
        project=project,
        zone=zone,
        instance=name).execute()


if __name__ == '__main__':
    print(handle_vm(token='1111', action='stop'))
