#include <gtest/gtest.h>
#include "bidi.h"
#include <stdio.h>
#include <utils.h>
TEST(BidiSanitizerTests_ReorderRLO_Test, ReordersRLOSegment)
{
    BidiCharSanitizer bidi_sanitizer;

    std::vector<char32_t> text = {
        0x202E,
        0x0064, 0x006C, 0x0072, 0x006F, 0x0057, // 'd','l','r','o','W'
        0x202C};
    
    std::cerr << utils::codepoints_to_utf8(text) << std::endl;

    bidi_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {
        0x202E,                                 // RLO
        0x0057, 0x006F, 0x0072, 0x006C, 0x0064, // 'W','o','r','l','d'
        0x202C                                  // PDF
    };

    EXPECT_EQ(text, expected);
}

