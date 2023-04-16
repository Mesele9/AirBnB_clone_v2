#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py) that creates
   and distributes an archive to your web servers, using the function deploy:
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['54.80.197.65', '54.157.160.175']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """ a Fabric script that generates a .tgz archive from the contents
    of the web_static folder of your AirBnB Clone rep"""
    time_stamp = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/"
              .format(time_stamp))
        return "versions/web_static_{}.tgz".format(time_stamp)
    except:
        return None


def do_deploy(archive_path):
    """ a function to deploy files to server"""
    try:
        if not (path.exists(archive_path)):
            return False

        archive_name = path.basename(archive_path)
        archive_basename = path.splitext(archive_name)[0]
        put(archive_path, '/tmp/{}'.format(archive_name))
        release_path = '/data/web_static/releases/{}'.format(archive_basename)
        run('sudo mkdir -p {}'.format(release_path))

        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_name, release_path))

        run('sudo rm /tmp/{}'.format(archive_name))

        run('sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'
            .format(archive_basename, archive_basename))

        run('sudo rm -rf /data/web_static/release/{}/web_static'
            .format(archive_basename))

        run('sudo rm -rf /data/web_static/current')

        run('sudo ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(archive_basename))

        except:
            return False

        return True


def deploy():
    """Fabric script that creates and distributes an archive to your
    web servers, using the function deploy"""
    archive_file = do_pack()

    if archive_file is None:
        return False
    return do_deploy(archive_file)
