# CSV converter for Google App Engine bulk import

import sys
reload(sys)
import locale
sys.setdefaultencoding(locale.getpreferredencoding())
import xml.dom.minidom
from datetime import datetime

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
EDITOR = 'my.name@gmail.com'
ID_START = 1

infilename = sys.argv[1]
doc = xml.dom.minidom.parse(open(infilename))

def escape_csv(s):
    return '"' + s.replace('"', '""') + '"'

ident = ID_START
for node in [n for n in doc.childNodes[0].childNodes if n.nodeType == n.ELEMENT_NODE]:
    keys = ['word', 'pos', 'stem', 'props', 'from',
            'orig', 'comment']
    results = []
    results.append(str(ident))
    ident += 1
    for key in keys:
        tags = node.getElementsByTagName(key)
        if tags:
            field = tags[0]
            if field.nodeName == 'props':
                if len(field.childNodes) == 0:
                    results.append('')
                elif len(field.childNodes[0].childNodes) == 0:
                    results.append('')
                else:
                    results.append(escape_csv(field.childNodes[0].childNodes[0].data))
            else:
                if len(field.childNodes) == 0:
                    results.append('')
                else:
                    results.append(escape_csv(field.childNodes[0].data))
        else:
            results.append('')
    # 'date', 'editor'
    results.append(escape_csv(NOW))
    results.append(escape_csv(EDITOR))
    results.append('')          # dummy
    print ','.join(results)

