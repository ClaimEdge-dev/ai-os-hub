#!/usr/bin/env python3
"""Compatibility shortcut for DEBO's canonical skill delta auditor.

The implementation lives in tools/debo_skill_delta.py. Keep both entrypoints
working; this file intentionally contains no duplicate audit logic.
"""
from debo_skill_delta import main

if __name__ == "__main__":
    main()
