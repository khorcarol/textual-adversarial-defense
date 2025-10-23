#pragma once
#include "sanitizer.h"
#include <vector>

class InvisibleCharSanitizer : public Sanitizer
{
public:
    void sanitize(std::vector<char32_t> &input) override;
};

