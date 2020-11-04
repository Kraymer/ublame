# boogit

boogit is born from the frustration of using `git blame` to track the successive 
editors of a code segment.
It performs a search on a file commits history and reports all the
modified lines that contain searched term.

The name is inspired from The Jackson's 1978 disco hit _"Blame It on the Boogie"_.

## Example

`git blame` can be of limited use when the last commit reported has no interest.
A common case is having a monster commit that converts the indentation type :

~~~
❯ git blame tests/rsrc/example.py | grep "if token in diff"

e65d24b3 (Fabrice Laporte 2020-11-04 21:51:32 +0100  8)     if token in diff:

❯ git show e65d24b3
commit e65d24b336570822d33f91847542743969b17fa2 (HEAD -> main)
Author: Fabrice Laporte
Date:   Wed Nov 4 21:51:32 2020 +0100

    chore: convert tabs to spaces
~~~

So you need to apply `git blame` on the version of the file preceding e65d24b3 and so on ...

With `boogit` the information is immediatley available in one command :

~~~
❯ boogit tests/rsrc/example.py "if token in diff"

Commit: e65d24b336570822d33f91847542743969b17fa2
Author: Fabrice Laporte
Date: 2020-11-04 22:12:33+01:00

    chore: convert tabs to spaces

 def trim_diff(diff, token):
-       """Keep only context surrounding searched token.
-       """
-       if token in diff:
-               LOC_BEFORE = LOC_AFTER = 3
-       lines = diff.split("\n")

Commit: 01c5f3e2a91bcffbb5bdb24cac20d76f98b33db4
Author: Fabrice Laporte <fabrice@yescapa.com>
Date: 2020-11-04 22:12:30+01:00

    tests: add example.py

+def trim_diff(diff, token):
+       """Keep only context surrounding searched token.
+       """
+       if token in diff:
+               LOC_BEFORE = LOC_AFTER = 3
+       lines = diff.split("\n")
~~~
