import blessed
import os
import click
from pydriller import RepositoryMining, GitRepository

""" ublame: `git blame` over a file lifetime
    Search for edits on a given string in a file git history. 
"""

__version__ = "0.1.0"

term = blessed.Terminal()


def print_commit_infos(commit):
    """Print commit summary infos."""
    print(
        """
Commit: {}
Author: {} <{}>
Date: {}

\t{}""".format(
            commit.hash,
            commit.author.name,
            commit.author.email,
            commit.committer_date,
            commit.msg,
        )
    )


def repo_path_for(filename):
    """Go up filename path and returns path of first repository met."""
    while filename:
        filename = os.path.dirname(filename)
        if os.path.exists(os.path.join(filename, ".git")):
            return filename


def trim_diff(diff, patterns, context=3):
    """Keep only context surrounding searched token."""
    if any([x in diff for x in patterns]):
        LOC_BEFORE = LOC_AFTER = context
        lines = diff.split("\n")
        for index, line in enumerate(lines):
            if any([x in line for x in patterns]):
                break
        if lines[index][0] not in ("+", "-"):
            return ""
        return "\n".join(lines[max(index - LOC_BEFORE, 0) : index + LOC_AFTER + 1])
    return ""


def diff_commit(commit, patterns):
    """Print diffs that contain token.
    Return True if token is present in file.
    """
    diffs = []
    for m in commit.modifications:
        diff = trim_diff(m.diff, patterns)
        if diff:
            diffs.append(diff)

    if any(diffs):
        print_commit_infos(commit)
        print(term.on_white(term.black("\n" + "\n".join(diffs))))


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="Search for PATTERNS in FILE commits history",
)
@click.argument("filename", type=click.Path(exists=True), metavar="FILE", nargs=1)
@click.argument("patterns", nargs=-1, required=True)
def ublame_cli(filename, patterns):
    filename = os.path.abspath(filename)
    repo_path = repo_path_for(filename)
    relative_filename = filename.split(repo_path)[-1].strip("/")
    repo = GitRepository(repo_path)

    for commit_hash in repo.get_commits_modified_file(relative_filename):
        commit = repo.get_commit(commit_hash)
        diff_commit(commit, patterns)


if __name__ == "__main__":
    ublame_cli()
