from fabric.api import env, task
from os.path import expanduser


@task
def prod():
    env.hosts = ("52.9.186.157",)
    env.branch = 'master'

prod()
env.key_filename = (
    expanduser('~/.ssh/nowcharleyworks.pem'),
)
env.user = 'ubuntu'
env.known_hosts = ''
env.chef = '/usr/local/bin/chef-solo -c solo.rb -j node.json'
env.app_user = 'ubuntu'
env.project_dir = '/apps/nowcharleyworks/repo/'
env.activate = 'source /apps/nowcharleyworks/bin/activate'
env.AWS_SECRET_ACCESS_KEY = 'L8yGqtt8ZRfxT4yELbD5AXnDiVJg4ImYescedCWn'
env.AWS_ACCESS_KEY_ID = 'AKIAIHQHKKW2OV3ZDZIA'
