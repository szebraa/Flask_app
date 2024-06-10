import sys
sys.path.insert(0,'/var/www/Canonical-flask-app')

virt_env = '/var/www/Canonical-flask-app/.venv/'
with open(virt_env) as file_:
	exec(file_.read(),dict(__file__=virt_env))

from app import app as application
