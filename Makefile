all: test

test:
	coverage run -m pytest && coverage report -m --include=vkpore/*

apidoc:
	sphinx-apidoc --separate -o docs/src/ vkpore ${PWD}/setup.py

htmldocs:
	cd docs && make html

run:
	@PYTHONPATH=${PWD} python example/lognpoll.py ${shell cat example/.token | tr -d '\n'}

check: test
	mypy vkpore
	pylint vkpore
