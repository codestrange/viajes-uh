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

backend_test:
	export FLASK_APP=run.py &&\
	cd backend &&\
	flask test &&\
	cd ..
