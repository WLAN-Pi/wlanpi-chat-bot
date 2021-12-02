#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Functions to retrieve centralized remote config file

Currently assumes cfg file on GitHub private repo
"""

import warnings
import requests
import json
from requests.exceptions import HTTPError
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings() # keep SSL warnings quiet
import time
import logging

logging.basicConfig(level=logging.INFO)
class_logger = logging.getLogger('RemoteConfig')

class RemoteConfig(object):

    '''
    A class to pull a remote config file from a http site
    '''

    def __init__(self, url, local_file, token='', refresh_interval=900, timestamp_file='/tmp/config_timestamp.dat', username='', password=''):

        self.cfg_file_url = url
        self.cfg_token = token
        self.cfg_username = username
        self.cfg_password = password
        self.cfg_refresh_interval = refresh_interval
        self.cfg_text = ''
        self.local_file = local_file
        self.timestamp_file = timestamp_file
        self.err_msg = ''
    
        # if we use a token, we need to set user/pwd to be same as token (for Github)
        if self.cfg_token:
            self.cfg_username = self.cfg_token
            self.cfg_password = self.cfg_token
    
    def write_cfg_timestamp(self):
        """
        Write current timestamp to cfg timestamp file
        """
        
        time_now = str(int(time.time()))
        
        class_logger.debug("Writing current time to cfg timestamp file...")
        try:   
            with open(self.timestamp_file, 'w') as f:
                f.write(time_now)
            class_logger.debug("Written OK.")
            return True
        except Exception as ex:
            self.err_msg = "Issue writing cfg timestamp file: {}".format(ex)
            class_logger.error(self.err_msg)
            return False
    
    def read_remote_cfg(self):
        """
        Pull the remote cfg file if refresh time expired or on first boot
        """

        class_logger.debug("Trying to pull config file from : {}".format(self.cfg_file_url))
        try:
            #warnings.simplefilter('ignore',InsecureRequestWarning)
            response = requests.get(self.cfg_file_url, auth=(self.cfg_username, self.cfg_password), timeout=5)
            if response.status_code == 200:
                self.cfg_text = response.text
                class_logger.debug("Config file pulled OK.")
        except Exception as err:
            self.err_msg = "Config file pull error: {}".format(err)
            class_logger.error(self.err_msg)
            return False

        if self.cfg_text:
            class_logger.debug("Writing pulled config file to local config...")
            try:   
                with open(self.local_file, 'w') as f:
                    f.write(self.cfg_text)
                class_logger.debug("Local config file written OK.")
                self.write_cfg_timestamp()
                return True
            except Exception as ex:
                self.err_msg = "Config file write error: {}".format(ex)
                class_logger.error(self.err_msg )
                return False
        else:
            self.err_msg = "No data detected in cfg file, nothing written to file (check file URL and access permissions)"
            class_logger.error(self.err_msg)
            return False

    
    def check_cfg_timestamp(self):
        """
        Read timestamp from cfg timestamp file and force pull of remote cfg file if required
        """

        time_now = int(time.time())
        last_read_time = 0

        class_logger.debug("Checking cfg last-read timestamp...")
        try:
            with open(self.timestamp_file) as f:
                last_read_time = f.read()
            class_logger.debug("Last read timestamp: {}".format(last_read_time))
        except FileNotFoundError:
            # file does not exist, create & write timestamp
            class_logger.debug("Timestamp file does not exist, creating...")
            self.write_cfg_timestamp()
        except Exception as e:
            self.err_msg = "Timestamp file read error: {}".format(e)
            class_logger.error(self.err_msg)
            return False
        
        # if config file not read in last refresh interval, pull cfg file
        current_diff = int(time_now) - int(last_read_time)
        class_logger.debug("Checking time diff, time now: {}, last read time: {}, interval: {}, current diff: {}".format(time_now, 
                                                                          last_read_time, self.cfg_refresh_interval, current_diff))

        if (time_now - int(last_read_time)) >  int(self.cfg_refresh_interval):
            class_logger.debug("Time to read remote cfg file...")
            return self.read_remote_cfg()
        else:
            class_logger.debug("Not time to read remote cfg file.")
            return False



