# Horror Photobooth

[![.github/workflows/ci.yml](https://github.com/yashpuneet/horror-photobooth/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yashpuneet/horror-photobooth/actions/workflows/ci.yml)  [![Coverage Status](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/YOUR_GITHUB_USERNAME/Horror_Photobooth)  [![Dependabot](https://img.shields.io/badge/dependabot-enabled-blue.svg?logo=dependabot)](https://github.com/YOUR_GITHUB_USERNAME/Horror_Photobooth)  [![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)  [![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)  [![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

---

### Prerequisites
* **Python**: 3.10 or higher
* **Webcam**: Connected local camera device

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yashpuneet/Horror_Photobooth.git](https://github.com/yashpuneet/Horror_Photobooth.git)
   cd Horror_Photobooth
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Photobooth:**
   ```bash
   py photobooth.py
   ```
---

## Local DevSecOps Quality

This project uses a zero-dependency local runner, `build.py`, to ensure all code complies with formatting, security, and coverage standards before pushing to GitHub.

To run automatic code fixes, security audits, and unit tests:

```bash
py build.py
```

### What `build.py` Executes
1. **Auto-Fix Phase**: Organizes imports and applies PEP 8 code formatting via **Ruff**.
2. **Security Audit**: Scans code for vulnerabilities using **Bandit**.
3. **Test Suite & Coverage**: Runs unit tests and verifies code coverage meets project thresholds.

---

## Security & Architecture

* **Strict Asset Enforcement**: The MediaPipe TFLite model model is downloaded via strict HTTPS stream validation (`urllib.request`) to prevent scheme manipulation (CWE-22 / Bandit B310).
* **Isolated Testing**: Mocked hardware interfaces allow 100% test coverage without requiring active camera access during CI/CD runs.

---