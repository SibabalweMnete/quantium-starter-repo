#!/bin/bash

# Activate the virtual environment
source venv/Scripts/activate

# Execute the test suite
python -m pytest tests/test_app.py -v

# Capture the exit code
exit_code=$?

# Return the exit code (0 if all tests passed, 1 if something went wrong)
exit $exit_code
