#!/bin/bash
set -e

# Install Node.js dependencies if package.json exists
if [ -f package.json ]; then
  npm install --yes
fi
