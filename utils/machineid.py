#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Simple class to read machine ID of SBC
"""

import logging

logging.basicConfig(level=logging.INFO)
class_logger = logging.getLogger('MachineId')

class MachineId(object):

    '''
    A class to pull a remote config file from a http site
    '''

    def __init__(self, machine_id_file = '/etc/machine-id'):

        self.err_msg = ''
        self.machine_id_file = '/etc/machine-id'
        self.machine_id = ''
    
   
    def read_machine_id(self):
        """
        Read data from machineid file
        """

        class_logger.debug("Reading machine id from local file...")
        try:   
            with open(self.machine_id_file, 'r') as f:
                self.machine_id = f.readline().strip()
            class_logger.debug("Data read OK.")
            return self.machine_id
        except Exception as ex:
            self.err_msg = "Issue reading machine_id file: {}".format(ex)
            class_logger.error(self.err_msg)
            return False

