all: clean install build

build:
	pyinstaller --add-data "info_icon.png:." --onefile --hidden-import "PIL._tkinter_finder" "Tephra Glass Trace Database GUI.pyw" --clean

install:
	-pip install requirements.txt

clean:
	-rm *.spec
	-rm -rf dist build