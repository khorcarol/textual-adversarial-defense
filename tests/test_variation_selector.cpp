#include <gtest/gtest.h>
#include "variation_selector.h"

TEST(SanitizeTests, ValidVariationSequence)
{
    VariationSelectorSanitizer variation_selector_sanitizer;
    std::vector<char32_t> text = {
        0x0023, 0xFE0F};

    variation_selector_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {
        0x0023, 0xFE0F};

    EXPECT_EQ(text, expected);
}

TEST(SanitizeTests, InvalidVariationSequence)
{
    VariationSelectorSanitizer variation_selector_sanitizer;
    std::vector<char32_t> text = {
        0x0001, 0xFE0F, 0xE01EF};

    variation_selector_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {
        0x0001};

    EXPECT_EQ(text, expected);
}