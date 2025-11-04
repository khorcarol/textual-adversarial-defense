#include "homoglyph.h"
#include <unordered_map>
#include <cstdint>
#include <iostream>
#include <nlohmann/json.hpp>
#include <fstream>
#include <vector>
#include <sstream>
#include <filesystem>


// HomoglyphSanitizer::HomoglyphSanitizer()
// {
//     // Gets path to confusables.json relative to source file
//     std::filesystem::path source_dir = std::filesystem::path(__FILE__).parent_path().parent_path();
//     std::filesystem::path json_path = source_dir / "utils" / "confusables.json";
//     std::ifstream f(json_path);
    
//     if (!f.is_open())
//     {
//         std::cerr << "Error: Could not open " << json_path << std::endl;
//         throw std::runtime_error("Failed to open confusables.json");
//     }

//     nlohmann::json j;
//     try
//     {
//         f >> j;
//     }
//     catch (const nlohmann::json::parse_error &e)
//     {
//         std::cerr << "JSON parse error: " << e.what() << std::endl;
//         throw;
//     }

//     for (auto &[key, value] : j.items())
//     {
//         // Convert hex string to integer (code point)
//         char32_t src = static_cast<char32_t>(std::stoul(key, nullptr, 16));
//         std::string dst = value.get<std::string>();

//         std::istringstream iss(dst);
//         std::string hex_part;
//         std::vector<char32_t> dst_seq;

//         // Handle mapping to two or more characters
//         while (iss >> hex_part)
//         {
//             dst_seq.push_back(static_cast<char32_t>(std::stoul(hex_part, nullptr, 16)));
//         }

//         homoglyph_map[src] = dst_seq;
//     }
// }

void HomoglyphSanitizer::sanitize(std::vector<char32_t> &input)
{

    // New vector since some mappings may expand to multiple code points
    std::vector<char32_t> output;
    for (auto &cp : input)
    {
        auto it = homoglyph_map.find(cp);
        if (it != homoglyph_map.end())
        {
            output.insert(output.end(), it->second.begin(), it->second.end());
        }
        else
        {
            output.push_back(cp);
        }
    }
    input = std::move(output);
}

int main()
{
    HomoglyphSanitizer sanitizer;
    std::vector<char32_t> text = {0x0430, 0x03B1, 0xFF41, 0x0062}; // 'а', 'α', 'ａ', 'b'
    sanitizer.sanitize(text);

    for (char32_t cp : text)
    {
        std::cout << std::hex << static_cast<uint32_t>(cp) << " "; // Should print: 61 61 61 62
    }
    std::cout << std::endl;

    return 0;
}