# c:\Users\devin\Documents\GitHub\Master_Clinerules\Global_Scripts\audit_python_project.py
import argparse
import os
import subprocess
import sys

def run_command(command):
    """Runs a shell command and returns its output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running command '{' '.join(command)}': {e.stderr}"

def check_dependencies(project_path):
    """Checks for pip-audit vulnerabilities."""
    print("\n--- Checking for vulnerable dependencies ---")
    # Ensure pip-audit is installed
    run_command(f"{sys.executable} -m pip install pip-audit")
    
    pyproject_path = os.path.join(project_path, 'pyproject.toml')
    requirements_path = os.path.join(project_path, 'requirements.txt')

    if os.path.exists(pyproject_path):
        print(f"Auditing dependencies from {pyproject_path}...")
        # Change directory to the project path to ensure pip-audit picks up the project context
        audit_result = run_command(f"cd {project_path} && {sys.executable} -m pip-audit")
        print(audit_result)
    elif os.path.exists(requirements_path):
        print(f"Auditing {requirements_path}...")
        audit_result = run_command(f"{sys.executable} -m pip-audit -r {requirements_path}")
        print(audit_result)
    else:
        print("No pyproject.toml or requirements.txt found.")

def check_code_quality(project_path):
    """Checks code quality using flake8."""
    print("\n--- Checking code quality with flake8 ---")
    # Ensure flake8 is installed
    run_command(f"{sys.executable} -m pip install flake8")
    src_path = os.path.join(project_path, 'src')
    if os.path.exists(src_path):
        quality_result = run_command(f"flake8 {src_path}")
        if quality_result.strip():
            print(quality_result)
        else:
            print("flake8 found no issues.")
    else:
        print("No src/ directory found to analyze.")

def main():
    parser = argparse.ArgumentParser(description="Automated Project Auditor based on Master Clinerules.")
    parser.add_argument("project_path", type=str, help="The root path of the project to audit.")
    args = parser.parse_args()

    if not os.path.isdir(args.project_path):
        print(f"Error: Project path '{args.project_path}' not found.")
        sys.exit(1)

    print(f"--- Starting Audit for: {args.project_path} ---")
    check_dependencies(args.project_path)
    check_code_quality(args.project_path)
    print("\n--- Audit Complete ---")

if __name__ == "__main__":
    main()
