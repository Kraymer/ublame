#!/usr/bin/env python3
# -*- coding: utf-8 -*-

for commit in RepositoryMining(".").traverse_commits():
    print("Hash {}, author {}".format(commit.hash, commit.author.name))

# for commit in get_commits_modified_file(filepath):
#   for m in commit.modifications:
#      if token in m.diff:
#       print(commit)
#       print(diff)
