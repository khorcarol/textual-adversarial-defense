
### Textual Adversarial Defenses
Building defenses for imperceptible textual attacks against NLP models. Work is based off https://arxiv.org/pdf/2106.09898.

#### Project Folders
- `core/` top level class definitions
- `modules/` source files for defenses
- `python/` Python bindings
- `tests/` Unit tests

#### Getting Started

To build the project, run 

`cd build && cmake .. && make && cd tests && ctest --output-on-failure `
