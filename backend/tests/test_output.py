"""Test script to check basic output functionality."""

def test_output():
    """Test that output is working."""
    print("This is a test output")
    return "Test successful"

if __name__ == "__main__":
    result = test_output()
    print(f"Test completed: {result}")
