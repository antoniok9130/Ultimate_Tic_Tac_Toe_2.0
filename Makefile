
build:
	cd UTTT/C++ && rm -f libUTTT.so && make

play: build
	python -u UTTT/Python/Game/Game.py

sandbox:
	sandboxer --create --name $(name) --lang $(lang)

experiment: build
	sandboxer --build --name $(name) --lang $(lang)

exp: experiment

pyexp: build
	sandboxer --build --name $(name) --lang python
