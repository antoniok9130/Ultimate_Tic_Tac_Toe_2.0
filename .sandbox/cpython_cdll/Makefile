CXX = g++
CXXFLAGS = -Ofast -std=c++17 -fPIC -shared
LIB = sandbox.so

OBJECTS =  sandbox.o
DEPENDS = ${OBJECTS:.o=.d}

${LIB}: ${OBJECTS}
	${CXX} ${CXXFLAGS} -Wl,-soname,${LIB} ${OBJECTS} -o ${LIB}
# $(CXX) -fPIC -shared -Wl,-soname,${LIB} -o ${LIB}

-include ${DEPENDS}

clean:
	rm ${OBJECTS} ${LIB} ${DEPENDS}
.PHONY: clean
