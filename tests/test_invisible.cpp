#include <gtest/gtest.h>
#include "invisible.h"
#include "pipeline.h"

TEST(InvisibleCharSanitizerTest, RemovesZeroWidthSpace)
{
    InvisibleCharSanitizer invisible_char_sanitizer;
    // Input: "a<ZWSP>b" where ZWSP is U+200B
    std::vector<char32_t> with_invisible = {U'a', 0x200B, U'b'};
    invisible_char_sanitizer.sanitize(with_invisible);

    std::vector<char32_t> expected = {U'a', U'b'};

    EXPECT_EQ(with_invisible, expected);
}

TEST(InvisibleCharSanitizerTest, PreserveCharacters)
{
    InvisibleCharSanitizer invisible_char_sanitizer;
    std::vector<char32_t> without_invisible = {U'a', U'b'};
    invisible_char_sanitizer.sanitize(without_invisible);

    EXPECT_EQ(without_invisible, without_invisible);
}
