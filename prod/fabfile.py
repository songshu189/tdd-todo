import re
from fabric.contrib.files import append, exists, upload_template
from fabric.api import cd, env, local, run, sudo, hide
from fabric.colors import green, yellow
from fabric.context_managers import settings
from fab_conf import FABRIC as conf


env.REPO_URL = conf.get("REPO_URL")
env.user = conf.get("user", "ubuntu")
env.project = conf.get("project", "myproject")
env.host_ip = conf.get("host_ip", "127.0.0.1")
env.hosts = conf.get("HOSTS", [""])
env.key_filename = conf.get("key_filename")
env.nginx = f"/etc/nginx/sites-available/{env.project}"
env.site_folder = f'/home/{env.user}/sites/{env.project}'

# ANSI Escape sequences - VT100 / VT52
ansi_escape = re.compile(r'(\x1b\[\?1[h|l])|(\x1b\[[m|K])|(\x1b[=|>])')

def update():
    site_folder = env.site_folder
    if not exists(site_folder):
       run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        output = run('git diff --name-only HEAD~ HEAD')
        changed_files = ansi_escape.sub('', output).strip().splitlines()
        if 'Pipfile' in changed_files:
           _update_pipenv()
        _update_setup_files()
        if any([file.endswith('models.py') for file in changed_files]):
            _update_database()

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {env.REPO_URL} .')
    # current_commit = local("git log -n 1 --format=%H", capture=True)
    # run(f'git reset --hard {current_commit}')
    print(green('get latese source'))

def _update_pipenv():
    if not run('which pipenv'):
        run(f'pip3 install --user pipenv')
    run('pipenv install')
    print(green('required package installed'))

def _update_setup_files():
    nginx_folder = f'/etc/nginx/sites-available/{env.project}'
    upload_template('prod/nginx.template',
                    nginx_folder,
                    env, use_sudo=True, backup=False
                    )
    upload_template('prod/local_settings.py.template',
        f'/home/{env.user}/sites/{env.project}/{conf["folder"]}/local_settings.py',
        env, use_sudo=True, backup=False
        )
    print(green('files updated'))
    sudo("systemctl daemon-reload")
    sudo("systemctl restart gunicorn")
    sudo("systemctl restart nginx")
    print(green('gunicorn and nginx restarted'))

def _update_database():
    run('pipenv shell')
    run('python manage.py makemigrations')
    run('python manage.py migrate')
    run('exit')
