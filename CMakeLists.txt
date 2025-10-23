cmake_minimum_required(VERSION 3.14)
project(my_project)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Create a library for tags module
add_library(DefensesLib
    modules/tags.cpp
)

# Add include directories
target_include_directories(DefensesLib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/modules
    ${CMAKE_CURRENT_SOURCE_DIR}/core
)

# Add the tests subdirectory
add_subdirectory(tests)