#pragma once

#include <filesystem>
#include <string>
#include <cstdlib>

namespace resources {

/**
 * Get the path to a resource file in the package.
 * Works for both wheel installations and local development.
 * 
 * @param relative_path Path relative to utils/, e.g., "homoglyphs/intentional.json"
 * @return Absolute filesystem path to the resource
 */
inline std::filesystem::path get_resource_path(const std::string &relative_path)
{
    // First, try environment variable (can be set by Python)
    const char *resources_env = std::getenv("TEXTUAL_DEFENSE_RESOURCES");
    if (resources_env)
    {
        std::filesystem::path resource_path(resources_env);
        resource_path /= relative_path;
        if (std::filesystem::exists(resource_path))
        {
            return resource_path;
        }
    }

    // Second, try relative to the source directory (local development)
    std::filesystem::path source_dir = std::filesystem::path(__FILE__).parent_path().parent_path();
    std::filesystem::path local_path = source_dir / "utils" / relative_path;
    if (std::filesystem::exists(local_path))
    {
        return local_path;
    }

    // Last resort: assume utils is in the current working directory or parent
    std::filesystem::path cwd_path = std::filesystem::current_path() / "utils" / relative_path;
    if (std::filesystem::exists(cwd_path))
    {
        return cwd_path;
    }

    // Return the local path even if it doesn't exist (will fail with clear error)
    return local_path;
}

} // namespace resources
