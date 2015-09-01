from __future__ import absolute_import

import re
from lib2to3 import fixer_base
from lib2to3.pygram import token
from lib2to3.fixer_util import Name, Call, syms
from libmodernize import touch_import

_mapping = {u"unichr" : u"chr", u"unicode" : u"str"}
_literal_re = re.compile(u"[uU][rR]?[\\'\\\"]")

class FixUnicode2(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = """STRING"""

    def transform(self, node, results):
        if not _literal_re.match(node.value):
            parent = node.parent
            if parent and parent.type == syms.simple_stmt and \
                    len(parent.children) > 0 and parent.children[0].type == token.STRING:
                # skip over docstring
                return node
            try:
                node.value.encode("ascii")
            except UnicodeEncodeError:
                new = node.clone()
                new.value = "u%s" % (node.value, )
                return new
