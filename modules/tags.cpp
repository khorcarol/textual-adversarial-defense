#include "tags.h"

#include <cstddef>
#include <unordered_set>
#include <string>
#include <iostream>

std::unordered_set<std::string> valid_sequences = {"validseq1", "validseq2"};

void TagCharSanitizer::sanitize(std::vector<char32_t> &text)
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
        else
        {
            result.push_back(cp);
        }
    }
    text = std::move(result);
}
