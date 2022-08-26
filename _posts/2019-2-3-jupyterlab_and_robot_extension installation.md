---
layout: post
title:  "jupyterlab and extension installation on mac"
date:   2019-02-03 19:29:41 +0800
categories: jupyter
tags: jupyter
---

## pre network setting ##
our internal network has some limitations, so firstly we should set the proxy of network.
```bash
export https_proxy=http://x.x.x.x:8080
export http_proxy=http://x.x.x.x:8080
```

## install conda and jupyter lab ##
### install conda, you can follow the
[conda installation guide on macos](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)


```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
```

### install jupyter lab

[jupyterlab installation guide](https://github.com/jupyterlab/jupyterlab/tree/2.2.x)

```bash
conda install -c conda-forge jupyterlab  #conda-forge: a open source channel name.
jupyter lab
```

### jupyter robot extension installation ###
[jupyter robot extension installtion guide](https://robots-from-jupyter.github.io/public/static/RobotLab-Workshop_2019-01-16-596135ce8f63423ca3dbcc6fac336e2c.pdf)


```bash
conda install -c conda-forge nodejs jupyterlab robotframework-seleniumlibrary geckodriver python-chromedriver-binary
pillow lunr

pip install robotkernel robotframework-seleniumscreenshots nbimporter

jupyter labextension install jupyterlab_robotmode
jupyter labextension install jupyterlab_robotmode@2.4.0  #recommend use this, latest version seems no syntax highlighting

jupyter labextension install @jupyter-widgets/jupyterlab-manager

jupyter lab
```

### install jupyterlab examples ###
[jupyterlab examples](https://github.com/jupyterlab/extension-examples)


from git readme:
```
> The examples currently target JupyterLab 2.x.
If you would like to use the examples with JupyterLab 1.x, check out the 1.x branch.
Note that the 1.x branch is not updated anymore.
```

---------



```bash
git clone https://github.com/jupyterlab/extension-examples.git jupyterlab-extension-examples && \
  cd jupyterlab-extension-examples && \
  conda env create && \
  conda activate jupyterlab-extension-examples && \
  cd basics/hello-world && \
  jlpm && \
  jlpm run build && \
  jupyter labextension install . && \
  jupyter lab

(jupyterlab-extension-examples) zhaoting@M-C02Q90LGFVH6:~/Documents/xxxx/jpyter/jupyterlab-extension-examples$ jupyter lab --version
2.1.5
```

### create our own jupyterlab extension ####
ref:https://jupyterlab.readthedocs.io/en/stable/developer/extension_dev.html

#### create own env

```bash
conda create  jupyterlab-zyt-test
conda activate  jupyterlab-zyt-test
```

1 create extension with cookiecutter
[extension-cookiecutter-ts](https://github.com/jupyterlab/extension-cookiecutter-ts)

```bash
pip install cookiecutter

cookiecutter https://github.com/jupyterlab/extension-cookiecutter-ts --checkout v2.0
```

2 add code in your index.ts
before import, you should use commands as follows to install some package you used:

```bash
jlpm add @jupyterlab/filebrowser
jlpm add @jupyterlab/application
```

3 test your ts file

```
npm install -g typescript
tsc test.ts
```


4  extension dev

[ extension dev guide](https://jupyterlab.readthedocs.io/en/stable/developer/extension_dev.html)


