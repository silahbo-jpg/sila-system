import sys
import os
import pytest

# Add the backend directory to Python path
backend_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, backend_dir)

# Print debug information
print("\n=== Python Path ===")
for path in sys.path:
    print(f"- {path}")

print("\n=== Running tests ===")

# Run the tests with detailed output
exit_code = pytest.main([
    "tests/modules/health/test_endpoints.py",
    "-v",
    "--tb=short"
])

sys.exit(exit_code)

