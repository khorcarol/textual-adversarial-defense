#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "core/pipeline.h"
#include "modules/invisible.h"
#include "modules/bidi.h"

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
        .def("sanitize", &Pipeline::sanitize);

    // Expose a convenience function that runs sanitize on a string
    m.def("sanitize_with_invisible", [](const std::string &s)
          {
        Pipeline p;
        p.addModule(std::make_unique<InvisibleCharSanitizer>());
        return p.sanitize(s); });
}
