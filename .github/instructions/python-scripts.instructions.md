# Code Review Instructions for Python Scripts

This file provides instructions for GitHub Copilot code review when reviewing changes to Python script files in the `scripts/` directory.

## Testing Requirements

When changes are made to any Python script file in the `scripts/` directory, verify that the test suite has been executed successfully.

### Verification Requirements

The `poetry run test` command must be executed before committing changes to Python scripts. This command:

1. Runs formatters (Prettier, isort, black)
2. Runs linters (mypy, pylint)
3. Executes pytest with coverage reporting

### Code Review Checks

When reviewing changes to Python scripts, verify that:

1. **Tests have been executed**: The developer should run `poetry run test` before committing
2. **All tests pass**: No test failures should be present
3. **Code coverage is maintained**: New code should include appropriate test coverage
4. **Type hints are present**: All functions must have parameter and return type annotations
5. **Code quality checks pass**: mypy and pylint should report no errors

### Flagging Issues

Flag the following issues:

- Python script files have been modified but tests were not run
- Test failures are present in the output
- New functions or methods lack type hints
- Code changes lack corresponding test updates when behavior is modified
- Code quality tools (mypy, pylint) report errors

## Code Style Requirements

All Python code must adhere to the following:

- **Formatting**: Black (default line length)
- **Import sorting**: isort with Black profile
- **Type checking**: mypy with strict typing
- **Linting**: pylint with no errors
- **Testing**: pytest with coverage

## Test Coverage Expectations

When modifying existing functions or adding new functionality:

- Maintain or improve test coverage
- Add tests for new functions and methods
- Update tests when function behavior changes
- Ensure edge cases are tested

## Related Files

- Test files are located in `tests/` directory
- Test naming convention: `test_<module_name>.py`
- Each script in `scripts/` should have a corresponding test file
