#!/usr/bin/env bash
set -e

pytest --cov=pyworks_generator --cov-report term-missing tests

