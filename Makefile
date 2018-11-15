frontend_run:
	cd frontend &&\
	npm run serve &&\
	cd ..

frontend_install:
	cd frontend &&\
	npm install &&\
	cd ..

frontend_build:
	cd frontend &&\
	npm run build &&\
	cd ..

backend_run:
	export FLASK_APP=run.py &&\
	export FLASK_ENV=development &&\
	export FLASK_DEBUG=1 &&\
	cd backend &&\
	flask run &&\
	cd ..

backend_pro:
	export FLASK_APP=run.py &&\
	export FLASK_ENV=production &&\
	export FLASK_DEBUG=0 &&\
	cd backend &&\
	flask run &&\
	cd ..

backend_shell:
	export FLASK_APP=run.py &&\
	cd backend &&\
	flask shell &&\
	cd ..

backend_ishell:
	cd backend &&\
	python run.py shell &&\
	cd ..

backend_test:
	export FLASK_APP=run.py &&\
	cd backend &&\
	flask test &&\
	cd ..

backend_db_init:
	export FLASK_APP=run.py &&\
	cd backend &&\
	flask db init &&\
	cd ..

backend_db_migrate:
	export FLASK_APP=run.py &&\
	cd backend &&\
	flask db migrate &&\
	cd ..

backend_db_upgrade:
	export FLASK_APP=run.py &&\
	cd backend &&\
	flask db upgrade &&\
	cd ..

backend_db_downgrade:
	export FLASK_APP=run.py &&\
	cd backend &&\
	flask db downgrade &&\
	cd ..

backend_db_stamp:
	export FLASK_APP=run.py &&\
	cd backend &&\
	flask db stamp &&\
	cd ..
