#include <gtest/gtest.h>
#include "deletion.h"

// One to One mappings sanitised
TEST(DeletionSanitizerTests, Deletion)
{
    DeletionCharSanitizer deletion_sanitizer;
    std::vector<char32_t> text = {0x3, 0x1, 0x2, 0x8, 0x8 , 0x9};
    deletion_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {0x3, 0x9}; 
    EXPECT_EQ(text, expected);
}

TEST(DeletionSanitizerTests, NoDeletions)
{
    DeletionCharSanitizer deletion_sanitizer;
    std::vector<char32_t> text = {0x3, 0x9};
    deletion_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {0x3, 0x9}; 
    EXPECT_EQ(text, expected);
}
