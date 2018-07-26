CXX = g++
CXXFLAGS = -std=c++14 -DDEBUG -Wall -MMD -Werror=vla
EXEC = UTTT
# Boards/Board2D.o Boards/Quadrants.o 
# MCTS/Game.o  main.o
OBJECTS = Boards/Board.o MCTS/Node.o MCTS/Game.o  main.o
DEPENDS = ${OBJECTS:.o=.d}

${EXEC}: ${OBJECTS}
	${CXX} ${CXXFLAGS} ${OBJECTS} -o ${EXEC}

-include ${DEPENDS}

clean:
	rm ${OBJECTS} ${EXEC} ${DEPENDS}
.PHONY: clean
