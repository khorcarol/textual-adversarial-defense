#include "combined.h"
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <nlohmann/json.hpp>
#include <fstream>
#include <sstream>
#include <filesystem>

void CombinedSanitizer::parse_tag_set(const std::string &json_path, std::unordered_set<std::string> &valid_sequences)
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
        std::string tag = value.get<std::string>();
        valid_sequences.insert(tag);
    }
}

CombinedSanitizer::CombinedSanitizer()
{
    deletion_char = 0x8;

    // Initialize invisible codepoints
    invisible_codepoints = {
        0x200B, 0x200C, 0x200D, 0x200E, 0x200F,
        0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
        0x2060, 0xFEFF, 0x2069, 0x2066, 0x2067};

    // Initialize variation selectors
    for (char32_t cp = 0xFE00; cp <= 0xFE0F; ++cp) {
        variation_selectors.insert(cp);
    }
    for (char32_t cp = 0xE0100; cp <= 0xE01EF; ++cp) {
        variation_selectors.insert(cp);
    }

    std::filesystem::path source_dir = std::filesystem::path(__FILE__).parent_path().parent_path();

    // Load tags
    std::filesystem::path tag_path_1 = source_dir / "utils" / "tags" / "region_subtags.json";
    std::filesystem::path tag_path_2 = source_dir / "utils" / "tags" / "subdivision_ids.json";
    parse_tag_set(tag_path_1.string(), valid_tag_sequences);
    parse_tag_set(tag_path_2.string(), valid_tag_sequences);

    // Load variation selector allowlist
    std::filesystem::path vs_path = source_dir / "utils" / "variation_selector" / "variation_selector.json";
    std::ifstream vs_file(vs_path);
    if (!vs_file.is_open())
    {
        std::cerr << "Error: Could not open " << vs_path << std::endl;
        throw std::runtime_error("Failed to open json");
    }
    nlohmann::json vs_json;
    try
    {
        vs_file >> vs_json;
    }
    catch (const nlohmann::json::parse_error &e)
    {
        std::cerr << "JSON parse error: " << e.what() << std::endl;
        throw;
    }
    for (auto &[key, value] : vs_json.items())
    {
        char32_t src = static_cast<char32_t>(std::stoul(key, nullptr, 16));
        for (const auto &cp : value)
        {
            char32_t dst = static_cast<char32_t>(std::stoul(cp.get<std::string>(), nullptr, 16));
            allowed_previous_variations[src].push_back(dst);
        }
    }

    // Load homoglyph map
    std::filesystem::path homo_path = source_dir / "utils" / "homoglyphs" / "intentional.json";
    std::ifstream homo_file(homo_path);
    if (!homo_file.is_open())
    {
        std::cerr << "Error: Could not open " << homo_path << std::endl;
        throw std::runtime_error("Failed to open json");
    }
    nlohmann::json homo_json;
    try
    {
        homo_file >> homo_json;
    }
    catch (const nlohmann::json::parse_error &e)
    {
        std::cerr << "JSON parse error: " << e.what() << std::endl;
        throw;
    }
    for (auto &[key, value] : homo_json.items())
    {
        char32_t src = static_cast<char32_t>(std::stoul(key, nullptr, 16));
        std::string dst = value.get<std::string>();
        std::istringstream iss(dst);
        std::string hex_part;
        std::vector<char32_t> dst_seq;
        while (iss >> hex_part)
        {
            dst_seq.push_back(static_cast<char32_t>(std::stoul(hex_part, nullptr, 16)));
        }
        homoglyph_map[src] = dst_seq;
    }
}

void CombinedSanitizer::sanitize(std::vector<char32_t> &input)
{
    std::vector<char32_t> result;
    std::vector<size_t> tag_base_positions;

    for (size_t i = 0; i < input.size(); ++i)
    {
        char32_t cp = input[i];

        // Skip invisible characters
        if (invisible_codepoints.count(cp))
        {
            continue;
        }

        // Handle tags - TAG_BASE marker
        if (cp == TAG_BASE)
        {
            tag_base_positions.push_back(result.size());
            result.push_back(cp);
            continue;
        }

        // Handle tags - TAG_END marker
        if (cp == TAG_END)
        {
            if (!tag_base_positions.empty())
            {
                size_t base_pos = tag_base_positions.back();
                tag_base_positions.pop_back();

                // Check tag length
                if (result.size() - base_pos - 1 > MAX_TAG_LENGTH)
                {
                    result.resize(base_pos);
                    continue;
                }

                // Extract and validate tag sequence
                std::string tag_sequence;
                for (size_t j = base_pos + 1; j < result.size(); ++j)
                {
                    char32_t tag_cp = result[j];
                    tag_sequence += static_cast<char>(tag_cp - TAG_START);
                }

                if (valid_tag_sequences.count(tag_sequence) == 0)
                {
                    result.resize(base_pos);
                    continue;
                }
                result.push_back(cp);
            }
            continue;
        }

        // Skip invalid tag middle characters
        if (cp >= TAG_START && cp <= TAG_END)
        {
            if (!tag_base_positions.empty())
            {
                result.push_back(cp);
            }
            continue;
        }

        // Handle variation selectors
        if (variation_selectors.count(cp))
        {
            if (!result.empty() &&
                std::find(allowed_previous_variations[cp].begin(),
                          allowed_previous_variations[cp].end(),
                          result.back()) != allowed_previous_variations[cp].end())
            {
                result.push_back(cp);
            }
            continue;
        }

        // Handle homoglyph replacement
        auto homo_it = homoglyph_map.find(cp);
        if (homo_it != homoglyph_map.end())
        {
            for (char32_t replacement : homo_it->second)
            {
                result.push_back(replacement);
            }
        }
        else
        {
            result.push_back(cp);
        }
    }

    input = std::move(result);
}
