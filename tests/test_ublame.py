import os
import unittest

from ..ublame import repo_path_for, trim_diff

LOREM_IPSUM = """
Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
"""

LINES = """{}
+def trim_diff(diff, token):
{}
""".format(
    LOREM_IPSUM * 3, LOREM_IPSUM * 3
)


class ConfigTest(unittest.TestCase):
    def test_repo_path_for(self):
        self.assertEquals(
            repo_path_for(__file__),
            os.path.abspath(os.path.dirname(os.path.join(__file__, "../../"))),
        )

    def test_trim_diff_not_found(self):
        self.assertEquals(trim_diff(LINES, "foobar"), "")

    def test_trim_diff_found(self):
        self.assertEquals(
            trim_diff(LINES, ("token",), 2), "\n".join(LINES.split("\n")[11:16])
        )
