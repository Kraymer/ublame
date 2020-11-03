#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import blessed
import os
import click
from pydriller import RepositoryMining, GitRepository

term = blessed.Terminal()


def trim_diff(diff, token):
    """Keep only context surrounding searched token.
    """
    LOC_BEFORE = LOC_AFTER = 3
    lines = diff.split("\n")
    for index, line in enumerate(lines):
        if token in line:
            break
    if lines[index][0] not in ("+", "-"):
        return
    return "\n".join(lines[max(index - LOC_BEFORE, 0) : index + LOC_AFTER])


def print_commit_infos(commit):
    """Print commit summary infos.
    """
    print(
        """
Commit: {}
Author: {}<{}>
Date: {}""".format(
            commit.hash, commit.author.name, commit.author.email, commit.committer_date
        )
    )


def repo_path_for(filename):
    """Go up filename path and returns path of first repository met.
    """
    while filename:
        filename = os.path.dirname(filename)
        if os.path.exists(os.path.join(filename, ".git")):
            return filename


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]), help="Recursive blame",
)
@click.argument("filename", type=click.Path(exists=True), metavar="FILE", nargs=1)
@click.argument("token", nargs=1)
def boogit(filename, token):
    repo_path = repo_path_for(filename)
    relative_filename = filename.split(repo_path)[-1].strip("/")
    repo = GitRepository(repo_path)
    ever_found = False
    for commit_hash in repo.get_commits_modified_file(relative_filename):
        commit = repo.get_commit(commit_hash)
        diffs = []
        ever_found = found = False
        for m in commit.modifications:
            if token in m.diff:
                diff = trim_diff(m.diff, token)
                if diff:
                    diffs.append(diff)
                found |= True
                ever_found = True
            elif not diffs and m.source_code:
                found |= token in m.source_code

        if any(diffs):
            print_commit_infos(commit)
            print(term.on_white(term.black("\n" + "\n".join(diffs))))
        elif ever_found and not found:
            exit()  # we went past the appearance of string in code, exit

    if not ever_found:
        print("'{}' not found in {} commits history".format(token, filename))


if __name__ == "__main__":
    boogit()
