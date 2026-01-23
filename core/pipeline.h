#pragma once

#include <vector>
#include <memory>
#include "sanitizer.h"

class Pipeline
{
private:
    std::vector<std::unique_ptr<Sanitizer>> modules;

public:
    void addModule(std::unique_ptr<Sanitizer> module);
    std::string sanitize(const std::string &input);
};

