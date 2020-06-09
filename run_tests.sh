#!/bin/bash

set -e

pylint pugsebot

python pugsebot/tests.py
