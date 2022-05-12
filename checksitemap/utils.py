#!/usr/bin/env python3

import sys

WARNING = "Warning"
ERROR = "Error"
NOTICE = "Notice"


def stderr(what: str, type_err: str = WARNING):
    print(f"{type_err}: {what}", file=sys.stderr)
