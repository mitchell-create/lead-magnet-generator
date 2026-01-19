#!/usr/bin/env python
"""
Test script to check Python version and library compatibility
"""
import sys

def test_import(module_name):
    """Test if a module can be imported."""
    try:
        __import__(module_name)
        return True, "OK"
    except Exception as e:
        return False, f"FAIL: {str(e)[:50]}"

print("=" * 60)
print("Python Version Check")
print("=" * 60)
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print()

print("Testing Core Libraries:")
print("-" * 60)

libraries = [
    ("slack_bolt", "Slack integration"),
    ("flask", "Flask web server"),
    ("requests", "HTTP requests"),
    ("openai", "OpenAI/OpenRouter API"),
    ("supabase", "Supabase database"),
    ("dotenv", "Environment variables"),
]

results = []
for lib, desc in libraries:
    success, message = test_import(lib)
    status = "[OK]" if success else "[FAIL]"
    print(f"{status} {lib:15} ({desc})")
    if not success:
        print(f"      Error: {message}")
    results.append((lib, success))

print()
print("=" * 60)
print("Summary")
print("=" * 60)

all_passed = all(result[1] for result in results)
if all_passed:
    print("[SUCCESS] All libraries imported successfully!")
    print("[SUCCESS] Your Python version is compatible")
else:
    print("[WARNING] Some libraries failed to import")
    print()
    print("Failed libraries:")
    for lib, success in results:
        if not success:
            print(f"  - {lib}")
    print()
    print("Recommendation: Install Python 3.12 for full compatibility")
    print("See INSTALL_PYTHON312.md for instructions")

print("=" * 60)
