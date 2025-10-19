#include <iostream>
#include <memory>
#include <cassert>

#include "core/pipeline.h"
#include "modules/invisible.h"

int main()
{
    Pipeline p;
    p.addModule(std::make_unique<InvisibleCharSanitizer>());

    // Input: "a<ZWSP>b" where ZWSP is U+200B encoded in UTF-8: 0xE2 0x80 0x8B
    std::string with_invisible = u8"a\u200Bb";
    std::string cleaned = p.sanitize(with_invisible);

    std::cout << "Input (hex): ";
    for (unsigned char c : with_invisible)
        std::cout << std::hex << (int)c << ' ';
    std::cout << std::dec << "\n";

    std::cout << "Ouput (hex): ";
    for (unsigned char c : cleaned)
        std::cout << std::hex << (int)c << ' ';
    std::cout << std::dec << "\n";
    
    assert(cleaned == "ab");

    std::cout << "Test passed\n";
    return 0;
}
