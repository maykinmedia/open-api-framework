"""
Script to check if open_api_framework has properly documented (or excluded) all environment
variables that are loaded by the library itself
"""

import ast
import sys
from pathlib import Path


class ConfigChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "config":
            has_help_text = False
            has_add_to_docs = False

            # Check for 'help_text' or 'add_to_docs' in the arguments
            for keyword in node.keywords:
                if keyword.arg == "help_text" and isinstance(
                    keyword.value, (ast.Constant, ast.JoinedStr)
                ):
                    has_help_text = True
                elif (
                    keyword.arg == "add_to_docs"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is False
                ):
                    has_add_to_docs = True

            # Record issue if neither is found
            if not (has_help_text or has_add_to_docs):
                self.issues.append((node.lineno, node.col_offset))

        self.generic_visit(node)


def check_config_usage(file_path):
    with file_path.open("r") as source:
        tree = ast.parse(source.read(), filename=str(file_path))

    checker = ConfigChecker()
    checker.visit(tree)

    return checker.issues


def check_library(directory):
    issues = {}
    for file_path in directory.rglob("*.py"):
        issues_in_file = check_config_usage(file_path)
        if issues_in_file:
            issues[file_path] = issues_in_file

    return issues


# Example usage
library_directory = Path("open_api_framework/")
issues = check_library(library_directory)

if issues:
    for file_path, positions in issues.items():
        for lineno, col_offset in positions:
            print(
                f"Issue in {file_path} at line {lineno}, column {col_offset}: "
                "'config' call lacks 'help_text' or 'add_to_docs=False'"
            )
    sys.exit(1)
else:
    print("All 'config' calls are correctly documented.")
