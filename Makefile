
build:
	cd UTTT/C++ && rm -f libUTTT.so && make
.PHONY: build

play: build
	python -u UTTT/UTTT.py

sandbox:
	sandboxer --create --name $(name) --lang $(lang)

experiment: build
	sandboxer --build --name $(name) --lang $(lang)

exp: experiment

pyexp: build
	sandboxer --build --name $(name) --lang python

package:
	pyinstaller --add-data "UTTT/C++/libUTTT.so:." --onefile UTTT/UTTT.py

pkg: package
