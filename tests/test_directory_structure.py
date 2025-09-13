"""
Tests to ensure the project directory structure remains clean and correct.
"""
import os
import unittest
from pathlib import Path

class TestDirectoryStructure(unittest.TestCase):
    """Test cases for directory structure validation."""

    def test_home_directory_should_not_exist(self):
        """
        Ensure the problematic 'home' directory doesn't get recreated.
        
        This test will fail if the 'home' directory exists and contains more than just
        the .gitkeep file. This helps prevent accidental recreation of a directory
        that was intentionally removed.
        """
        home_dir = Path("home")
        
        # Check if directory exists
        if not home_dir.exists():
            return  # This is the expected state
            
        # If directory exists, check its contents
        contents = list(home_dir.glob("*"))
        gitkeep = home_dir / ".gitkeep"
        
        # Only .gitkeep is allowed
        if len(contents) == 1 and contents[0].samefile(gitkeep):
            return  # Only .gitkeep exists, which is allowed
            
        # If we get here, the directory has unexpected contents
        unexpected_files = [str(f.relative_to(home_dir)) for f in contents 
                          if not f.samefile(gitkeep)]
                          
        self.fail(
            f"The 'home' directory contains unexpected files: {unexpected_files}\n"
            "This directory was intentionally removed and should not be recreated.\n"
            "If you need to store files, please use an appropriate directory under 'storage/'."
        )

if __name__ == "__main__":
    unittest.main()

