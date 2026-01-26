enable_testing()

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
FetchContent_MakeAvailable(googletest)


include(GoogleTest)
set(TEST_TARGETS
    test_invisible
    test_tags
    test_homoglyph
    test_variation_selector
    test_bidi
    test_deletion
    test_combination
)

foreach(test_target ${TEST_TARGETS})
    add_executable(${test_target}
        ${test_target}.cpp
    )
    
    target_link_libraries(${test_target} PRIVATE
        DefensesLib
        GTest::gtest_main
    )

    if(MSVC)
        set_property(TARGET ${test_target} PROPERTY
        MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL"
        )
    endif()
    
    gtest_discover_tests(${test_target})
endforeach()