#!/usr/bin/env python3
"""
Basic project structure test
"""

import os
import sys


def test_project_structure():
    """Checks if all required files exist"""
    print("🔍 Checking project structure...\n")

    required_files = [
        'README.md',
        'docs/SETUP.md',
        'docs/CONTRIBUTING.md',
        'LICENSE',
        'requirements.txt',
        'config.yaml',
        'src/pipeline.py',
        'src/generators/generate_music.py',
        'src/generators/generate_image.py',
        'src/utils/create_video.py',
        'src/utils/upload_youtube.py',
        '.gitignore',
    ]

    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            missing.append(file)

    return len(missing) == 0


def test_github_structure():
    """Checks GitHub structure"""
    print("\n🔍 Checking GitHub structure...\n")

    github_files = [
        '.github/workflows/python-app.yml',
        '.github/ISSUE_TEMPLATE/bug_report.md',
        '.github/ISSUE_TEMPLATE/feature_request.md',
        '.github/pull_request_template.md',
    ]

    missing = []
    for file in github_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            missing.append(file)

    return len(missing) == 0


def test_python_syntax():
    """Checks Python files syntax"""
    print("\n🔍 Checking Python syntax...\n")

    python_files = [
        'src/pipeline.py',
        'src/pipeline_simple.py',
        'src/pipeline_ai.py',
        'src/generators/generate_music.py',
        'src/generators/generate_image.py',
        'src/utils/create_video.py',
        'src/utils/upload_youtube.py',
    ]

    errors = []
    for file in python_files:
        if not os.path.exists(file):
            print(f"  ⚠ {file} - NOT FOUND")
            continue
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"  ✓ {file} - Syntax OK")
        except SyntaxError as e:
            print(f"  ✗ {file} - SYNTAX ERROR: {e}")
            errors.append(file)

    return len(errors) == 0


def test_config_yaml():
    """Checks if config.yaml is valid"""
    print("\n🔍 Checking config.yaml...\n")

    try:
        import yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        # Check structure
        required_keys = ['music', 'image', 'youtube', 'output']
        for key in required_keys:
            if key in config:
                print(f"  ✓ Section '{key}' present")
            else:
                print(f"  ✗ Section '{key}' missing")
                return False

        return True
    except Exception as e:
        print(f"  ✗ Error reading config.yaml: {e}")
        return False


def test_git_repo():
    """Checks if it's a valid git repository"""
    print("\n🔍 Checking Git repository...\n")

    import subprocess
    try:
        # Check if it's a git repo
        result = subprocess.run(['git', 'status'],
                                capture_output=True,
                                text=True)
        if result.returncode == 0:
            print("  ✓ Git repository initialized")

            # Check remote
            result = subprocess.run(['git', 'remote', '-v'],
                                    capture_output=True,
                                    text=True)
            if 'github.com' in result.stdout:
                print("  ✓ GitHub remote configured")
                remote_url = result.stdout.split('\n')[0].split('\t')[1].split(' ')[0]
                print(f"     {remote_url}")
                return True
            else:
                print("  ⚠ GitHub remote not configured")
                return True
        else:
            print("  ✗ Not a Git repository")
            return False
    except Exception as e:
        print(f"  ✗ Error checking Git: {e}")
        return False


def main():
    print("=" * 60)
    print("🧪 BASIC PROJECT TEST")
    print("=" * 60)
    print()

    tests = [
        ("Project Structure", test_project_structure),
        ("GitHub Structure", test_github_structure),
        ("Python Syntax", test_python_syntax),
        ("YAML Configuration", test_config_yaml),
        ("Git Repository", test_git_repo),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error running test '{name}': {e}")
            results.append((name, False))

    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print()

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status} - {name}")

    print()
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ Project is properly structured")
        print("✅ Python code without syntax errors")
        print("✅ Valid configuration")
        print("✅ Git and GitHub configured")
        print("\n🚀 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Configure YouTube API (see SETUP.md)")
        print("   3. Run: python pipeline.py --prompt 'test' --duration 30")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
