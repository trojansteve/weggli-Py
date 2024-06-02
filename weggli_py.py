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

def setup_logging():
    # Configure the logger with the name 'weggli_logger' and set the logging level to INFO
    logger = logging.getLogger('weggli_logger')
    logger.setLevel(logging.INFO)

    # Create a file handler that logs messages to 'weggli_scan_results.log'
    file_handler = logging.FileHandler('weggli_scan_results.log')
    # Define the format for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Set the defined format to the file handler
    file_handler.setFormatter(formatter)
    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Return the configured logger
    return logger

def load_weggli_patterns(file_path):
    # Open the JSON file containing weggli patterns and return the parsed JSON
    with open(file_path, 'r') as file:
        return json.load(file)

def run_weggli_commands(weggli_patterns, code_path, logger):
    # Iterate over the patterns defined in the JSON file
    for pattern in weggli_patterns['weggli_patterns']:
        category = pattern['category']
        # Output the category being scanned to the console and log file
        console_output(f"\nScanning for: {category}", "blue")
        logger.info(f"Scanning for: {category}")
        
        # Iterate over the commands within the current category
        for command_info in pattern['commands']:
            # Construct the command by appending the code path to the base command
            command = command_info['command'] + f" {code_path}"
            # Output the command being run to the console and log file
            console_output(f"\nRunning command: {command}", "yellow")
            logger.info(f"Running command: {command}")
            
            try:
                # Execute the weggli command using the subprocess module
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                # If the command has output, display and log the findings
                if result.stdout:
                    console_output("Findings:", "green")
                    console_output(result.stdout, "white")
                    logger.info(f"Findings:\n{result.stdout}")
                else:
                    # If there are no findings, indicate this in the console and log file
                    console_output("No findings.", "red")
                    logger.info("No findings.")
            except subprocess.CalledProcessError as e:
                # If the command execution fails, output and log the error
                console_output(f"Error executing command: {e}", "red")
                logger.error(f"Error executing command: {e}")
                logger.error(e.stderr)

def console_output(message, color):
    # Define a dictionary mapping color names to ANSI escape codes
    colors = {
        "blue": "\033[1;34m",
        "yellow": "\033[1;33m",
        "green": "\033[1;32m",
        "white": "\033[0;37m",
        "red": "\033[1;31m"
    }
    # Define the ANSI code to reset formatting
    reset = "\033[0m"
    # Print the message to the console with the specified color
    print(f"{colors.get(color, '')}{message}{reset}")

def main():
    # Initialize logging
    logger = setup_logging()

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Scan a codebase for bugs using weggli with predefined patterns.')
    parser.add_argument('patterns_file', type=str, help='Path to the JSON file containing weggli patterns.')
    parser.add_argument('code_path', type=str, help='Path to the codebase to scan.')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Load the weggli patterns from the specified JSON file
    weggli_patterns = load_weggli_patterns(args.patterns_file)
    # Run the weggli commands using the loaded patterns and the specified code path
    run_weggli_commands(weggli_patterns, args.code_path, logger)

# Check if the script is being run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    # If so, execute the main function
    main()
