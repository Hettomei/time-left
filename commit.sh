set -eu

python -m pytest -vvvx src
python -m mypy src
python -m black src
