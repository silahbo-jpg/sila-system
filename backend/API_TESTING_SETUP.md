# API Testing Setup Instructions

## Windows/PowerShell Automated API Testing

This solution provides a complete, automated API testing workflow optimized for Windows environments.

### Files Created

1. **`scripts/test_endpoints.py`** - The testing script (PowerShell-compatible)
2. **`run_tests.ps1`** - PowerShell automation script

### Key Features

✅ **Automatic server detection** - Checks if server is already running
✅ **Auto-start capability** - Starts Uvicorn if needed  
✅ **No grep dependency** - Uses pure Python and PowerShell
✅ **Comprehensive reporting** - HTML report with success/failure counts
✅ **Error handling** - Robust error checking throughout
✅ **Windows optimized** - Designed specifically for Windows/PowerShell

### Usage

#### Option 1: One-Command Testing (Recommended)
```powershell
.\run_tests.ps1
```

#### Option 2: Manual Testing
```bash
# Start server manually (if not running)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python scripts/test_endpoints.py
```

### Prerequisites

- Python 3.9+ installed and in PATH
- Required Python packages: `requests`
- PowerShell execution policy allowing script execution

### Setup PowerShell Execution Policy (if needed)

If you get permission errors, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Expected Output

The script will:

1. ✅ Check if server is running
2. 🚀 Start server if needed  
3. 🧪 Run all endpoint tests
4. 📄 Generate a detailed HTML report
5. ✅ Provide clear success/failure status

### Output Files

- **`endpoint_report.html`** - Comprehensive test results with statistics

### Troubleshooting

**Server won't start:**
- Ensure you're in the backend directory
- Check that uvicorn is installed: `pip install uvicorn`
- Verify app.main:app exists and is accessible

**Permission errors:**
- Run PowerShell as Administrator
- Set execution policy as shown above

**Import errors:**
- Ensure requests is installed: `pip install requests`
- Check Python version compatibility

### Integration with Existing Workflow

This solution integrates seamlessly with the existing SILA system:
- Uses the same FastAPI application structure
- Leverages existing OpenAPI documentation
- Compatible with current development workflow
- No changes required to existing code