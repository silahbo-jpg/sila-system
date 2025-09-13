#!/usr/bin/env python3
"""
Test runner script for SILA System.

This script provides a consistent way to run tests with proper configuration
and reporting. It can be used both locally and in CI environments.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Project directories
BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "reports"
COVERAGE_DIR = REPORTS_DIR / "coverage"
JUNIT_XML = REPORTS_DIR / "junit.xml"
COVERAGE_JSON = COVERAGE_DIR / "coverage.json"
COVERAGE_XML = COVERAGE_DIR / "coverage.xml"
COVERAGE_HTML = COVERAGE_DIR / "html"
PYTEST_HTML = REPORTS_DIR / "pytest-report.html"


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> int:
    """Run a shell command and return the exit code."""
    print(f"\n\033[1m$ {' '.join(cmd)}\033[0m")
    result = subprocess.run(cmd, cwd=cwd or BASE_DIR)
    return result.returncode


def ensure_dirs() -> None:
    """Ensure all required directories exist."""
    for directory in [REPORTS_DIR, COVERAGE_DIR, COVERAGE_HTML]:
        directory.mkdir(parents=True, exist_ok=True)


def clean_reports() -> None:
    """Clean up previous test reports."""
    for path in [JUNIT_XML, COVERAGE_JSON, COVERAGE_XML, PYTEST_HTML]:
        if path.exists():
            path.unlink()
    
    if COVERAGE_HTML.exists():
        shutil.rmtree(COVERAGE_HTML)
    COVERAGE_HTML.mkdir(exist_ok=True)


def run_tests(
    test_paths: List[str] = None,
    markers: List[str] = None,
    parallel: bool = True,
    verbose: bool = False,
    fail_fast: bool = False,
    coverage: bool = True,
) -> int:
    """Run tests with the given options."""
    cmd = [
        sys.executable,
        "-m", "pytest",
        "--strict-markers",
        "--durations=10",
    ]

    if verbose:
        cmd.append("-v")
    
    if fail_fast:
        cmd.append("-x")
    
    if parallel:
        cmd.extend(["-n", "auto"])
    
    if markers:
        cmd.extend(["-m", " and ".join(markers)])
    
    if coverage:
        cmd.extend([
            "--cov=app",
            f"--cov-report=term-missing:skip-covered",
            f"--cov-report=xml:{COVERAGE_XML}",
            f"--cov-report=html:{COVERAGE_HTML}",
            f"--cov-report=json:{COVERAGE_JSON}",
        ])
    
    # Add test paths if specified, otherwise run all tests
    if test_paths:
        cmd.extend(test_paths)
    else:
        cmd.append("tests")
    
    return run_command(cmd)


def generate_coverage_badge() -> None:
    """Generate a coverage badge using pybadges."""
    try:
        import pybadges
        
        with open(COVERAGE_JSON, 'r') as f:
            coverage_data = json.load(f)
        
        total = coverage_data['totals']['percent_covered']
        color = 'success' if total >= 80 else 'important' if total >= 70 else 'critical'
        
        badge = pybadges.badge(
            left_text='coverage',
            right_text=f'{total:.1f}%',
            right_color=color,
        )
        
        with open(REPORTS_DIR / 'coverage.svg', 'w') as f:
            f.write(badge)
            
    except ImportError:
        print("pybadges not installed, skipping badge generation")
    except Exception as e:
        print(f"Error generating coverage badge: {e}")


def main() -> int:
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Run SILA System tests")
    parser.add_argument(
        "test_paths", nargs="*", default=[],
        help="Specific test files or directories to run"
    )
    parser.add_argument(
        "-m", "--marker", action="append", default=[],
        help="Only run tests matching the given marker"
    )
    parser.add_argument(
        "--no-parallel", action="store_true",
        help="Disable parallel test execution"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Increase verbosity"
    )
    parser.add_argument(
        "-x", "--fail-fast", action="store_true",
        help="Stop after first failure"
    )
    parser.add_argument(
        "--no-coverage", action="store_true",
        help="Disable coverage reporting"
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Clean up previous reports before running"
    )
    
    args = parser.parse_args()
    
    # Setup environment
    ensure_dirs()
    if args.clean:
        clean_reports()
    
    # Run tests
    exit_code = run_tests(
        test_paths=args.test_paths,
        markers=args.marker,
        parallel=not args.no_parallel,
        verbose=args.verbose,
        fail_fast=args.fail_fast,
        coverage=not args.no_coverage,
    )
    
    # Generate coverage badge if tests passed
    if exit_code == 0 and not args.no_coverage:
        generate_coverage_badge()
    
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nTest run cancelled by user")
        sys.exit(1)
