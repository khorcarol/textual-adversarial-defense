#include <iostream>
#include <memory>
#include <cassert>

#include "core/pipeline.h"
#include "modules/bidi.h"
#include "utils.h"

int main()
{
    Pipeline p;
    p.addModule(std::make_unique<BidiCharSanitizer>());

    std::string with_reorderings = u8"Hello \u202EWorld \u202C";
    std::string cleaned = p.sanitize(with_reorderings);

    std::cout << "Before: " << with_reorderings << "\n";
    std::cout << "After : " << cleaned << "\n";
    return 0;
}
