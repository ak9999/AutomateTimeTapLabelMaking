# Author: AJ Khan
# Email: aj@ajkhan.me

all: directories
	make labels
	make samples

clean:
	rm codes/*
	rm samples/*
	rm *.log

directories:
	mkdir codes
	mkdir samples

labels:
	python create_label.py

retry: clean labels

sample:
	python sample.py
