#!/bin/bash

# Script to check if the home directory is being committed
# This is a safety measure to prevent accidental recreation of the problematic home directory

# Check if home directory exists and doesn't contain just .gitkeep
if [ -d "home" ] && [ "$(ls -A home | grep -v '^\.gitkeep$' | wc -l)" -gt 0 ]; then
  echo "❌ ERROR: The 'home' directory contains files and should not be committed!"
  echo "   This directory was intentionally removed and should not be recreated."
  echo "   If you need to store files, please use a different directory."
  echo "   Files found in 'home' directory:"
  ls -la home/
  exit 1
fi

exit 0

