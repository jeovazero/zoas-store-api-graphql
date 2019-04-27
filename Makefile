ACT=. env/bin/activate
REQF=requirements-to-freeze.txt
REQ=requirements.txt
FREEZE=pip3.7 freeze -r $(REQF) > $(REQ)

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
	$(ACT); FLASK_APP=flaskr/app.py FLASK_ENV=development python3.7 -m flask run

freeze:
	$(ACT); $(FREEZE); echo "Freezing done!"

test:
	$(ACT); FLASK_TESTING=True pytest -vs

_install:
	pip3.7 install -r $(REQ)

gunicorn: # TESTING only to seed the database, remove it in for production :)
	$(ACT); FLASK_TESTING=True gunicorn --bind 0.0.0.0:5000 flaskr.app:app
