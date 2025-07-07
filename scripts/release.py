#!/usr/bin/env python3
"""
Release script for financial-mcp package
Handles version bumping, tagging, and release preparation
"""

import subprocess
import sys
import os
import re
from pathlib import Path
from datetime import datetime

def get_current_version():
    """Get current version from __init__.py"""
    init_file = Path('financial_mcp/__init__.py')
    if not init_file.exists():
        raise FileNotFoundError("Cannot find financial_mcp/__init__.py")
    
    content = init_file.read_text()
    version_match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if not version_match:
        raise ValueError("Cannot find version in __init__.py")
    
    return version_match.group(1)

def update_version(new_version):
    """Update version in __init__.py and setup.py"""
    files_to_update = [
        'financial_mcp/__init__.py',
        'setup.py',
        'pyproject.toml'
    ]
    
    for file_path in files_to_update:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping")
            continue
        
        content = file_path.read_text()
        
        # Update version patterns
        if file_path.name == '__init__.py':
            content = re.sub(r'__version__ = ["\'][^"\']+["\']', 
                           f'__version__ = "{new_version}"', content)
        elif file_path.name == 'setup.py':
            content = re.sub(r'version="[^"]+"', f'version="{new_version}"', content)
        elif file_path.name == 'pyproject.toml':
            content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)
        
        file_path.write_text(content)
        print(f"Updated version in {file_path}")

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\nRunning: {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def bump_version(current_version, bump_type):
    """Bump version number based on type"""
    parts = list(map(int, current_version.split('.')))
    
    if bump_type == 'major':
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif bump_type == 'minor':
        parts[1] += 1
        parts[2] = 0
    elif bump_type == 'patch':
        parts[2] += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    return '.'.join(map(str, parts))

def main():
    """Main release process"""
    print("Financial MCP - Release Tool")
    print("============================")
    
    # Change to repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    # Check if we're in a git repository
    if not Path('.git').exists():
        print("ERROR: Not in a git repository")
        sys.exit(1)
    
    # Check for uncommitted changes
    result = subprocess.run(['git', 'status', '--porcelain'], 
                          capture_output=True, text=True)
    if result.stdout.strip():
        print("ERROR: You have uncommitted changes. Please commit or stash them first.")
        print("Uncommitted files:")
        print(result.stdout)
        sys.exit(1)
    
    # Get current version
    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")
    except Exception as e:
        print(f"Error getting current version: {e}")
        sys.exit(1)
    
    # Ask for new version or bump type
    print("\nHow would you like to update the version?")
    print("1. Patch (bug fixes)")
    print("2. Minor (new features)")
    print("3. Major (breaking changes)")
    print("4. Custom version")
    
    choice = input("Choose an option (1-4): ").strip()
    
    if choice == '1':
        new_version = bump_version(current_version, 'patch')
    elif choice == '2':
        new_version = bump_version(current_version, 'minor')
    elif choice == '3':
        new_version = bump_version(current_version, 'major')
    elif choice == '4':
        new_version = input("Enter new version: ").strip()
        # Validate version format
        if not re.match(r'^\d+\.\d+\.\d+$', new_version):
            print("Error: Version must be in format X.Y.Z")
            sys.exit(1)
    else:
        print("Invalid choice")
        sys.exit(1)
    
    print(f"\nNew version will be: {new_version}")
    confirm = input("Continue? (y/N): ")
    if confirm.lower() != 'y':
        print("Release cancelled")
        sys.exit(0)
    
    # Update version in files
    try:
        update_version(new_version)
    except Exception as e:
        print(f"Error updating version: {e}")
        sys.exit(1)
    
    # Run tests
    print("\nRunning tests...")
    if not run_command("python -m pytest tests/ -v", "Running tests"):
        print("Tests failed. Please fix before releasing.")
        sys.exit(1)
    
    # Commit version changes
    if not run_command("git add .", "Staging changes"):
        sys.exit(1)
    
    commit_msg = f"Bump version to {new_version}"
    if not run_command(f'git commit -m "{commit_msg}"', "Committing version bump"):
        sys.exit(1)
    
    # Create git tag
    tag_name = f"v{new_version}"
    tag_msg = f"Release {new_version}"
    if not run_command(f'git tag -a {tag_name} -m "{tag_msg}"', "Creating git tag"):
        sys.exit(1)
    
    # Push changes and tags
    print("\nPushing changes to remote...")
    if not run_command("git push origin main", "Pushing commits"):
        sys.exit(1)
    
    if not run_command(f"git push origin {tag_name}", "Pushing tag"):
        sys.exit(1)
    
    print(f"\n{'='*50}")
    print("RELEASE COMPLETED SUCCESSFULLY!")
    print(f"{'='*50}")
    print(f"Version: {new_version}")
    print(f"Tag: {tag_name}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("\nNext steps:")
    print("1. Check GitHub Actions for automated PyPI publishing")
    print("2. Monitor PyPI for package availability")
    print("3. Test installation: pip install financial-mcp")
    print("4. Update documentation if needed")
    
if __name__ == "__main__":
    main()
