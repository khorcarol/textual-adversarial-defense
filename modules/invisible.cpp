#include "invisible.h"
#include <algorithm>
#include <unordered_set>


InvisibleCharSanitizer::InvisibleCharSanitizer(){
    invisible_codepoints = {
        0x200B, 0x200C, 0x200D, 0xFEFF, //zero-widths
        0x200E, 0x200F, //bidi 
        0x202A, 0x202B, 0x202C, 0x202D, 0x202E, //bidi
        0x2060, //wordjoiner
        0x2066, 0x2067,0x2068, 0x2069}; //bidi
}
void InvisibleCharSanitizer::sanitize(std::vector<char32_t> &input)
{
    // C++ 20 erase_if to remove invisible characters
    std::erase_if(input,
                  [this](char32_t cp)
                  { return (this->invisible_codepoints).count(cp); });
}
