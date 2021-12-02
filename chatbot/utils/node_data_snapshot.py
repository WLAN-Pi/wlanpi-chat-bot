#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Read & write snapshot of node status data dumped to local file system.

This data is used to detect things like sytem changes that may need to be reported.
"""

import json
import time
import logging
import os
import socket
import psutil
import netifaces as ni

logging.basicConfig(level=logging.INFO)
class_logger = logging.getLogger('DataSnapshot')
#class_logger.setLevel(logging.DEBUG)

class DataSnapshot(object):

    '''
    Read & write snapshot of status data dumped to file system
    '''

    def __init__(self, local_file="/tmp/snapshot.json",):

        self.local_file = local_file
        self.err_msg = ''
        self.data = {}
    
    def write_data(self):
        """
        Write current data snapshot to file
        """
              
        class_logger.debug("Writing snapshot data to local file...")
        try:   
            with open(self.local_file, 'w') as f:
                json.dump(self.data, f, indent=4)
            class_logger.debug("Data written OK.")
            return True
        except Exception as ex:
            self.err_msg = "Issue writing data file: {}".format(ex)
            class_logger.error(self.err_msg)
            return False
    
    def read_data(self):
        """
        Read data from snapshot file
        """

        class_logger.debug("Reading snapshot data from local file...")
        try:   
            with open(self.local_file, 'r') as f:
                data = json.load(f)
            class_logger.debug("Data read OK.")
            return data
        except Exception as ex:
            self.err_msg = "Issue reading data file: {}".format(ex)
            class_logger.error(self.err_msg)
            return False


    def check_snapshot_exists(self):
        """
        Check snapshot file exists on local file system, create if not
        """

        if os.path.exists(self.local_file):
            return True
        
        return False
    
    def get_hostname(self):

        # get hostname
        return socket.gethostname()
    
    def get_uptime(self, format="string"):
        seconds = time.time() - psutil.boot_time()

        if format == "raw":
            return seconds

        min, sec = divmod(seconds, 60) 
        hour, min = divmod(min, 60)
        day, hour = divmod(hour, 24)
        return "%d days %d:%02d:%02d" % (day, hour, min, sec)
    
    def get_interface_details(self):
        
        interfaces = ni.interfaces()
        AF_INET = 2
        interface_data = {}

        for interface in interfaces:

            # ignore loopback
            if interface == 'lo':
                continue

            # check if interface has IP address
            interface_details = ni.ifaddresses(interface)

            if AF_INET in interface_details.keys():
                address = interface_details[AF_INET][0]['addr']
                interface_data[interface] = address

        return interface_data
    
    def init_snapshot(self):
        """
        Create snapshot file from scratch 
        """

        interface_data = self.get_interface_details()
        hostname = self.get_hostname()

        self.data = {
            'interfaces': interface_data,
            'hostname': hostname,
        }

        return self.data
    
    def node_status(self):

        unit_status = ''
        
        # check if snapshot exists, create if not
        class_logger.debug("Checking if we already have a status snapshot...")

        if self.check_snapshot_exists():
            class_logger.debug("Snapshot exists, create new one and compare to original (any diff)?")
            # snapshot exists - compare existing snapshot with new snapshot
            if self.read_data() == self.init_snapshot():
                class_logger.debug("Snapshots match, no changes detected.")
                # nothing has changed, nothing to report
                return False

            else:
                # something has changed with the config, set status
                class_logger.debug("Snapshots do not match...config change detected")
                self.write_data()
                unit_status = "Config change"

        else:
            # unit must have freshly booted, create snapshot &
            # set status to rebooted
            class_logger.debug("Boot detected...create snapshot")
            self.init_snapshot()
            self.write_data()
            unit_status = "Rebooted"
            if self.get_uptime(format="raw") > 120:
                unit_status = "Running"
        
        class_logger.debug("Create status data...")
        # get hostname
        hostname =  self.data['hostname']

        # get uptime
        uptime = self.get_uptime()

        # Figure out the interface addresses:
        interfaces = self.data['interfaces']
        ip_addresses = []

        for name, ip in interfaces.items():
            # ignore loopback interface
            if name == 'lo':
                continue

            ip_addresses.append(f" {name}: {ip}")

        # Construct message to send
        now = time.ctime()
        messages = [
            f"Time: {now}", 
            f"Hostname: {hostname}", 
            f"Uptime: {uptime}",
            f"Unit status: {unit_status}",
            '\nInterfaces: '] + ip_addresses
        
        return messages
