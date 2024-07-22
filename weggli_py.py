# MIT License
# 
# Copyright (c) 2024 Stephen O. Haruna
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import json
import subprocess
import argparse
import logging
import os
from concurrent.futures import ThreadPoolExecutor

def setup_logging(log_level, output_dir):
    logger = logging.getLogger('weggli_logger')
    logger.setLevel(log_level)
    
    log_file_path = os.path.join(output_dir, 'weggli_scan_results.log')
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def load_weggli_patterns(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def run_weggli_command(command, logger, verbose):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            if verbose:
                console_output(result.stdout, "white")
            logger.info(f"Findings:\n{result.stdout}")
            return result.stdout
        else:
            if verbose:
                console_output("No findings.", "red")
            logger.info("No findings.")
            return ""
    except subprocess.CalledProcessError as e:
        if verbose:
            console_output(f"Error executing command: {e}", "red")
        logger.error(f"Error executing command: {e}")
        logger.error(e.stderr)
        return f"Error: {e}"

def run_weggli_commands(weggli_patterns, code_path, logger, verbose):
    summary_report = {}
    
    def scan_category(category, commands):
        console_output(f"\nScanning for: {category}", "blue")
        logger.info(f"Scanning for: {category}")
        findings = 0
        for command_info in commands:
            command = command_info['command'] + f" {code_path}"
            console_output(f"\nRunning command: {command}", "yellow")
            logger.info(f"Running command: {command}")
            result = run_weggli_command(command, logger, verbose)
            if result and "Findings" in result:
                findings += 1
        summary_report[category] = findings

    with ThreadPoolExecutor() as executor:
        futures = []
        for pattern in weggli_patterns['weggli_patterns']:
            category = pattern['category']
            commands = pattern['commands']
            futures.append(executor.submit(scan_category, category, commands))
        for future in futures:
            future.result()  # Ensure all threads have completed
    
    return summary_report

def console_output(message, color):
    colors = {
        "blue": "\033[1;34m",
        "yellow": "\033[1;33m",
        "green": "\033[1;32m",
        "white": "\033[0;37m",
        "red": "\033[1;31m"
    }
    reset = "\033[0m"
    print(f"{colors.get(color, '')}{message}{reset}")

def write_summary_report(summary_report, output_dir):
    summary_file_path = os.path.join(output_dir, 'summary_report.txt')
    with open(summary_file_path, 'w') as file:
        for category, findings in summary_report.items():
            file.write(f"{category}: {findings} findings\n")
    console_output(f"Summary report written to {summary_file_path}", "green")

def main():
    parser = argparse.ArgumentParser(description='Scan a codebase for bugs using weggli with predefined patterns.')
    parser.add_argument('patterns_file', type=str, help='Path to the JSON file containing weggli patterns.')
    parser.add_argument('code_path', type=str, help='Path to the codebase to scan.')
    parser.add_argument('--log-level', type=str, default='INFO', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).')
    parser.add_argument('--output-dir', type=str, default='.', help='Directory to store the log file and summary report.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode.')
    args = parser.parse_args()
    
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    logger = setup_logging(log_level, args.output_dir)
    weggli_patterns = load_weggli_patterns(args.patterns_file)
    summary_report = run_weggli_commands(weggli_patterns, args.code_path, logger, args.verbose)
    write_summary_report(summary_report, args.output_dir)

if __name__ == "__main__":
    main()
