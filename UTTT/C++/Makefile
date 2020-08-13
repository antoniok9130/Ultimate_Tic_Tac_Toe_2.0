CXX = g++
CXXFLAGS = -Ofast -g -std=c++17 -fPIC -shared -fopenmp -DLEAF_PARALLEL
LIB = libUTTT.so

SOURCES = $(wildcard src/*.cc)
OBJECTS = $(SOURCES:.cc=.o)
DEPENDS = ${OBJECTS:.o=.d}

${LIB}: ${OBJECTS}
	${CXX} ${CXXFLAGS} -Wl,-soname,${LIB} ${OBJECTS} -o ${LIB}

-include ${DEPENDS}

clean:
	rm -f ${OBJECTS} ${LIB} ${DEPENDS}
.PHONY: clean
