#!/bin/bash
# AI Workspace — Unix quick install
set -e
echo "Installing dependencies..."
pip install watchdog plyer
echo "Running setup wizard..."
python init.py
