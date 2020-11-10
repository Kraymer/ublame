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


def trim_diff(diff, token, context=3):
    """Keep only context surrounding searched token."""
    if token in diff:
        LOC_BEFORE = LOC_AFTER = context
        lines = diff.split("\n")
        for index, line in enumerate(lines):
            if token in line:
                break
        if lines[index][0] not in ("+", "-"):
            return ""
        return "\n".join(lines[max(index - LOC_BEFORE, 0) : index + LOC_AFTER + 1])
    return ""


def diff_commit(commit, token):
    """Print diffs that contain token.
    Return True if token is present in file.
    """
    diffs = []
    found = False
    for m in commit.modifications:
        diff = trim_diff(m.diff, token)
        if diff:
            diffs.append(diff)
        elif m.source_code:
            found |= token in m.source_code

    if any(diffs):
        print_commit_infos(commit)
        print(term.on_white(term.black("\n" + "\n".join(diffs))))

    return any(diffs) or found


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]), help="Recursive blame",
)
@click.argument("filename", type=click.Path(exists=True), metavar="FILE", nargs=1)
@click.argument("token", nargs=1)
def ublame_cli(filename, token):
    filename = os.path.abspath(filename)
    repo_path = repo_path_for(filename)
    relative_filename = filename.split(repo_path)[-1].strip("/")
    repo = GitRepository(repo_path)
    ever_found = False

    for commit_hash in repo.get_commits_modified_file(relative_filename):
        commit = repo.get_commit(commit_hash)
        found = diff_commit(commit, token)
        ever_found |= found

        if ever_found and not found:
            exit()  # we went past the appearance of string in code, exit

    if not ever_found:
        print("'{}' not found in {} commits history".format(token, filename))


if __name__ == "__main__":
    ublame_cli()
