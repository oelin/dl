import time
import warnings
import os
import requests
import pyquery
import normality

from sys import argv


README_TEMPLATE = '''# {}

An implementation of {} from [{}]({}) in {}.

Installation
------------

Install with pip.

```sh
pip install git+{}
```

Citations
---------

```bibtex
{}
```
```'''

WRITEUP_TEMPLATE = '''# {}

- Paper: [{}]({})
- Code: [{}]({})
- Notebook: n/a
- Model: n/a
- Dataset: n/a

Introduction
------------

## Section 1

## Section 2

## Section 3

Citations
---------

```bibtex
{}
```'''

LICENSE_TEMPLATE = '''MIT License

Copyright (c) {} {}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

GITIGNORE_TEMPLATE = '''**__pycache__/
**.lock
**.bak
**.swp
**.ckpt
**.pth
**.pt
**logs/**'''


warnings.filterwarnings("ignore")


def write_file(path: str, content: str) -> None:

    with open(path, 'w') as file:
        size = file.write(content)

    size = size / 1e3

    print(f'[+]   💾 Wrote {path} ({size:0.2f} kB)')


def main():

    if len(argv) != 2:
        print('usage: dl [arXiv URL]')
        return

    print('[*]   ⏬ Downloading arXiv page...')

    arxiv_url = argv[1]
    arxiv_page = requests.get(arxiv_url).text
    arxiv_document = pyquery.PyQuery(arxiv_page.encode('utf-8', 'ignore'))
    paper_bibtex = requests.get(arxiv_url.replace('abs', 'bibtex')).text.strip()
    paper_title = arxiv_document.find('.title.mathjax').text().replace('Title:', '')
    paper_author = arxiv_document.find('.authors').children()[1].text.strip().split(' ')[-1]
    #paper_year = arxiv_document.find('.dateline').text().split(' ')[-1][: -1]

    print(f'[*]   📃 Extracting paper information...')
    print(f'[-]   @paper-title  = {paper_title}')
    print(f'[-]   @paper-author = {paper_author} et al.')
    #print(f'[-]   @paper-year   = {paper_year}')
    print(f'[-]   @paper-bibtex = {bool(paper_bibtex)}')

    download_url = arxiv_url.replace('abs', 'pdf') + '.pdf'

    project_title = input(f'[?]   🔮 Project title (Untitled Project): ').strip() or 'Untitled Project'
    project_slug = normality.slugify(project_title)
    project_slug = input(f'[?]   🐌 Project slug ({project_slug}): ').strip() or project_slug
    project_slug = normality.slugify(project_slug)
    project_root = project_slug.replace('-', '_')
    project_framework = input(f'[?]   🧪 Project framework (PyTorch): ').strip() or 'PyTorch'
    project_dependencies = input(f'[?]   🧩 Project dependencies (space separated): ').strip() or 'black'

    git_username = input(f'[?]   🌍 GIT username (kore): ').strip() or f'kore'
    git_host = input(f'[?]   🌍 GIT host (codeberg.org): ').strip() or f'codeberg.org'

    project_repository = f'{git_username}/{project_slug}'
    project_repository_web = f'https://{git_host}/{git_username}/{project_repository}'
    project_repository_ssh = f'git@{git_host}:{git_username}/{project_repository}'

    print(f'[-]   @project-title        = {project_title}')
    print(f'[-]   @project-slug         = {project_slug}')
    print(f'[-]   @project-dependencies = {project_dependencies}')
    print(f'[-]   @project-framework    = {project_framework}')
    print(f'[-]   @project-repository   = {project_repository}')
    print(f'[*]   💀 Creating project skeleton...')

    os.system(f'poetry new {project_slug} --no-interaction')
    os.system(f'cd {project_slug}; poetry add {project_dependencies}')

    write_file(f'./{project_slug}/README.md', README_TEMPLATE.format(
        project_title,
        project_title,
        paper_title,
        arxiv_url,
        project_framework,
        project_repository_ssh,
        paper_bibtex,
    ))

    write_file(f'./{project_slug}/WRITEUP.md', WRITEUP_TEMPLATE.format(
        project_title,
        paper_title,
        arxiv_url,
        project_repository,
        project_repository_web,
        paper_bibtex,
    ))

    write_file(f'./{project_slug}/LICENSE', LICENSE_TEMPLATE.format(
	git_username,
	time.localtime().tm_year,
    ))

    write_file(f'./{project_slug}/.gitignore', GITIGNORE_TEMPLATE)

    print(f'[*]   🌍 Initializing GIT repository...')

    os.system(f'cd ./{project_slug}; git init')
    os.system(f'cd ./{project_slug}; git remote add origin {project_repository_ssh}')

    print(f'[+]   🥳 PROJECT CREATED!')
