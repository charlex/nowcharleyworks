from fabric.api import settings, task
from .pull import pull
from .clean import clean
from .pipinstall import pipinstall
from .collectstatic import collectstatic
from .restartapache import restartapache
from .restartcelery import restartcelery
from .takemetothecloudsabove import takemetothecloudsabove


@task
def deploy():
    """
    Deploy the latest code and restart everything.
    """
    pull()
    with settings(warn_only=True):
        clean()
    pipinstall()
    collectstatic()
    restartapache()
    restartcelery()
    takemetothecloudsabove()
