import os

# Ensure tests use temporary DB file to avoid collisions and keep test isolation
os.environ['PYTEST_DB'] = '1'
