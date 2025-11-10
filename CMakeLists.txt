cmake_minimum_required(VERSION 3.14)
project(my_project)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Create a library for tags module
add_library(DefensesLib
    modules/invisible.cpp
    modules/tags.cpp
    modules/bidi.cpp
    modules/homoglyph.cpp
    modules/variation_selector.cpp
    modules/deletion.cpp
    core/pipeline.cpp
    utils.cpp
)
set_target_properties(DefensesLib PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

# Add include directories
target_include_directories(DefensesLib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/modules
    ${CMAKE_CURRENT_SOURCE_DIR}/core
    ${CMAKE_CURRENT_SOURCE_DIR}
)

include(FetchContent)
FetchContent_Declare(
  json
  GIT_REPOSITORY https://github.com/nlohmann/json.git
  GIT_TAG v3.11.2
)
FetchContent_MakeAvailable(json)

target_link_libraries(DefensesLib PUBLIC
    fribidi nlohmann_json::nlohmann_json
)

# Add the tests subdirectory
add_subdirectory(tests)


# Enable Python bindings
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.11.1  # Use latest stable version
)
FetchContent_MakeAvailable(pybind11)

pybind11_add_module(_pipeline
    python/pipeline_bindings.cpp  
)

target_link_libraries(_pipeline PRIVATE
    DefensesLib  
)

set_target_properties(_pipeline PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/python
)

