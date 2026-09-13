"""Executable module entrypoint for clip-storyboard-director (python -m clip_director)."""

import sys
from clip_director.cli import main

if __name__ == "__main__":
    sys.exit(main() or 0)
