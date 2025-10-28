#include <gtest/gtest.h>
#include "variation_selector.h"

TEST(SanitizeTests, ValidVariationSequence)
{
    VariationSelectorSanitizer variation_selector_sanitizer;
    variation_selector_sanitizer.allowed_previous_variations[0x3] = {};
    variation_selector_sanitizer.allowed_previous_variations[0x2] = {0x1};
    variation_selector_sanitizer.allowed_previous_variations[0x1] = {};

    std::vector<char32_t> text = {
        0x1, 0x2, 0x3};

    variation_selector_sanitizer.sanitize(text);

    std::vector<char32_t> expected = {
        0x2};

    EXPECT_EQ(text, expected);
}