#!/bin/bash

set -e

flake8

python pugsebot/tests.py
