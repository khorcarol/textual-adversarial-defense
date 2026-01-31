python -m perf_measure.benchmarking --mode single --attack bidi --impl python
python -m perf_measure.benchmarking --mode single --attack bidi --impl cpp

python -m perf_measure.benchmarking --mode single --attack deletion --impl python
python -m perf_measure.benchmarking --mode single --attack deletion --impl cpp

python -m perf_measure.benchmarking --mode single --attack homoglyph --impl homoglyphs
python -m perf_measure.benchmarking --mode single --attack homoglyph --impl decancer
python -m perf_measure.benchmarking --mode single --attack homoglyph --impl cpp

python -m perf_measure.benchmarking --mode single --attack invisible --impl python_mcp
python -m perf_measure.benchmarking --mode single --attack invisible --impl cpp

python -m perf_measure.benchmarking --mode single --attack tag --impl python_aws
python -m perf_measure.benchmarking --mode single --attack tag --impl cpp

python -m perf_measure.benchmarking --mode single --attack variation --impl python
python -m perf_measure.benchmarking --mode single --attack variation --impl cpp
