LINTER = flake8 --ignore=E501,E251,W503,E203,E201
API_DIR = API
DB_DIR = db
REQ_DIR = .
PYDOC = python3 -m pydoc -w
TESTFINDER = nose2

export TEST_MODE = 1

FORCE:

tests: unit

unit: FORCE
	$(TESTFINDER)

lint: FORCE
	$(LINTER) *.py

docs: FORCE
	$(PYDOC) ./*.py
	git add ./*.html
