backend_host = 0.0.0.0
backend_port = 5000
backend_env = development
backend_debug = 1

frontend_run:
	cd frontend &&\
	npm run serve

frontend_install:
	cd frontend &&\
	sudo npm install

backend_run:
	export FLASK_APP=run.py &&\
	export FLASK_ENV=${backend_env} &&\
	export FLASK_DEBUG=1${backend_debug} &&\
	cd backend &&\
	flask run --host=${backend_host} --port=${backend_port}

backend_install:
	pipenv install

backend_activate_env:
	pipenv shell

backend_shell:
	export FLASK_APP=run.py &&\
	cd backend &&\
	flask shell
