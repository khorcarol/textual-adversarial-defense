#include <iostream>
#include <memory>
#include <cassert>

#include "core/pipeline.h"
#include "modules/bidi.h"
#include "modules/invisible.h"
#include "utils.h"

int main()
{
    Pipeline p;
    p.addModule(std::make_unique<BidiCharSanitizer>());
    p.addModule(std::make_unique<InvisibleCharSanitizer>());

    std::string with_reorderings = u8"Hello \u202EWorld \u202C \u202B";
    std::string cleaned = p.sanitize(with_reorderings);

    std::cout << "Before: " << with_reorderings << "\n";
    std::cout << "After : " << cleaned << "\n";

    std::cout << "Input (hex): ";
    for (unsigned char c : with_reorderings)
        std::cout << std::hex << (int)c << ' ';
    std::cout << std::dec << "\n";

    std::cout << "Ouput (hex): ";
    for (unsigned char c : cleaned)
        std::cout << std::hex << (int)c << ' ';
    std::cout << std::dec << "\n";
    return 0;
}
