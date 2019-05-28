all: test

test:
	coverage3 run -m pytest && coverage3 report -m --include=vkpore/*

apidoc:
	sphinx-apidoc --separate -o docs/src/ vkpore ${PWD}/setup.py

htmldocs:
	cd docs && make html

run_example:
	@PYTHONPATH=${PWD} python3 example/run.py ${shell cat example/.token | tr -d '\n'}

check: test
	mypy vkpore
	pylint vkpore
