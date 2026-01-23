#include <gtest/gtest.h>
#include "combined.h"


// Test homoglyph functionality in combined sanitizer
TEST(CombinedSanitizerTests, CombinedOneToOneMappings)
{
    CombinedSanitizer combined_sanitizer;
    std::vector<char32_t> text = {0x0391, 0x001C3, 0x0392}; 
    combined_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {0x0041, 0x0021, 0x0042}; 
    EXPECT_EQ(text, expected);
}

// No mappings present, input remains unchanged
TEST(CombinedSanitizerTests, CombinedNoMappings)
{
    CombinedSanitizer combined_sanitizer;
    std::vector<char32_t> text = {0x0062, 0x0063, 0x0064}; // 'b', 'c', 'd'
    combined_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {0x0062, 0x0063, 0x0064}; // 'b', 'c', 'd'
    EXPECT_EQ(text, expected);
}


// Test invisible characters in combined sanitizer
TEST(CombinedSanitizerTests, CombinedRemovesZeroWidthSpace)
{
    CombinedSanitizer combined_sanitizer;
    // Input: "a<ZWSP>b" where ZWSP is U+200B
    std::vector<char32_t> with_invisible = {U'a', 0x200B, U'b'};
    combined_sanitizer.sanitize(with_invisible);

    std::vector<char32_t> expected = {U'a', U'b'};

    EXPECT_EQ(with_invisible, expected);
}

TEST(CombinedSanitizerTests, CombinedPreserveCharacters)
{
    CombinedSanitizer combined_sanitizer;
    std::vector<char32_t> without_invisible = {U'a', U'b'};
    combined_sanitizer.sanitize(without_invisible);

    EXPECT_EQ(without_invisible, without_invisible);
}


// Test tags in combined sanitizer
TEST(CombinedSanitizerTests, CombinedValidTagSequence)
{
    CombinedSanitizer combined_sanitizer;

    std::vector<char32_t> text = {
        0x1F3F4,
        0xE0000 + 'g', 0xE0000 + 'b', 0xE0000 + 'e', 0xE0000 + 'n', 0xE0000 + 'g',
        0xE007F};

    combined_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {
        0x1F3F4,
        0xE0000 + 'g', 0xE0000 + 'b', 0xE0000 + 'e', 0xE0000 + 'n', 0xE0000 + 'g',
        0xE007F};

    EXPECT_EQ(text, expected);
}

TEST(CombinedSanitizerTests, CombinedTagOutsideBase)
{
    CombinedSanitizer combined_sanitizer;
    std::vector<char32_t> text2 = {
        0xE0000 + 'g', 0xE0000 + 'b', 0xE0000 + 'e', 0xE0000 + 'n', 0xE0000 + 'g'};
    combined_sanitizer.sanitize(text2);

    // Invalid tag sequence should be removed
    std::vector<char32_t> expected = {};
    EXPECT_EQ(text2, expected);
}

TEST(CombinedSanitizerTests, CombinedInvalidTagSequence)
{
    CombinedSanitizer combined_sanitizer;
    std::vector<char32_t> text2 = {
        0x1F3F4,
        0xE0000 + 'a', 0xE0000 + 'b', 0xE0000 + 'c',
        0xE007F};
    combined_sanitizer.sanitize(text2);

    // Invalid tag sequence should be removed
    std::vector<char32_t> expected = {};
    EXPECT_EQ(text2, expected);
}

TEST(CombinedSanitizerTests, CombinedNoTags)
{
    CombinedSanitizer combined_sanitizer;
    std::vector<char32_t> text3 = {'h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd'};
    combined_sanitizer.sanitize(text3);

    // Should remain unchanged
    std::vector<char32_t> expected = {'h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd'};
    EXPECT_EQ(text3, expected);
}

TEST(CombinedSanitizerTests, CombinedTooLongTagSequence)
{
    CombinedSanitizer combined_sanitizer;
    std::vector<char32_t> text4 = {0x1F3F4};
    for (int i = 0; i < 33; i++) // 33 > MAX_TAG_LENGTH
        text4.push_back(0xE0000 + 'a');
    text4.push_back(0xE007F);

    combined_sanitizer.sanitize(text4);

    // Excessively long tag sequence should be removed
    std::vector<char32_t> expected = {};
    EXPECT_EQ(text4, expected);
}

// Test variation selectors in combined sanitizer
TEST(CombinedSanitizerTests, CombinedValidVariationSequence)
{
    CombinedSanitizer combined_sanitizer;
    std::vector<char32_t> text = {
        0x0023, 0xFE0F};

    combined_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {
        0x0023, 0xFE0F};

    EXPECT_EQ(text, expected);
}

TEST(CombinedSanitizerTests, CombinedInvalidVariationSequence)
{
    CombinedSanitizer combined_sanitizer;
    std::vector<char32_t> text = {
        0x0001, 0xFE0F, 0xE01EF};

    combined_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {
        0x0001};

    EXPECT_EQ(text, expected);
}