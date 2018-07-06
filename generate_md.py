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
problems = {}
solutions = {}

pat_problem = re.compile('Problem >_{\s+(.+?)\s+}_<', re.DOTALL)
pat_solution = re.compile('Solution >_{\s+(.+?)\s+}_<', re.DOTALL)

for i in files:
    r = os.path.basename(i).split('.')[0]
    if r not in ids:
        continue
    content = open(i).read()
    problem = pat_problem.findall(content)
    if len(problem) > 0:
        problems[r] = problem[0].replace('\n', '<br>').decode('utf8')
    solution = pat_solution.findall(content)
    if len(solution) > 0:
        solutions[r] = solution[0].replace('\n', '<br>').decode('utf8')

headers = '|ID | Title | Problem | Solution \n|:---:|-|-|:-:\n'
print headers

f = open('README.md', 'w')
f.write(headers)
for r in ids:
    s = rq.get('http://hihocoder.com/problemset/problem/%s')
    f.write(('[%s](http://hihocoder.com/problemset/problem/%s)|%s|%s\n' % \
        (r, r, (r in problems and problems[r]) or '', (r in solutions and solutions[r]) or '')).encode('utf8'))
