
~~~
import pydriller

for commit in get_commits_modified_file(filepath):
  for m in commit.modifications:
     if token in m.diff:
      print(commit)
      print(diff)

~~~
