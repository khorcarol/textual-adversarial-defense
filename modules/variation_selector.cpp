#include "variation_selector.h"
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
    std::filesystem::path source_dir = std::filesystem::path(__FILE__).parent_path().parent_path();
    std::filesystem::path json_path = source_dir / "utils" / "variation_selector" / "variation_selector.json";
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