#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['54.80.197.65', '54.157.160.175']
env.user = 'ubuntu'
env.my_ssh_private_key = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """ a function to deploy files to server"""
    try:
        if not (path.exists(archive_path)):
            return False

        put(archive_path, '/tmp/')

        time_stamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'
            .format(time_stamp))

        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/\
                releases/web_static_{}/'.format(time_stamp, time_stamp))

        run('sudo rm /tmp/web_static_{}.tgz'.format(time_stamp))

        run('sudo mv /data/web_static/releases/web_static_{}/web_static/*\
            /data/web_static/releases/web_static_{}/'
            .format(time_stamp, time_stamp))

        run('sudo rm -rf /data/web_static/release/\
            web_static_{}/web_static'.format(time_stamp))

        run('sudo rm -rf /data/web_static/current')

        run('sudo ln -s /data/web_static/releases/\
            web_static_{}/ /data/web_static/current'.format(time_stamp))
    except:
        return False

    return True
