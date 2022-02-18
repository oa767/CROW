LINTER = flake8
API_DIR = API
DB_DIR = db
REQ_DIR = .
PYDOC = python3 -m pydoc -w
TESTFINDER = nose2

FORCE:

prod: all_tests github

github: FORCE
	git add -A
	- git commit -a
	git push origin master

dev_env: FORCE
	- ./setup.sh DEMO_HOME
	pip install -r requirements-dev.txt

all_tests: FORCE
	cd $(API_DIR); make tests
	cd $(DB_DIR); make tests

all_docs: FORCE
	cd $(API_DIR); make docs
	cd $(DB_DIR); make docs
