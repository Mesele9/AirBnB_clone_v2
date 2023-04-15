#!/usr/bin/python3
from fabric.api import local
from datetime import datetime

def do_pack():
    """ a Fabric script that generates a .tgz archive from the contents
    of the web_static folder of your AirBnB Clone rep"""
    try:
        time_stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_path = "versions/web_static_{}.tqz".format(time_stamp)
        local("tar -cvzf{} web_static".format(file_path))
        return file_path
    except Exception as e:
        return None
