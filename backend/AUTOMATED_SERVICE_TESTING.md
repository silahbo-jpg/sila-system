# SILA Automated Service Mapping & Testing System

## Overview

This comprehensive automation system provides intelligent discovery, testing, and reporting for all API endpoints in the SILA system. It seamlessly integrates with SILA's modular architecture and automation hub to deliver professional-grade service testing capabilities.

## Features

### 🔍 Intelligent Service Discovery
- **Automatic Endpoint Detection**: Scans all 25+ FastAPI modules in `app/modules/`
- **Smart Router Analysis**: Discovers APIRouter instances and extracts endpoint metadata
- **Graceful Error Handling**: Continues operation despite module import issues
- **Comprehensive Metadata**: Captures methods, descriptions, router prefixes, and tags

### 🧪 Comprehensive Testing
- **Multi-Method Support**: Tests GET, POST, PUT, DELETE endpoints intelligently
- **Retry Logic**: Automatic retries with exponential backoff for reliability
- **Authentication Detection**: Identifies endpoints requiring authentication
- **Response Analysis**: Detailed timing, status codes, and content type analysis

### 📊 Professional Reporting
- **Interactive HTML Reports**: Beautiful, filterable reports with statistics
- **Real-time Filtering**: Filter by status (Success, Auth Required, Errors, etc.)
- **Module Breakdown**: Organized by SILA modules with endpoint details
- **Export Capabilities**: JSON configuration files for integration

### 🚀 Automation Pipeline
- **One-Click Execution**: Complete pipeline automation via batch/PowerShell scripts
- **Server Management**: Automatic server detection and startup guidance
- **Cross-Platform**: Windows batch and PowerShell script options
- **CI/CD Ready**: Scriptable for continuous integration workflows

## File Structure

```
backend/
├── scripts/
│   ├── generate_services_map.py     # Service discovery engine
│   ├── test_all_services.py         # Comprehensive testing system
│   └── README.md                    # Scripts documentation
├── reports/                         # Generated reports and backups
├── modules_services.json           # Main service configuration
├── services_test_report.html       # Latest test report
├── run_service_tests.ps1          # PowerShell automation (advanced)
├── run_service_tests_simple.ps1   # PowerShell automation (simplified)
├── run_service_tests.bat          # Batch automation (most reliable)
└── AUTOMATED_SERVICE_TESTING.md   # This documentation
```

## Usage

### Quick Start

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Run the complete pipeline**:
   ```bash
   # Using batch file (recommended for Windows)
   .\run_service_tests.bat
   
   # Using PowerShell (advanced)
   .\run_service_tests.ps1
   ```

3. **Review results**:
   - Open `services_test_report.html` in your browser
   - Check `modules_services.json` for service configuration
   - Review `reports/` directory for additional analysis

### Individual Components

#### Service Discovery Only
```bash
python scripts\generate_services_map.py
```
- Scans all modules and generates `modules_services.json`
- Creates backup and summary reports
- Preserves existing frontend mappings

#### Testing Only
```bash
python scripts\test_all_services.py
```
- Tests all discovered endpoints
- Generates HTML report with interactive features
- Updates service configuration with test results

### Advanced Options

#### PowerShell Script Options
```powershell
# Skip server startup (use existing running server)
.\run_service_tests.ps1 -SkipServerStart

# Auto-open report in browser
.\run_service_tests.ps1 -OpenReport

# Enable verbose logging
.\run_service_tests.ps1 -Verbose

# Show help
.\run_service_tests.ps1 -Help
```

## Configuration

### Service Configuration File

The `modules_services.json` file contains comprehensive service metadata:

```json
{
  "module_name": {
    "display_name": "Human Readable Name",
    "module_path": "app\\modules\\module_name",
    "total_endpoints": 10,
    "last_scanned": "2025-08-27T03:47:45.236290",
    "scan_status": "success",
    "services": [
      {
        "endpoint": "/api/endpoint-path/",
        "methods": ["GET", "POST"],
        "function_name": "endpoint_function",
        "description": "Endpoint description",
        "router_prefix": "/api",
        "router_tags": ["Module Name"],
        "frontend_admin": null,
        "frontend_citizen": null,
        "test_status": "SUCCESS",
        "last_test_result": "200 (45ms)",
        "last_test_time": "2025-08-27T03:47:45.236290"
      }
    ]
  }
}
```

### Frontend Mapping

Add frontend route mappings to connect backend endpoints with frontend components:

```json
{
  "endpoint": "/api/some-endpoint/",
  "frontend_admin": "/admin/some-page",
  "frontend_citizen": "/citizen/some-page"
}
```

## Report Features

### HTML Report Capabilities

- **Interactive Filtering**: Filter by endpoint status, module, or method
- **Sortable Tables**: Click column headers to sort results
- **Responsive Design**: Works on desktop and mobile devices
- **Export Ready**: Print-friendly CSS for documentation

### Status Categories

- **SUCCESS** ✅: Endpoint responding correctly (2xx status codes)
- **AUTH_REQUIRED** 🔐: Authentication/authorization needed (401, 403)
- **WARNING** ⚠️: Endpoint accessible but with warnings (4xx, 5xx)
- **ERROR** ❌: Network errors, timeouts, or server issues
- **SKIP** ⏭️: Endpoints requiring parameters or special handling
- **NOT_FOUND** 🔍: Endpoint not found (404)
- **VALIDATION_ERROR** 📝: Request validation issues (422, 400)

## Integration with SILA

### Module Compatibility

The system is designed to work with SILA's modular architecture:

- **25+ Modules Supported**: All modules in `app/modules/` are automatically discovered
- **Graceful Degradation**: Continues working even if some modules have issues
- **Preserves Customizations**: Frontend mappings and manual configurations are preserved
- **Version Aware**: Integrates with SILA's API versioning system

### Development Workflow

1. **Develop new endpoints** in module route files
2. **Run service discovery** to detect new endpoints
3. **Test endpoints** automatically with comprehensive coverage
4. **Review results** and fix any issues
5. **Update frontend mappings** in the configuration
6. **Integrate** with frontend applications

### CI/CD Integration

The scripts can be integrated into continuous integration workflows:

```yaml
# Example GitHub Actions workflow
- name: Test SILA Services
  run: |
    cd backend
    python scripts/generate_services_map.py
    # Start server in background
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    sleep 10
    python scripts/test_all_services.py
```

## Troubleshooting

### Common Issues

#### Import Errors
- **Symptom**: `No module named 'app.db.session'`
- **Solution**: Ensure database dependencies are installed and configured
- **Impact**: Affected modules will show 0 endpoints but system continues

#### Syntax Errors in Route Files
- **Symptom**: `invalid syntax. Perhaps you forgot a comma?`
- **Solution**: Fix syntax errors in the specific route files
- **Impact**: Affected route files are skipped but other routes in the module work

#### Server Connection Issues
- **Symptom**: `Server not responding on any known endpoints`
- **Solution**: Start the SILA server: `python -m uvicorn app.main:app --reload`
- **Impact**: Service discovery works, but testing is skipped

### Debug Mode

Enable verbose output for troubleshooting:

```bash
# PowerShell with verbose logging
.\run_service_tests.ps1 -Verbose

# Python scripts with debug output
python scripts\generate_services_map.py  # Already includes detailed output
python scripts\test_all_services.py      # Already includes progress indicators
```

### Performance Considerations

- **Large Projects**: The system handles 25+ modules efficiently
- **Rate Limiting**: Built-in delays between requests prevent server overload
- **Memory Usage**: Optimized for large endpoint collections
- **Parallel Safety**: Scripts are designed to be run sequentially for safety

## Contributing

### Adding New Features

1. **Service Discovery Enhancements**: Modify `generate_services_map.py`
2. **Testing Capabilities**: Extend `test_all_services.py`
3. **Report Features**: Update HTML generation in the testing script
4. **Automation Improvements**: Enhance the PowerShell/batch scripts

### Code Quality

- Follow existing code patterns and documentation
- Include error handling for graceful degradation
- Add progress indicators for long-running operations
- Maintain compatibility with SILA's architecture

## Support

For issues or questions regarding the automated service testing system:

1. Check the generated reports for specific error details
2. Review the troubleshooting section above
3. Examine the verbose output from the scripts
4. Consult the SILA project documentation for module-specific issues

## Version History

- **v1.0**: Initial implementation with complete service discovery and testing
- **Features**: 25+ module support, HTML reporting, automation pipeline
- **Platform**: Windows with Python 3.8+ support
- **Integration**: SILA architecture compatible

---

*This automated service testing system is part of SILA's comprehensive automation hub, designed to enhance development productivity and ensure API reliability across the entire municipal services platform.*