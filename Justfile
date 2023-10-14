pytest:
    maturin develop
    .venv/bin/pytest

test: pytest
    cargo test

deploy-docs:
    . .venv/bin/activate
    mkdocs gh-deploy

venv:
    rm -rf .venv
    python3 -m venv .venv
    . .venv/bin/activate
    .venv/bin/pip install wheel pytest mkdocs-material
    .venv/bin/pip install jupyter pandas seaborn


timedruns-old:
    .venv/bin/pip install jellyfish==0.10.0 # last C version
    .venv/bin/python benchmarks/timedruns.py old > benchmarks/timedruns-old.csv

timedruns-new:
    .venv/bin/pip uninstall jellyfish
    .venv/bin/pip install -e .
    #.venv/bin/pip install --pre jellyfish # latest Rust version
    .venv/bin/python benchmarks/timedruns.py new >> benchmarks/timedruns-new.csv
