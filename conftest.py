# conftest.py intentionally left minimal for CI hygiene.
# The project previously added sys.path modifications here to make pytest import the package
# during local development. For CI we prefer to install the package in editable mode
# (pip install -e .) so tests run with the package properly installed instead of
# mutating sys.path.
#
# If you run tests locally and face import errors, run:
#   python -m venv .venv
#   source .venv/bin/activate
#   pip install -e .
#   pip install -r requirements.txt
# and then run `pytest` from the project root.
