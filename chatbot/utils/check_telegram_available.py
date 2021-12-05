#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess

"""
Simple class check if Telegram available
"""

import logging

logging.basicConfig(level=logging.INFO)
class_logger = logging.getLogger("Telegram_Checker")


class CheckTelegram(object):

    """
    A class to check if Telegram available
    """

    def __init__(self):

        self.nc_cmd = "/bin/nc"
        self.telegram_url = "api.telegram.org"
        self.telegram_port = 443

    def check_telegram_available(self):

        """
        Check we can hit the telegram server port to verify our network connection is good
        """
        class_logger.debug("Checking telegram port available")

        try:
            subprocess.check_output(
                "{} -zvw10 {} {}".format(
                    self.nc_cmd, self.telegram_url, self.telegram_port
                ),
                stderr=subprocess.STDOUT,
                shell=True,
            ).decode()
            class_logger.debug("Network connection to Telegram is good.")
            return True
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            class_logger.debug(
                "Network connection to Telegram is bad: {}".format(output)
            )
            return False
