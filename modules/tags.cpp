#include <vector>
#include <cstddef>
#include <unordered_set>
#include <string>
#include <iostream>

std::unordered_set<std::string> valid_sequences = {"validseq1", "validseq2"};

void sanitize(std::vector<char32_t> &text)
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
        }
        else if (cp == TAG_END)
        {
            if (!base_positions.empty())
            {
                int base_pos = base_positions.back();
                base_positions.pop_back();

                // Length check
                if (i - base_pos - 1 > MAX_TAG_LENGTH){
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

                if (valid_sequences.count(tag_sequence) == 0)
                {
                    result.resize(base_pos);
                }
            }
        }
        else
        {
            result.push_back(cp);
        }
    }
    text = std::move(result);
}

int main()
{
    std::vector<char32_t> text = {
        0x1F3F4,
        0xE0000 + 'v', 0xE0000 + 'a', 0xE0000 + 'l', 0xE0000 + 'i', 0xE0000 + 'd',
        0xE0000 + 's', 0xE0000 + 'e', 0xE0000 + 'q', 0xE0000 + '1',
        0xE007F};
    sanitize(text);
    for (char32_t cp : text)
    {
        std::cout << std::hex << cp << " ";
    }
    std::cout << std::endl;

    std::vector<char32_t> text2 = {
        0x1F3F4,
        0xE0000 + 'a', 0xE0000 + 'b', 0xE0000 + 'c',
        0xE007F};
    sanitize(text2);
    for (char32_t cp : text2)
    {
        std::cout << std::hex << cp << " ";
    }
    std::cout << std::endl;

    std::vector<char32_t> text3 = {
        'h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd'};
    sanitize(text3);
    for (char32_t cp : text3)
    {
        std::cout << std::hex << cp << " ";
    }
    std::cout << std::endl;

    // test case for length of tag sequence > MAX_TAG_LENGTH
    std::vector<char32_t> text4 = {
        0x1F3F4};
    for (int i = 0; i < 33; i++) // 33 > MAX_TAG_LENGTH
    {
        text4.push_back(0xE0000 + 'a'); // arbitrary tag characters 
    }
    text4.push_back(0xE007F);
    sanitize(text4);
    for (char32_t cp : text3)
    {
        std::cout << std::hex << cp << " ";
    }
    std::cout << std::endl;
}