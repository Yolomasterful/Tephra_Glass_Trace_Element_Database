all: install build

build:
	pyinstaller --onefile "Tephra Glass Trace Database GUI.pyw"

install:
	-pip install requirements.txt