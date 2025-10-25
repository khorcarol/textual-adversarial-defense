
#pragma once
#include "sanitizer.h"
#include <vector>

class HomoglyphSanitizer : public Sanitizer
{
public:
    void sanitize(std::vector<char32_t> &input);
};

