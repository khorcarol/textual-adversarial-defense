#include "homoglyph.h"
#include <unordered_map>
#include <cstdint>
#include <iostream>
#include <nlohmann/json.hpp>
#include <fstream>

void HomoglyphSanitizer::sanitize(std::vector<char32_t> &input)
{
    std::ifstream f("utils/confusables.json");
    nlohmann::json j;
    f >> j;
    std::unordered_map<char32_t, char32_t> homoglyph_map;

    // TODO: Handle mapping to two or more characters
    for (auto &[key, value] : j.items())
    {
        // Convert hex string to integer (code point)
        char32_t src = static_cast<char32_t>(std::stoul(key, nullptr, 16));
        char32_t dst = static_cast<char32_t>(std::stoul(value.get<std::string>(), nullptr, 16));

        homoglyph_map[src] = dst;
    }
    
    for (auto &cp : input)
    {
        auto it = homoglyph_map.find(cp);
        if (it != homoglyph_map.end())
        {
            std::cout << "Replacing U+" << std::hex << cp << " with U+" << it->second << std::dec << std::endl;
            cp = it->second; // Replace with the mapped character
        }
    }
}

int main()
{
    HomoglyphSanitizer sanitizer;
    std::vector<char32_t> text = {0x0430, 0x03B1, 0xFF41, 0x0062}; // 'а', 'α', 'ａ', 'b'
    sanitizer.sanitize(text);

    for (char32_t cp : text)
    {
        std::cout << std::hex << cp << " "; // Should print: 61 61 61 62
    }
    std::cout << std::endl;

    return 0;
}