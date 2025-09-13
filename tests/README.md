# SILA System - Testing Guide

This document provides an overview of the testing infrastructure and guidelines for the SILA System project.

## Table of Contents
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Environment](#test-environment)
- [Writing Tests](#writing-tests)
- [Credential Policy](#credential-policy)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)

## Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Global pytest configuration and fixtures
├── test_config.py        # Test configuration and constants
├── test_utils/           # Shared test utilities
│   ├── __init__.py
│   └── test_db.py        # Database testing utilities
└── modules/              # Module-specific tests
    └── [module_name]/
        └── test_*.py     # Test files
```

## Test Reporting

### Local Test Reports

When you run tests locally, several types of reports are generated in the `reports/` directory:

- `reports/coverage/` - HTML coverage report (open `index.html` in a browser)
- `reports/coverage.xml` - Coverage data in XML format (for CI tools)
- `reports/junit.xml` - Test results in JUnit format
- `reports/pytest-report.html` - Interactive HTML test report

### Viewing Reports

1. **Coverage Report**:
   ```bash
   # Generate and open coverage report
   make coverage
   # Or manually open in default browser
   open reports/coverage/index.html  # macOS
   start reports/coverage/index.html # Windows
   xdg-open reports/coverage/index.html  # Linux
   ```

2. **Test Results**:
   ```bash
   # Generate and open HTML test report
   python -m pytest --html=reports/pytest-report.html --self-contained-html
   open reports/pytest-report.html  # macOS
   ```

### CI Integration

The CI pipeline generates and archives test reports. You can find them in the GitHub Actions artifacts after a run:

1. Go to the Actions tab in GitHub
2. Select the workflow run
3. Look for the "Artifacts" section to download test reports

### Code Coverage

Code coverage is enforced at 80% minimum. The CI will fail if coverage drops below this threshold.

To check coverage locally:
```bash
# Run tests with coverage
make coverage

# Check coverage in terminal
coverage report -m
```

### Test Badges

Add these badges to your README.md:

```markdown
![Tests](https://github.com/your-org/sila-system/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/your-org/sila-system)
```

### Advanced Reporting

For more detailed analysis, you can use the following tools:

1. **Coverage.py**:
   ```bash
   # Generate detailed coverage report
   coverage html --show-contexts
   ```

2. **Pytest Options**:
   ```bash
   # Show slowest tests
   pytest --durations=10 -v
   
   # Run only failed tests
   pytest --last-failed
   
   # Run tests matching a pattern
   pytest -k "test_user"
   ```

## Running Tests

### Prerequisites
- Python 3.11+
- PostgreSQL (for local testing)
- Docker (for containerized testing)

### Local Testing

1. Install test dependencies:
   ```bash
   pip install -r requirements-test.txt
   ```

2. Run all tests:
   ```bash
   make test
   ```

3. Run specific test file:
   ```bash
   make test-file file=tests/test_example.py
   ```

4. Run tests with coverage:
   ```bash
   make coverage
   ```

### Docker Testing

Run tests in an isolated Docker environment:

```bash
make test-docker
```

This will:
1. Build the test environment
2. Start required services (PostgreSQL, MailHog)
3. Run all tests
4. Generate coverage reports

## Test Environment

The test environment includes:
- **PostgreSQL**: Test database
- **MailHog**: Fake SMTP server for email testing
- **Environment Variables**: Loaded from `.env.test` (see `.env.test.example`)

## Writing Tests

### Test Organization
- Group related tests in classes
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

### Example Test

```python
def test_user_creation(client, db_session):
    # Arrange
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    # Act
    response = client.post("/api/users/", json=user_data)
    
    # Assert
    assert response.status_code == 201
    assert "id" in response.json()
```

### Fixtures

Common fixtures available in `conftest.py`:
- `client`: Test client for making HTTP requests
- `db_session`: Database session with automatic rollback
- `auth_headers`: Authentication headers for protected routes

## Credential Policy

### Allowed Credentials
- **Database**:
  - Username: `postgres`
  - Password: `Truman1_Marcelo1_1985`
  - Database: `postgres`
  - Host: `localhost`
  - Port: `5432`
- **SMTP**:
  - Username: `postgres`
  - Password: `Truman1_Marcelo1_1985`

### Enforcement
- Pre-commit hook checks for credential violations
- CI pipeline fails on any violation
- Automatic scanning of all files in the repository

## CI/CD Integration

The CI pipeline includes:
1. Credential policy check
2. Code style and quality checks
3. Unit and integration tests
4. Security scanning
5. Test coverage reporting

## Best Practices

1. **Isolation**: Each test should be independent
2. **Speed**: Keep tests fast (use mocks for external services)
3. **Readability**: Clear test names and assertions
4. **Coverage**: Aim for high test coverage (minimum 80%)
5. **Documentation**: Document test cases and assumptions

## Troubleshooting

### Common Issues

**Database connection issues**
- Ensure PostgreSQL is running
- Check `.env.test` configuration

**Test failures**
- Run tests with `-v` for verbose output
- Check for database migrations

**Credential policy violations**
- Use only allowed credentials
- Check for hardcoded values in test data

## License

This project is licensed under the terms of the MIT license.
