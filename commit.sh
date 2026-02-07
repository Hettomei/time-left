set -eu

python -m black src
python -m pytest -vvvx src
python -m mypy src
