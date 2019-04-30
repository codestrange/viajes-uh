host = 0.0.0.0
port = 5000

run:
	@export FLASK_APP=run.py &&\
	export FLASK_ENV=development &&\
	export FLASK_DEBUG=1 &&\
	flask run --host=${host} --port=${port}

run_pro:
	@export FLASK_APP=run.py &&\
	export FLASK_ENV=production &&\
	export FLASK_DEBUG=0
	flask run --host=${host} --port=${port}

shell:
	@export FLASK_APP=run.py &&\
	flask shell

db_init:
	@export FLASK_APP=run.py &&\
	flask db init

db_migrate:
	@export FLASK_APP=run.py &&\
	flask db migrate

db_upgrade:
	@export FLASK_APP=run.py &&\
	flask db upgrade

db_delete:
	@sudo rm -r migrations &&\
	sudo rm app/data_dev.sqlite

db_start: db_init db_migrate db_upgrade ;
	@export FLASK_APP=run.py &&\
	flask init

db_restart: db_delete db_start ;
