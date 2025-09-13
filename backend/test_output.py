# Test script to check basic Python output
import sys

def main():
    print("Standard output test")
    print("This should appear in the console")
    sys.stdout.write("Direct stdout write test\n")
    sys.stderr.write("Direct stderr write test\n")
    
    # Try writing to a file
    try:
        with open("output_test.txt", "w") as f:
            f.write("This is a test file. If you see this, the script ran successfully.\n")
        print("Test file created: output_test.txt")
    except Exception as e:
        print(f"Error writing to file: {e}")
    
    print("Script completed successfully")

if __name__ == "__main__":
    main()
