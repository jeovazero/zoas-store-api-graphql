ACT=. env/bin/activate
REQF=requeriments-to-freeze.txt
REQ=requeriments.txt
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
	$(ACT); FLASK_APP=src/app.py FLASK_DEBUG=1 python3.7 -m flask run

freeze:
	$(ACT); $(FREEZE); echo "Freezing done!"

_install:
	pip3.7 install -r $(REQ)
