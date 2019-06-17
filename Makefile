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
	$(ACT); FLASK_APP="flaskr:create_app('development')" python3.7 -m flask run

freeze:
	$(ACT); $(FREEZE); echo "Freezing done!"

test:
	$(ACT); pytest -vs

testCoverage:
	${ACT}; pytest -vs --cov=flaskr

_install:
	pip3.7 install -r $(REQ)

gunicorn:
	$(ACT); gunicorn --bind 0.0.0.0:5000 "flaskr:create_app('production')"

genSchema:
	$(ACT); python3.7 scripts/gen_schema.py
