import sys

# Keep image baselines tied to the interpreter version they were regenerated on.
collect_ignore_glob = ["test_*.py"] if sys.version_info[:2] <= (3, 10) else []
