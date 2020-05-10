CXX = g++
CXXFLAGS = -Ofast -std=c++17 -Wall -MMD -Werror=vla -DDEBUG -I../../UTTT/C++/
EXEC = sandbox

OBJECTS =  sandbox.o
DEPENDS = ${OBJECTS:.o=.d}

${EXEC}: ${OBJECTS}
	${CXX} ${CXXFLAGS} ${OBJECTS} -o ${EXEC} -L../../UTTT/C++ -lUTTT

-include ${DEPENDS}

clean:
	rm -f ${OBJECTS} ${EXEC} ${DEPENDS}
.PHONY: clean
