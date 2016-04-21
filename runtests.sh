#!/bin/bash
py.test tests/test_metadata.py --doctest-modules -v
cd src
python python_serpent_test.py
cd ..
