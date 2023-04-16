#!/usr/bin/python3
from fabric.api import local
from time import strftime
from datetime import datetime


def do_pack():
    """ a Fabric script that generates a .tgz archive from the contents
    of the web_static folder of your AirBnB Clone rep"""
    time_stamp = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/"
              .format(time_stamp))
        return "versions/web_static_{}.tgz".format(time_stamp)
    except Exception as e:
        return None
