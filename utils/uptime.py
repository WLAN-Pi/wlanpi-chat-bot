#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psutil
import time

class Uptime(object):

    '''
    A class that returns the probe uptime
    '''

    def __init__(self):

        pass
    
    def get_uptime(self, format="string"):
        """[summary]

        Args:
            format (str, optional): "raw" returns number of seconds, "string" returns formatted # days & hh:mm:ss. Defaults to "string".

        Returns:
            [string]: Uptime string
        """
        seconds = time.time() - psutil.boot_time()

        if format == "raw":
            return seconds

        min, sec = divmod(seconds, 60) 
        hour, min = divmod(min, 60)
        day, hour = divmod(hour, 24)
        
        return "%d days %d:%02d:%02d" % (day, hour, min, sec)

