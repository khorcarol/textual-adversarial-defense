#include "variation_selector.h"
#include "resources.h"
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <array>
#include <memory>
#include <cstdio>
#include <filesystem>
#include <fstream>
#include <nlohmann/json.hpp>
#include <algorithm>

VariationSelectorSanitizer::VariationSelectorSanitizer(){
    // Variation Selectors (U+FE00 to U+FE0F)
    for (char32_t cp = 0xFE00; cp <= 0xFE0F; ++cp) {
        variation_selectors.insert(cp);
    }

    // Variation Selectors Supplement (U+E0100 to U+E01EF)
    for (char32_t cp = 0xE0100; cp <= 0xE01EF; ++cp) {
        variation_selectors.insert(cp);
    }
    
    std::filesystem::path json_path = resources::get_resource_path("variation_selector/variation_selector.json");
    std::ifstream f(json_path);

    if (!f.is_open())
    {
        std::cerr << "Error: Could not open " << json_path << std::endl;
        throw std::runtime_error("Failed to open json");
    }

    nlohmann::json j;
    try
    {
        f >> j;
    }
    catch (const nlohmann::json::parse_error &e)
    {
        std::cerr << "JSON parse error: " << e.what() << std::endl;
        throw;
    }

    for (auto &[key, value] : j.items())
    {
        // Convert hex string to integer (code point)
        char32_t src = static_cast<char32_t>(std::stoul(key, nullptr, 16));
        for (const auto &cp : value)
        {
            char32_t dst = static_cast<char32_t>(std::stoul(cp.get<std::string>(), nullptr, 16));
            allowed_previous_variations[src].push_back(dst);
        }        
    }
}


void VariationSelectorSanitizer::sanitize(std::vector<char32_t> &input)
{
    std::vector<char32_t> res; // copy original order
    for (size_t i = 0; i < input.size(); ++i)
    {
        char32_t cp = input[i];
        // Check if cp is a variation selector
        if (variation_selectors.find(cp) != variation_selectors.end())
        {
            // If it is not the first character and previous character is allowed, add it
            if (i != 0 &&
                std::find(allowed_previous_variations[cp].begin(),
                          allowed_previous_variations[cp].end(),
                          input[i - 1]) != allowed_previous_variations[cp].end())
            {
                res.push_back(cp);
            }
            else{
                continue;
            }
        }
        else{res.push_back(cp);}
    }
    input = std::move(res);
}

// int main()
// {
//     VariationSelectorSanitizer sanitizer;
//     std::vector<char32_t> text = {0x1312f, 0xfe06};
//     sanitizer.sanitize(text);

//     for (char32_t cp : text)
//     {
//         std::cout << std::hex << static_cast<uint32_t>(cp) << '\n';
//     }
//     std::cout << std::endl;

//     std::vector<char32_t> text2 = {0x1312, 0xfe06};
//     sanitizer.sanitize(text2);

//     for (char32_t cp : text2)
//     {
//         std::cout << std::hex << static_cast<uint32_t>(cp) << '\n';
//     }
//     std::cout << std::endl;
// }