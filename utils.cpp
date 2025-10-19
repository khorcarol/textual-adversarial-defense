#include "utils.h"
#include <stdexcept>

namespace utils
{

    //Decode UTF-8
    std::vector<char32_t> utf8_to_codepoints(const std::string &s)
    {
        std::vector<char32_t> out;
        size_t i = 0;
        const size_t n = s.size();

        while (i < n)
        {
            unsigned char c = static_cast<unsigned char>(s[i]);
            char32_t cp = 0;
            int additional = 0;

            if (c < 0x80)
            {
                cp = c;
                additional = 0;
            }
            else if ((c & 0xE0) == 0xC0)
            {
                cp = c & 0x1F;
                additional = 1;
            }
            else if ((c & 0xF0) == 0xE0)
            {
                cp = c & 0x0F;
                additional = 2;
            }
            else if ((c & 0xF8) == 0xF0)
            {
                cp = c & 0x07;
                additional = 3;
            }
            else
                throw std::runtime_error("Invalid UTF-8 start byte");

            if (i + additional >= n)
                throw std::runtime_error("Truncated UTF-8 sequence");

            for (int j = 1; j <= additional; ++j)
            {
                unsigned char cc = static_cast<unsigned char>(s[i + j]);
                if ((cc & 0xC0) != 0x80)
                    throw std::runtime_error("Invalid UTF-8 continuation byte");
                cp = (cp << 6) | (cc & 0x3F);
            }

            out.push_back(cp);
            i += 1 + additional;
        }

        return out;
    }

    //Encode UTF-8
    std::string codepoints_to_utf8(const std::vector<char32_t> &v)
    {
        std::string out;
        out.reserve(v.size() * 2);
        for (char32_t cp : v)
        {
            if (cp <= 0x7F)
                out.push_back(static_cast<char>(cp));
            else if (cp <= 0x7FF)
            {
                out.push_back(static_cast<char>(0xC0 | ((cp >> 6) & 0x1F)));
                out.push_back(static_cast<char>(0x80 | (cp & 0x3F)));
            }
            else if (cp <= 0xFFFF)
            {
                out.push_back(static_cast<char>(0xE0 | ((cp >> 12) & 0x0F)));
                out.push_back(static_cast<char>(0x80 | ((cp >> 6) & 0x3F)));
                out.push_back(static_cast<char>(0x80 | (cp & 0x3F)));
            }
            else
            {
                out.push_back(static_cast<char>(0xF0 | ((cp >> 18) & 0x07)));
                out.push_back(static_cast<char>(0x80 | ((cp >> 12) & 0x3F)));
                out.push_back(static_cast<char>(0x80 | ((cp >> 6) & 0x3F)));
                out.push_back(static_cast<char>(0x80 | (cp & 0x3F)));
            }
        }
        return out;
    }

} 