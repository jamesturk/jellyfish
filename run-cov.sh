#!/bin/sh

export PYTHONPATH=.;
pip install -e .
py.test jellyfish/test.py --cov jellyfish --cov-report html
