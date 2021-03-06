# -*- coding: utf-8 -*-
import logging
from util import full_stack
from workflow.steps.util.base import BaseStep
from workflow.exceptions.error_codes import DBAAS_0021
from util import exec_remote_command_host

LOG = logging.getLogger(__name__)


class UmountDataVolume(BaseStep):

    def __unicode__(self):
        return "Umounting old data..."

    def do(self, workflow_dict):
        try:
            command = 'umount /data'
            for host_and_export in workflow_dict['hosts_and_exports']:
                host = host_and_export['host']
                LOG.info('umount data volume on host {}'.format(host))
                output = {}
                return_code = exec_remote_command_host(host, command, output)
                if return_code != 0:
                    raise Exception(str(output))

            return True
        except Exception:
            traceback = full_stack()

            workflow_dict['exceptions']['error_codes'].append(DBAAS_0021)
            workflow_dict['exceptions']['traceback'].append(traceback)

            return False

    def undo(self, workflow_dict):
        LOG.info("Running undo...")
        try:
            command = 'mount /data'
            for host_and_export in workflow_dict['hosts_and_exports']:
                host = host_and_export['host']
                LOG.info('mount data volume on host {}'.format(host))
                output = {}
                return_code = exec_remote_command_host(host, command, output)
                if return_code != 0:
                    LOG.info(str(output))

            return True
        except Exception:
            traceback = full_stack()

            workflow_dict['exceptions']['error_codes'].append(DBAAS_0021)
            workflow_dict['exceptions']['traceback'].append(traceback)

            return False
