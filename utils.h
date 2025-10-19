#include <vector>
#include <string>

namespace utils
{
    std::vector<char32_t> utf8_to_codepoints(const std::string &s);
    std::string codepoints_to_utf8(const std::vector<char32_t> &v);
}

