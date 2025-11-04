
#pragma once
#include "sanitizer.h"
#include <vector>
#include <unordered_map>

class HomoglyphSanitizer : public Sanitizer
{
private:
    static const std::unordered_map<char32_t, std::vector<char32_t>> homoglyph_map;

public:
    // HomoglyphSanitizer();
    void sanitize(std::vector<char32_t> &input);
};

