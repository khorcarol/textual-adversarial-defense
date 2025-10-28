
#pragma once
#include "sanitizer.h"
#include <vector>
#include <unordered_map>


class VariationSelectorSanitizer : public Sanitizer
{

public:
    // Mapping of variation selectors to allowed preceding code points
    std::unordered_map<char32_t, std::vector<char32_t>> allowed_previous_variations;
    VariationSelectorSanitizer();
    void sanitize(std::vector<char32_t> &input);
};
