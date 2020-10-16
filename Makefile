# Author: AJ Khan
# Email: aj@ajkhan.me

all:
	pyinstaller --onefile --noupx --windowed --icon ./resources/clock.ico ./AutoTimeTapLabelMaker2.py

clean:
	rm *.spec
	rm dist/AutoTimeTapLabelMaker.exe