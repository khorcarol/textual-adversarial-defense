#include "invisible.h"
#include <algorithm>
#include <unordered_set>

static const std::unordered_set<char32_t> INVISIBLE_CPS = {
    0x200B, 0x200C, 0x200D, 0x200E, 0x200F,
    0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
    0x2060, 0xFEFF};

void InvisibleCharSanitizer::sanitize(std::vector<char32_t> &input)
{
    input.erase(std::remove_if(input.begin(), input.end(),
                               [](char32_t cp)
                               { return INVISIBLE_CPS.count(cp); }),
                input.end());
}
