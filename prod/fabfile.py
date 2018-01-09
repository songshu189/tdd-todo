import random
from fabric.contrib.files import append, exists, upload_template
from fabric.api import cd, env, local, run, sudo
from fabric.colors import green, yellow

from django.conf import settings
conf = settings.FABRIC

REPO_URL = 'https://github.com/hjwp/book-example.git'
env.REPO_URL = conf.get("REPO_URL")
env.user = conf.get("user", "ubuntu")
env.project = conf.get("project", "myproject")
env.host_ip = conf.get("host_ip", "127.0.0.1")
env.hosts = conf.get("HOSTS", [""])
env.nginx = f"/etc/nginx/sites-available/{env.project}"
env.site_folder = f'/home/{env.user}/sites/{env.project}'


def update():
    site_folder = env.site_folder
    if not exists(site_folder):
       run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_pipenv()
        _update_files()
        _update_database()

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')
    print(green(''))

def _update_pipenv():
    if not run('which pipenv'):
        run(f'pip instsll --user pipenv')
    run('pipenv install')
    print(green('package installed'))

def update_files():
    nginx_folder = f'/etc/nginx/sites-available/{env.project}'
    upload_template('deploy/nginx.template',
                    nginx_folder,
                    env, use_sudo=True, backup=False
                    )
    upload_template('deploy/local_settings.py.template',
        f'/home/{env.user}/sites/{env.project}/{conf["folder"]}/local_settings.py',
        env, use_sudo=True, backup=False
        )
    print(green('files updated'))
    sudo("systemctl daemon-reload")
    sudo("systemctl restart gunicorn")
    sudo("systemctl restart nginx")
    print(green('gunicorn and nginx restarted'))

def _update_database():
    run('python manage.py makemigrations')
    run('python manage.py migrate')
