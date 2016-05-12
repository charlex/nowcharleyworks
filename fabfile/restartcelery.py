from fabric.api import sudo, task


@task
def restartcelery():
    """
    Restarts apache on both app servers.
    """
    sudo("/etc/init.d/celeryd_p2pliveblog restart", pty=True)
