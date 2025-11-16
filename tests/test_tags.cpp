#include <gtest/gtest.h>
#include "tags.h"

TEST(SanitizeTests, ValidTagSequence)
{
    TagCharSanitizer tag_char_sanitizer;

    std::vector<char32_t> text = {
        0x1F3F4,
        0xE0000 + 'g', 0xE0000 + 'b', 0xE0000 + 'e', 0xE0000 + 'n', 0xE0000 + 'g',
        0xE007F};

    tag_char_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {
        0x1F3F4,
        0xE0000 + 'g', 0xE0000 + 'b', 0xE0000 + 'e', 0xE0000 + 'n', 0xE0000 + 'g',
        0xE007F};

    EXPECT_EQ(text, expected);
}

TEST(SanitizeTests, TagOutsideBase)
{
    TagCharSanitizer tag_char_sanitizer;
    std::vector<char32_t> text2 = {
        0xE0000 + 'g', 0xE0000 + 'b', 0xE0000 + 'e', 0xE0000 + 'n', 0xE0000 + 'g'};
    tag_char_sanitizer.sanitize(text2);

    // Invalid tag sequence should be removed
    std::vector<char32_t> expected = {};
    EXPECT_EQ(text2, expected);
}

TEST(SanitizeTests, InvalidTagSequence)
{
    TagCharSanitizer tag_char_sanitizer;
    std::vector<char32_t> text2 = {
        0x1F3F4,
        0xE0000 + 'a', 0xE0000 + 'b', 0xE0000 + 'c',
        0xE007F};
    tag_char_sanitizer.sanitize(text2);

    // Invalid tag sequence should be removed
    std::vector<char32_t> expected = {};
    EXPECT_EQ(text2, expected);
}

TEST(SanitizeTests, NoTags)
{
    TagCharSanitizer tag_char_sanitizer;
    std::vector<char32_t> text3 = {'h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd'};
    tag_char_sanitizer.sanitize(text3);

    // Should remain unchanged
    std::vector<char32_t> expected = {'h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd'};
    EXPECT_EQ(text3, expected);
}

TEST(SanitizeTests, TooLongTagSequence)
{
    TagCharSanitizer tag_char_sanitizer;
    std::vector<char32_t> text4 = {0x1F3F4};
    for (int i = 0; i < 33; i++) // 33 > MAX_TAG_LENGTH
        text4.push_back(0xE0000 + 'a');
    text4.push_back(0xE007F);

    tag_char_sanitizer.sanitize(text4);

    // Excessively long tag sequence should be removed
    std::vector<char32_t> expected = {};
    EXPECT_EQ(text4, expected);
}