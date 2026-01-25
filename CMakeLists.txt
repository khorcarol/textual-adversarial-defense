if(MSVC)
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
endif()

cmake_minimum_required(VERSION 3.14)
project(my_project)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

# Download fribidi manually (bypass CMake step since it uses Meson)
set(FRIBIDI_VERSION "1.0.16")
set(FRIBIDI_SOURCE_DIR "${CMAKE_BINARY_DIR}/_deps/fribidi-src")
set(FRIBIDI_BUILD_DIR "${CMAKE_BINARY_DIR}/_deps/fribidi-build")
set(FRIBIDI_INSTALL_DIR "${CMAKE_BINARY_DIR}/_deps/fribidi-install")
# Meson installs to lib/x86_64-linux-gnu on Linux
set(FRIBIDI_LIB_PATH "${FRIBIDI_INSTALL_DIR}/lib/libfribidi.a")
set(FRIBIDI_INCLUDE_PATH "${FRIBIDI_INSTALL_DIR}/include")

# Download if not already present
    if(NOT EXISTS "${FRIBIDI_SOURCE_DIR}")
    # Find executables first
    find_program(MESON_EXECUTABLE meson REQUIRED)
    find_program(NINJA_EXECUTABLE ninja REQUIRED)
    message(STATUS "Downloading fribidi v${FRIBIDI_VERSION}...")
    file(DOWNLOAD
        "https://github.com/fribidi/fribidi/releases/download/v${FRIBIDI_VERSION}/fribidi-${FRIBIDI_VERSION}.tar.xz"
        "${CMAKE_BINARY_DIR}/fribidi-${FRIBIDI_VERSION}.tar.xz"
        SHOW_PROGRESS
    )
    # Create deps directory if needed
    file(MAKE_DIRECTORY "${CMAKE_BINARY_DIR}/_deps")
    
    # Extract archive with full path
    execute_process(
        COMMAND tar xJf "${CMAKE_BINARY_DIR}/fribidi-${FRIBIDI_VERSION}.tar.xz" -C "${CMAKE_BINARY_DIR}/_deps"
        RESULT_VARIABLE EXTRACT_RESULT
        OUTPUT_VARIABLE EXTRACT_OUTPUT
        ERROR_VARIABLE EXTRACT_ERROR
    )
    if(NOT EXTRACT_RESULT EQUAL 0)
        message(STATUS "Extract output: ${EXTRACT_OUTPUT}")
        message(STATUS "Extract error: ${EXTRACT_ERROR}")
        message(FATAL_ERROR "Failed to extract fribidi archive (code: ${EXTRACT_RESULT})")
    endif()
    # Rename extracted directory
    file(RENAME 
        "${CMAKE_BINARY_DIR}/_deps/fribidi-${FRIBIDI_VERSION}"
        "${FRIBIDI_SOURCE_DIR}"
    )
endif()

# Build fribidi with Meson - use add_custom_command to generate the library file
add_custom_command(OUTPUT "${FRIBIDI_LIB_PATH}"
    COMMAND ${CMAKE_COMMAND} -E make_directory ${FRIBIDI_BUILD_DIR}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${FRIBIDI_INSTALL_DIR}
    
    COMMAND ${MESON_EXECUTABLE} setup 
        --prefix=${FRIBIDI_INSTALL_DIR}
        --libdir=lib
        --default-library=static
        -Dtests=false
        -Ddocs=false
        ${FRIBIDI_BUILD_DIR}
        ${FRIBIDI_SOURCE_DIR}
    
    COMMAND ${NINJA_EXECUTABLE} -C ${FRIBIDI_BUILD_DIR}
    COMMAND ${NINJA_EXECUTABLE} -C ${FRIBIDI_BUILD_DIR} install
    
    DEPENDS ${FRIBIDI_SOURCE_DIR}/meson.build
    COMMENT "Building fribidi with Meson"
)

# Create a custom target that produces the library file
add_custom_target(fribidi_build ALL DEPENDS "${FRIBIDI_LIB_PATH}")

# Create imported library target for fribidi
add_library(fribidi STATIC IMPORTED)
set_target_properties(fribidi PROPERTIES
    IMPORTED_LOCATION "${FRIBIDI_LIB_PATH}"
)
# Static linking declaration(needed on Windows)
target_compile_definitions(fribidi INTERFACE FRIBIDI_LIB_STATIC)

add_dependencies(fribidi fribidi_build)

# --- Core Library Setup ---
add_library(DefensesLib
    modules/invisible.cpp
    modules/tags.cpp
    modules/bidi.cpp
    modules/homoglyph.cpp
    modules/variation_selector.cpp
    modules/deletion.cpp
    modules/combined.cpp
    core/pipeline.cpp
    utils.cpp
)

set_target_properties(DefensesLib PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Add dependency AFTER fribidi_build is defined
add_dependencies(DefensesLib fribidi_build)

target_include_directories(DefensesLib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/modules
    ${CMAKE_CURRENT_SOURCE_DIR}/core
    ${CMAKE_CURRENT_SOURCE_DIR}
    "$<BUILD_INTERFACE:${FRIBIDI_INCLUDE_PATH}>"
)

FetchContent_Declare(
  json
  GIT_REPOSITORY https://github.com/nlohmann/json.git
  GIT_TAG v3.11.3
)

FetchContent_MakeAvailable(json)

target_link_libraries(DefensesLib PUBLIC
    fribidi nlohmann_json::nlohmann_json
)

FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.11.1
)
FetchContent_MakeAvailable(pybind11)

add_subdirectory(tests)

pybind11_add_module(_pipeline
    python/pipeline_bindings.cpp  
)

target_link_libraries(_pipeline PRIVATE DefensesLib)
add_dependencies(_pipeline fribidi_build)

install(TARGETS _pipeline LIBRARY DESTINATION textual_adversarial_defense)