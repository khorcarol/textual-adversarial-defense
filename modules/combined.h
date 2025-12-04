#pragma once

#include <vector>
#include <cstdint>
#include <unordered_set>
#include <unordered_map>
#include <string>
#include "sanitizer.h"

class CombinedSanitizer: public Sanitizer
{
public:
    CombinedSanitizer();
    void sanitize(std::vector<char32_t> &input);

private:
    // Deletion
    char32_t deletion_char;

    // Invisible
    std::unordered_set<char32_t> invisible_codepoints;

    // Tags
    std::unordered_set<std::string> valid_tag_sequences;
    static constexpr char32_t TAG_BASE = 0x1F3F4;
    static constexpr char32_t TAG_END = 0xE007F;
    static constexpr char32_t TAG_START = 0xE0000;
    static constexpr size_t MAX_TAG_LENGTH = 32;

    // Variation Selector
    std::unordered_set<char32_t> variation_selectors;
    std::unordered_map<char32_t, std::vector<char32_t>> allowed_previous_variations;

    // Homoglyph
    std::unordered_map<char32_t, std::vector<char32_t>> homoglyph_map;

    // Helper methods
    void parse_tag_set(const std::string &json_path, std::unordered_set<std::string> &valid_sequences);
};
