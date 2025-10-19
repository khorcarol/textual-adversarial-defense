#include "pipeline.h"
#include "utils.h"

void Pipeline::addModule(std::unique_ptr<Sanitizer> module)
{
    modules.push_back(std::move(module));
}

std::string Pipeline::sanitize(const std::string &input)
{
    auto cps = utils::utf8_to_codepoints(input);
    for (auto &module : modules)
        module->sanitize(cps); // each module operates on std::vector<char32_t>
    return utils::codepoints_to_utf8(cps);
}