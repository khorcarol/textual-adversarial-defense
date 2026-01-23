#pragma once

#include <string>
#include <vector>

class Sanitizer
{
public:
    virtual void sanitize(std::vector<char32_t> &input) = 0;
    virtual ~Sanitizer() = default;
};

