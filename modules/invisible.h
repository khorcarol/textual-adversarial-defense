#pragma once
#include "sanitizer.h"
#include <vector>
#include <unordered_set>

class InvisibleCharSanitizer : public Sanitizer
{
private:
    std::unordered_set<char32_t> invisible_codepoints;

public:
    InvisibleCharSanitizer();
    void sanitize(std::vector<char32_t> &input) override;
};

