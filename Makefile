ACT=. env/bin/activate
REQF=requirements-to-freeze.txt
REQ=requirements.txt
FREEZE=pip3.7 freeze -r $(REQF) > $(REQ)
APP_DEV="flaskr:create_app('development')"
APP_PROD="flaskr:create_app('production')"

init: createenv install

createenv:
	rm -rf env
	python3.7 -m venv env

install:
	$(ACT); pip3.7 install -r $(REQ)

upgradeInstall:
	$(ACT); pip3.7 install -r $(REQF) --upgrade
	$(ACT); $(FREEZE)

start:
	$(ACT); FLASK_APP=$(APP_DEV) flask seed-db
	$(ACT); FLASK_APP=$(APP_DEV) flask run

freeze:
	$(ACT); $(FREEZE); echo "Freezing done!"

test:
	$(ACT); pytest -vs

testCoverage:
	${ACT}; pytest -vs --cov=flaskr

_install:
	pip3.7 install -r $(REQ)

gunicorn:
	$(ACT); FLASK_APP=$(APP_PROD) python3.7 -m flask seed-db
	$(ACT); gunicorn --bind 0.0.0.0:5000 $(APP_PROD)

run_gunicorn:
	FLASK_APP=$(APP_PROD) python3.7 -m flask seed-db
	gunicorn --bind 0.0.0.0:5000 $(APP_PROD)

genSchema:
	$(ACT); python3.7 scripts/gen_schema.py

formatterLinter:
	$(ACT); black flaskr
	$(ACT); flake8 flaskr
