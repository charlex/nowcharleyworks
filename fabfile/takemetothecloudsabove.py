from fabric.api import task, local


@task
def takemetothecloudsabove():
    """
    Let Whitney tell it.
    """
    local("curl -I http://databank-soundsystem.latimes.com/take-me-to-the-clouds-above/")
