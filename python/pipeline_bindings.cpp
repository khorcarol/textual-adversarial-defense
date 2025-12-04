#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "core/pipeline.h"
#include "modules/invisible.h"
#include "modules/bidi.h"
#include "modules/tags.h"
#include "modules/homoglyph.h"
#include "modules/variation_selector.h"
#include "modules/deletion.h"
#include "modules/combined.h"

namespace py = pybind11;

PYBIND11_MODULE(_pipeline, m)
{
    m.doc() = "Bindings for Pipeline and sanitizers";

    py::class_<Pipeline>(m, "Pipeline")
        .def(py::init<>())
        .def("add_invisible_sanitizer", [](Pipeline &p)
             { p.addModule(std::make_unique<InvisibleCharSanitizer>()); })
        .def("add_bidi_sanitizer", [](Pipeline &p)
             { p.addModule(std::make_unique<BidiCharSanitizer>()); })
        .def("add_tag_sanitizer", [](Pipeline &p)
             { p.addModule(std::make_unique<TagCharSanitizer>()); })
        .def("add_homoglyph_sanitizer", [](Pipeline &p)
             { p.addModule(std::make_unique<HomoglyphSanitizer>()); })
        .def("add_variation_selector_sanitizer", [](Pipeline &p)
             { p.addModule(std::make_unique<VariationSelectorSanitizer>()); })
        .def("add_deletion_sanitizer", [](Pipeline &p)
             { p.addModule(std::make_unique<DeletionCharSanitizer>()); })
        .def("add_combined_sanitizer", [](Pipeline &p)
             { p.addModule(std::make_unique<CombinedSanitizer>()); })
        .def("sanitize", &Pipeline::sanitize);

    // Expose a convenience function that runs sanitize on a string
    m.def("sanitize_with_invisible", [](const std::string &s)
          {
        Pipeline p;
        p.addModule(std::make_unique<InvisibleCharSanitizer>());
        return p.sanitize(s); });
}
