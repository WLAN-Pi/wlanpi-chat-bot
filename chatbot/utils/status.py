import os


def get_status():
    """ Read in status from bash script """
    here = os.path.dirname(os.path.realpath(__file__))
    stream = os.popen(os.path.join(here, "../bash_scripts/probe_status_msg.sh"))
    startup_msg = stream.read()
    return startup_msg
