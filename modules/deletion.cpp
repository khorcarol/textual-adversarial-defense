#include "deletion.h"
#include <algorithm>
#include <unordered_set>

DeletionCharSanitizer::DeletionCharSanitizer()
{
    deletion_char = 0x8;
}
void DeletionCharSanitizer::sanitize(std::vector<char32_t> &input)
{
    size_t write_pos = 0;

    for (size_t read_pos = 0; read_pos < input.size(); ++read_pos)
    {
        if (input[read_pos] == deletion_char)
        {
            if (write_pos > 0)
                --write_pos; // delete previous char
        }
        else
        {
            input[write_pos++] = input[read_pos]; // keep current char
        }
    }

    input.resize(write_pos); // truncate to new length
}

// #include <iostream>
// int main()
// {
//     std::vector<char32_t> s = {0x3, 0x1, 0x2, 0x8, 0x8 , 0x9};
//     DeletionCharSanitizer d;
//     d.sanitize(s);
//     for (char32_t cp : s)
//         {
//             std::cout << std::hex << static_cast<uint32_t>(cp) << " "; // Should print: 61 61 61 62
//         }
//         std::cout << std::endl;
// }