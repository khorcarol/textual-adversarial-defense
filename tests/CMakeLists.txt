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
)

foreach(test_target ${TEST_TARGETS})
    add_executable(${test_target}
        ${test_target}.cpp
    )
    
    target_link_libraries(${test_target} PRIVATE
        DefensesLib
        GTest::gtest_main
    )
    
    gtest_discover_tests(${test_target})
endforeach()