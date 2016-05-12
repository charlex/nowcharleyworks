import os
from .venv import _venv
from .env import env
from fabric.api import task, sudo, settings


@task
def restart_celery():
    """
    Restarts the celeryd task server
    """
    _venv("/etc/init.d/celeryd_p2pliveblog restart")


@task
def kill_celery():
    sudo("ps auxww | grep celeryd | awk '{print $2}' | xargs kill -9")


@task
def update_celery_daemon():
    """
    Update the celeryd init file on prod.
    """
    with settings(warn_only=True):
        sudo("service celeryd_p2pliveblog stop")
    source = os.path.join(env.project_dir, 'project', 'celeryd_p2pliveblog')
    target = os.path.join('/etc', 'init.d', 'celeryd_p2pliveblog')
    with settings(warn_only=True):
        sudo("rm %s" % target)
    sudo("cp %s %s" % (source, target))
    sudo("chmod +x %s" % target)
    sudo("service celeryd_p2pliveblog restart")
