cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(UTTT)

set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

find_package(Torch REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

add_executable(train train.cc)
target_sources(train PRIVATE model.cc)
target_link_libraries(train "${TORCH_LIBRARIES}")
set_property(TARGET train PROPERTY CXX_STANDARD 17)
