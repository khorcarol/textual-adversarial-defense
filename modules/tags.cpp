#include "tags.h"
#include <cstddef>
#include <unordered_set>
#include <string>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <nlohmann/json.hpp>


void parse_set(std::filesystem::path json_path, std::unordered_set<std::string> &valid_sequences)
{
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

    for (auto &value : j)
    {
        // Convert hex string to integer (code point)
        std::string tag = value.get<std::string>();
        valid_sequences.insert(tag);
    }
}
TagCharSanitizer::TagCharSanitizer()
{
    std::filesystem::path source_dir = std::filesystem::path(__FILE__).parent_path().parent_path();
    std::filesystem::path json_path_1 = source_dir / "utils" / "tags" /"region_subtags.json";
    std::filesystem::path json_path_2 = source_dir / "utils" / "tags" / "subdivision_ids.json";

    parse_set(json_path_1, valid_sequences);
    parse_set(json_path_2, valid_sequences);
}



void TagCharSanitizer::sanitize(std::vector<char32_t> & text)
{

    constexpr char32_t TAG_BASE = 0x1F3F4; // 🏴
    constexpr char32_t TAG_END = 0xE007F;
    constexpr char32_t TAG_START = 0xE0000;
    constexpr size_t MAX_TAG_LENGTH = 32;

    std::vector<char32_t> result;
    std::vector<int> base_positions;

    for (int i = 0; i < text.size(); i++)
    {
        char32_t cp = text[i];
        if (cp == TAG_BASE)
        {
            base_positions.push_back(i);
            result.push_back(cp);
        }
        else if (cp == TAG_END)
        {
            if (!base_positions.empty())
            {
                int base_pos = base_positions.back();
                base_positions.pop_back();

                // Exceeds valid tag length 
                if (i - base_pos - 1 > MAX_TAG_LENGTH)
                {
                    result.resize(base_pos);
                    continue;
                }

                // Extract tag sequence
                std::string tag_sequence;
                for (int j = base_pos + 1; j < i; j++)
                {
                    char32_t tag_cp = text[j];
                    tag_sequence += static_cast<char>(tag_cp - TAG_START);
                }

                // Not a valid sequence
                if (valid_sequences.count(tag_sequence) == 0)
                {
                    result.resize(base_pos);
                    continue;
                }
                result.push_back(cp);
            }
        }
        else if (cp >= TAG_START && cp <= TAG_END)
        {
            // Remove tag characters that are outside a tag sequence
            if (base_positions.empty())
            {
                continue;
            }
            else
            {
                result.push_back(cp);
            }
        }

        else
        {
            result.push_back(cp);
        }
    }
    text = std::move(result);
}
