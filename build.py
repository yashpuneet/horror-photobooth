#!/usr/bin/env python3
"""Local DevSecOps runner and auto-fixer for Horror Photobooth."""

import subprocess
import sys


def run_command(title: str, command: list[str], ignore_failure: bool = False) -> bool:
    """Execute a subprocess command with structured console output."""
    print("\n==========================================")
    print(f" ▶ {title}")
    print("==========================================")

    result = subprocess.run(command, text=True)

    if result.returncode != 0:
        if not ignore_failure:
            print(f"\n❌ {title} FAILED")
            return False
        print(f"\n⚠️ {title} completed with warnings")
        return True

    print(f"\n✅ {title} PASSED")
    return True


def main():
    print("🚀 Starting Horror Photobooth Local Verification Suite & Auto-Fixer...\n")

    # 1. AUTO-FIX PHASE
    print("------------------------------------------")
    print(" PHASE 1: Automatic Code Formatting & Lint Fixes")
    print("------------------------------------------")

    run_command("Ruff Auto-Fix", [sys.executable, "-m", "ruff", "check", "--fix", "."])
    run_command("Ruff Code Formatter", [sys.executable, "-m", "ruff", "format", "."])

    # 2. VERIFICATION & AUDIT PHASE
    print("\n------------------------------------------")
    print(" PHASE 2: Security & Quality Verification")
    print("------------------------------------------")

    checks = [
        ("Ruff Final Quality Check", [sys.executable, "-m", "ruff", "check", "."]),
        (
            "Bandit Security Audit",
            [sys.executable, "-m", "bandit", "-c", "pyproject.toml", "-r", "."],
        ),
        (
            "Unit Tests & Coverage",
            [sys.executable, "-m", "coverage", "run", "-m", "unittest", "discover", "-s", "tests"],
        ),
    ]

    failed_checks = []

    for title, command in checks:
        if not run_command(title, command):
            failed_checks.append(title)

    # 3. SUMMARY REPORT
    print("\n==========================================")
    print(" 📊 VERIFICATION SUMMARY REPORT")
    print("==========================================")

    print("\n[Coverage Metrics]")
    subprocess.run([sys.executable, "-m", "coverage", "report", "-m"])

    if failed_checks:
        print("\n❌ VERIFICATION FAILED! Address issues in these stages before pushing:")
        for check in failed_checks:
            print(f"  - {check}")
        sys.exit(1)
    else:
        print("\n✨ ALL CHECKS PASSED & CODE FORMATTED! Ready for Git commit.")
        sys.exit(0)


if __name__ == "__main__":
    main()
