#include <gtest/gtest.h>
#include "homoglyph.h"

// // One to One mappings sanitised
// TEST(HomoglyphSanitizerTests, OneToOneMappings)
// {
//     HomoglyphSanitizer homoglyph_sanitizer;
//     std::vector<char32_t> text = {0x0430, 0x03B1, 0xFF41}; // 'а', 'α', 'ａ', 'b'
//     homoglyph_sanitizer.sanitize(text);

//     std::vector<char32_t> expected = {0x0061, 0x0061, 0x0061}; // 'a', 'a', 'a', 'b'
//     EXPECT_EQ(text, expected);
// }

// // One to Many mappings sanitised
// TEST(HomoglyphSanitizerTests, OneToManyMappings)
// {
//     HomoglyphSanitizer homoglyph_sanitizer;
//     std::vector<char32_t> text = {0x1F124}; // '⒤' (circled U)
//     homoglyph_sanitizer.sanitize(text);

//     std::vector<char32_t> expected = {0x0028, 0x0055, 0x0029}; // '(U)'
//     EXPECT_EQ(text, expected);
// }

// One to One mappings sanitised
TEST(HomoglyphSanitizerTests, OneToOneMappings)
{
    HomoglyphSanitizer homoglyph_sanitizer;
    std::vector<char32_t> text = {0x0391, 0x001C3, 0x0392}; 
    homoglyph_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {0x0041, 0x0021, 0x0042}; 
    EXPECT_EQ(text, expected);
}

// No mappings present, input remains unchanged
TEST(HomoglyphSanitizerTests, NoMappings)
{
    HomoglyphSanitizer homoglyph_sanitizer;
    std::vector<char32_t> text = {0x0062, 0x0063, 0x0064}; // 'b', 'c', 'd'
    homoglyph_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {0x0062, 0x0063, 0x0064}; // 'b', 'c', 'd'
    EXPECT_EQ(text, expected);
}