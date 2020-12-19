# Author: AJ Khan
# Email: aj@ajkhan.me

all:
	pyinstaller --onefile --noupx --windowed --icon ./resources/clock.ico ./AutoTimeTapLabelMaker2.py

dev:
	pyinstaller --onefile --noupx --windowed --icon ./resources/clock.ico ./AutoTimeTapLabelMaker3.py

clean:
	rm *.spec
	rm dist/*