#include "variation_selector.h"
#include <iostream>

VariationSelectorSanitizer::VariationSelectorSanitizer()
{
    // Example:
    allowed_previous_variations[0x3] = {0x1};
    allowed_previous_variations[0x2] = {0x1};
    allowed_previous_variations[0x1] = {};
}

void VariationSelectorSanitizer::sanitize(std::vector<char32_t> &input)
{
    std::vector<char32_t> res; // copy original order
    for (size_t i = 0; i < input.size(); ++i)
    {
        char32_t cp = input[i];
        // Check if cp is a variation selector
        if (allowed_previous_variations.find(cp) != allowed_previous_variations.end())
        {
            // If it's the first character or previous character not allowed, skip it
            if (i == 0 || 
                std::find(allowed_previous_variations[cp].begin(),
                          allowed_previous_variations[cp].end(),
                          input[i - 1]) == allowed_previous_variations[cp].end())
            {
                continue; // skip this variation selector
            }
        }
        res.push_back(cp);
    }
    input = std::move(res);
}

// int main()
// {
//     VariationSelectorSanitizer sanitizer;
//     std::vector<char32_t> text = {0x1, 0x2, 0x3};
//     sanitizer.sanitize(text);

//     for (char32_t cp : text)
//     {
//         std::cout << std::hex << static_cast<uint32_t>(cp) << '\n';
//     }
//     std::cout << std::endl;
// }