# dl

dl is a script for creating deep learning projects. It automates the following tasks:

- Extracting information from arXiv pages (title, author, etc).
- Creating boilerplate files (README, LICENSE etc).
- Creating Python packages using Poetry.
- Initializing GIT repositories.

Installation 
------------

Install with pip.

```sh
pip install git+https://github.com/oelin/dl
```

Usage
-----

dl takes in a single argument, an arXiv URL such as `https://arxiv.org/abs/2202.00273v2`. This URL is intended to point to a paper that you'll be implementing or basing your project on. In future, dl will support multi-paper projects.

```sh
dl [arXiv URL]
```

Example
-------

In this example, the project being created is an implementation of [StyleGAN-XL](https://arxiv.org/abs/2202.00273v2).

```
$ dl 'https://arxiv.org/abs/2202.00273v2'
[*]   ⏬ Downloading arXiv page...
[*]   📃 Extracting paper information...
[-]   @paper-title  = StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets
[-]   @paper-author = Sauer et al.
[-]   @paper-bibtex = True
[?]   🔮 Project title (Untitled Project): StyleGAN-XL
[?]   🐌 Project slug (stylegan-xl):
[?]   🧪 Project framework (PyTorch):
[?]   🧩 Project dependencies (space separated): pillow
[?]   🌍 GIT username (oelin):
[?]   🌍 GIT host (codeberg.org): github.com
[-]   @project-title        = StyleGAN-XL
[-]   @project-slug         = stylegan-xl
[-]   @project-dependencies = pillow
[-]   @project-framework    = PyTorch
[-]   @project-repository   = oelin/stylegan-xl
[*]   💀 Creating project skeleton...
Created package stylegan_xl in stylegan-xl
Using version ^10.1.0 for pillow

Updating dependencies
Resolving dependencies... (0.1s)

Package operations: 1 install, 0 updates, 0 removals

  • Installing pillow (10.1.0)

Writing lock file
[+]   💾 Wrote ./stylegan-xl/README.md (0.57 kB)
[+]   💾 Wrote ./stylegan-xl/WRITEUP.md (0.60 kB)
[+]   💾 Wrote ./stylegan-xl/LICENSE (1.06 kB)
[+]   💾 Wrote ./stylegan-xl/.gitignore (0.07 kB)
[*]   🌍 Initializing GIT repository...
Initialized empty Git repository in /home/oelin/projects/stylegan-xl/.git/
[+]   🥳 PROJECT CREATED!
```

Future
------

- Additional project types for more specific applications (e.g. `huggingface-diffusers-project`).
- Standardized project configuration format.
- Jupyter notebook automation.
- Windows and MacOS support.
