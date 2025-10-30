#include "variation_selector.h"
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <array>
#include <memory>
#include <cstdio>


std::string fetchURL(const std::string &url)
{
    std::array<char, 4096> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(("curl -s " + url).c_str(), "r"), pclose);
    if (!pipe)
        throw std::runtime_error("popen() failed!");
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr)
        result += buffer.data();
    return result;
}

void load_from_data(const std::string &data, std::unordered_map<char32_t, std::vector<char32_t>> &allowed_previous_variations)
{
    std::istringstream file(data);
    std::string line;

    while (std::getline(file, line))
    {
        // Skip comments or empty lines
        if (line.empty() || line[0] == '#')
            continue;

        // Remove trailing comments
        size_t hash = line.find('#');
        if (hash != std::string::npos)
            line = line.substr(0, hash);

        // Stop at semicolon
        size_t semicolon = line.find(';');
        if (semicolon == std::string::npos)
            continue;
        std::string left = line.substr(0, semicolon);

        // Extract the two hex strings (base, variation)
        std::istringstream iss(left);
        std::string base_str, variation_str;
        if (!(iss >> base_str >> variation_str))
            continue; // malformed line

        char32_t variation = static_cast<char32_t>(std::stoul(variation_str, nullptr, 16));
        char32_t base = static_cast<char32_t>(std::stoul(base_str, nullptr, 16));
        allowed_previous_variations[variation].push_back(base);
    }
}

VariationSelectorSanitizer::VariationSelectorSanitizer()
{
    loadDataOnce();
}

void VariationSelectorSanitizer::loadDataOnce(){
    if (!isDataLoaded)
    {
        std::string emoji = fetchURL("https://www.unicode.org/Public/17.0.0/ucd/emoji/emoji-variation-sequences.txt");
        std::string ivd = fetchURL("https://www.unicode.org/ivd/data/2025-07-14/IVD_Sequences.txt");
        std::string standardized_variants = fetchURL("https://www.unicode.org/Public/17.0.0/ucd/StandardizedVariants.txt");

        load_from_data(emoji, allowed_previous_variations);
        load_from_data(ivd, allowed_previous_variations);
        load_from_data(standardized_variants, allowed_previous_variations);
        isDataLoaded = true;
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