def check_package(name):
    try:
        module = __import__(name)
        version = getattr(module, '__version__', 'version not found')
        print(f"[OK] {name} is installed (version: {version}).")
        return True
    except ImportError:
        print(f"[X] {name} is NOT installed or has issues.")
        return False

def main():
    print("=== Checking virtual environment ===\n")
    packages = ["pydantic", "fastapi", "pytest", "prisma"]
    results = {pkg: check_package(pkg) for pkg in packages}
    
    if all(results.values()):
        print("\n[SUCCESS] All required packages are installed and working!")
    else:
        missing = [pkg for pkg, present in results.items() if not present]
        print(f"\n[ERROR] Missing packages: {', '.join(missing)}")
        print("Please install them using: pip install " + " ".join(missing))

if __name__ == "__main__":
    main()

