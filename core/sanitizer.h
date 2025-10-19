
#ifndef SANITIZER_H
#define SANITIZER_H

#include <string>
#include <vector>

class Sanitizer
{
public:
    virtual void sanitize(std::vector<char32_t> &input) = 0;
    virtual ~Sanitizer() = default;
};

#endif // SANITIZER_H
