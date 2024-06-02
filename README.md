# Weggli-Py

Weggli-Py is a Python-based interface designed to automate and enhance the scanning of C/C++ codebases for security vulnerabilities. It extends [weggli](https://github.com/googleprojectzero/weggli), a highly efficient query tool by Google Project Zero for C/C++ codebases, by providing a user-friendly interface and additional features to streamline the scanning process.

## Features

- **Automated Pattern Execution**: Execute patterns defined in a JSON file against a codebase automatically.
- **Enhanced Output Formatting**: Color-coded and structured output for easy interpretation of findings.
- **Logging Capability**: Scan results are logged to a file for permanent record-keeping.
- **User-Friendly Interface**: Command-line interface with clear instructions for users of all technical levels.

## Getting Started

### Prerequisites

Before installing Weggli-Py, you must have weggli installed and built on your system. Follow the installation and build instructions provided in the [weggli repository](https://github.com/googleprojectzero/weggli).

### Installation

1. Clone the Weggli-Py repository to your local machine:
2. Copy the Weggli-Py files into the weggli repository directory

### Usage
With Weggli-Py integrated into weggli, you can now run the tool using the following command:

1. python weggli_py.py --patterns patterns.json --codebase /path/to/codebase

2. Replace /path/to/codebase with the path to the C/C++ codebase you wish to scan.
