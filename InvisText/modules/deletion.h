#pragma once
#include "sanitizer.h"
#include <vector>

class DeletionCharSanitizer : public Sanitizer
{
private:
    char32_t deletion_char;

public:
    DeletionCharSanitizer();
    void sanitize(std::vector<char32_t> &input) override;
};

