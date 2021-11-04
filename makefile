LINTER = flake8
API_DIR = API
DB_DIR = db
REQ_DIR = .
PYDOC = python3 -m pydoc -w
TESTFINDER = nose2

FORCE:

prod: tests github

github: FORCE
	git add -A
	- git commit -a
	git push origin master

tests: lint unit

unit: FORCE
	cd $(API_DIR); $(TESTFINDER) --with-coverage

lint: FORCE
	$(LINTER) $(API_DIR)/*.py
	$(LINTER) $(DB_DIR)/*.py

dev_env: FORCE
	pip install -r requirements-dev.txt

docs: FORCE
	$(PYDOC) $(API_DIR)/*.py
	$(PYDOC) $(DB_DIR)/*.py
