import glob
import os
import re
import requests as rq

web = rq.get('http://hihocoder.com/user/22090/problemset').text
pat_id = re.compile(u'>#(.*?)\uff1a(.*?)</a>')
ids = []
title = {}
for i in pat_id.findall(web):
    ids.append(i[0])
    title[i[0]] = i[1]
ids = sorted(ids)

files = sorted(glob.glob('../*.cpp') + glob.glob('../*.py'))
problems = {i: '' for i in ids}
solutions = {i: '' for i in ids}

pat_problem = re.compile('Problem >_{\s+(.+?)\s+}_<', re.DOTALL)
pat_solution = re.compile('Solution >_{\s+(.+?)\s+}_<', re.DOTALL)
pat_latex = re.compile('\$(.*?)\$')

def get_markdown(content, pat, pat_latex):
    results = pat.findall(content)
    if len(results) == 0:
        return ''
    ret = results[0].replace('\n', '<br>').decode('utf8')
    ret = pat_latex.sub(r'<img src="http://latex.codecogs.com/gif.latex?\1"/>', ret)
    return ret

for i in files:
    r = os.path.basename(i).split('.')[0]
    if r not in ids:
        continue
    content = open(i).read()
    problems[r] = get_markdown(content, pat_problem, pat_latex)
    solutions[r] = get_markdown(content, pat_solution, pat_latex)

headers = '|ID | Title | Problem | Solution \n|:---:|:-:|-|-\n'
print headers

f = open('README.md', 'w')
f.write(headers)
for r in ids:
    s = rq.get('http://hihocoder.com/problemset/problem/%s')
    f.write(('[%s](http://hihocoder.com/problemset/problem/%s)|%s|%s|%s\n' % \
        (r, r, title[r], problems[r], solutions[r])).encode('utf8'))
