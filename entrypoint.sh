#!/bin/bash
python migrate.py
flask run --host=0.0.0.0 --port ${PORT:-5000}