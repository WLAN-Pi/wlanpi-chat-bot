#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Manipulate the global config file
"""

import json
import logging

config_file = "/opt/wlanpi-chat-bot/etc/config.json"

logging.basicConfig(level=logging.INFO)
class_logger = logging.getLogger('Config')

class Config(object):

    '''
    Manipulate the global config file
    '''

    def __init__(self, config_file=config_file,):

        self.config_file = config_file
        self.config = {}

    def read_config(self):
        """
        Read data from json config file
        """

        class_logger.debug("Reading config data from local file...")
        try:   
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            class_logger.debug("Data read OK.")
            return True
        except Exception as ex:
            self.err_msg = "Issue reading config file: {}".format(ex)
            class_logger.error(self.err_msg)
            return False
        
    def update_config(self):
        """
        Write data to json config file
        """

        class_logger.debug("writing config data to local file...")
        try:   
            with open(self.config_file, 'w') as f:
                json.dump(self.config,  f, indent=4)
            class_logger.debug("Data dumped OK.")
            return True
        except Exception as ex:
            self.err_msg = "Issue writing config file: {}".format(ex)
            class_logger.error(self.err_msg)
            return False


    