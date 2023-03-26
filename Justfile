venv:
    rm -rf .venv
    python3 -m venv .venv
    . .venv/bin/activate
    .venv/bin/pip install wheel 
    .venv/bin/pip install jupyter matplotlib pandas


timedruns:
    .venv/bin/pip install jellyfish==0.10.0 # last C version
    .venv/bin/python benchmarks/timedruns.py old > benchmarks/timedruns.csv
    .venv/bin/pip uninstall jellyfish
    .venv/bin/pip install -e .
    .venv/bin/python benchmarks/timedruns.py new >> benchmarks/timedruns.csv