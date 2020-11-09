#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def trim_diff(diff, token):
    """Keep only context surrounding searched token."""
    if token in diff:
        LOC_BEFORE = LOC_AFTER = 3
    lines = diff.split("\n")
    for index, line in enumerate(lines):
        if token in line:
            break
    if lines[index][0] not in ("+", "-"):
        return
    return "\n".join(lines[max(index - LOC_BEFORE, 0) : index + LOC_AFTER])
