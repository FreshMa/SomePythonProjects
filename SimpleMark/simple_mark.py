import sys, re
from util import *

print '<html><head><title>...</title><body>'
title = True
for block in blocks(sys.stdin):
    #对块中用 * * 标记的内容进行斜体替换。\1代表正则匹配结果中第一个组的引用，即第一组括号中的内容
    block = re.sub(r'\*(.+?)\*',r'<em>\1</em>',block)
    #第一个块作为标题，用h1标签标记
    if title:
        print '<h1>'
        print block
        print '</h1>'
        title = False
    #其余的块都作为普通段落
    else:
        print '<p>'
        print block
        print '</p>'
print '</body></html>'
