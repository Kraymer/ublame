.. image:: https://coveralls.io/repos/github/Kraymer/ublame/badge.svg?branch=main
   :target: https://coveralls.io/github/Kraymer/ublame
.. image:: https://img.shields.io/pypi/v/ublame.svg
   :target: https://pypi.python.org/pypi/ublame
.. image:: https://pepy.tech/badge/ublame  
   :target: https://pepy.tech/project/ublame

Ublame
======

.. image:: https://github.com/Kraymer/__pub/raw/master/ublame.jpg

*Artist's rendering of the bathyscaphe Trieste -- britannica.com*

    **/ˈublaːm(ə)/** :

    | ``git blame``\ with some depth.  
    | Portmanteau word from : 
    | 1. *u-boat*: anglicised version of the German word U-Boot that refers to any submarine  
    | 2. *blame*: git command that annotate each line in a given file with information from the revision which last modified the line.

Install
-------

Ublame is written for Python 3.6+ and is tested on Linux.

Install with pip via ``pip3 install ublame`` command.

Why
---

``ublame`` is born from the frustration of using ``git blame`` to track the successive editors of a code segment.  
It performs a search on a file commits history and reports all the revisions that contain searched term in their diffs.

See SO question `Git blame — prior commits? <https://stackoverflow.com/questions/5098256/git-blame-prior-commits/>`_

.. figure:: https://raw.githubusercontent.com/Kraymer/ublame/main/docs/ublame_why.png

Example
-------

The last modification is not always the information you need when you
try to grasp a piece of code.

::

    ❯ git blame tests/rsrc/example.py | grep "if token in diff"

    e65d24b3 (Fabrice Laporte 2020-11-04 21:51:32 +0100  8)     if token in diff:

    ❯ git show e65d24b3
    commit e65d24b336570822d33f91847542743969b17fa2 (HEAD -> main)
    Author: Fabrice Laporte
    Date:   Wed Nov 4 21:51:32 2020 +0100

        chore: convert tabs to spaces

In that example, the last commit modified the code only to convert tabs
to spaces and previous commits that were probably more interesting to
get the original intention of the developer(s) are not captured by
``git blame``. So you need to apply ``git blame`` on the version of the
file preceding *e65d24b3* and so on ...

With ``ublame`` the information is instantly available in one command :

::

    ❯ ublame tests/rsrc/example.py "if token in diff"

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

Screenshot
----------

.. figure:: https://raw.githubusercontent.com/Kraymer/ublame/main/docs/ublame_screenshot.png
