#pragma once
#include "sanitizer.h"
#include <unordered_set>
#include <vector>


class TagCharSanitizer : public Sanitizer
{
private:
    std::unordered_set<std::string> valid_sequences;
public:
    TagCharSanitizer();
    void sanitize(std::vector<char32_t> &input) override;
};
