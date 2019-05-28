all: test

test:
	coverage3 run -m pytest && coverage3 report -m --include=vkpore/*

run_example:
	@PYTHONPATH=${PWD} python3 example/run.py ${shell cat example/.token | tr -d '\n'}
