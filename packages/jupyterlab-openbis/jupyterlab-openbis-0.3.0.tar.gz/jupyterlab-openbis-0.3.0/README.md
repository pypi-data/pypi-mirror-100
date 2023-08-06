# JupyterLab openBIS extension

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fsissource.ethz.ch%2Fsispub%2Fjupyterlab-openbis/master?urlpath=lab)

## About

JupyterLab openBIS extension is a client-side extension for JupyterLab that enables connectivity with openBIS instances.

## Installing prebuilt extension (recommended)

```bash
pip install jupyterlab-openbis
```

## Installing source extension (requires Node.js)

1. Install jupyter-openbis-server (see <https://pypi.org/project/jupyter-openbis-server/>) to your Jupyter server
2. Install JupyterLab openBIS extension with command

```bash
jupyter labextension install jupyterlab-openbis@0.3.0
```

## Compatibility

| jupyterlab-openbis | jupyter-openbis-server | jupyterlab    |
| ------------------ | ---------------------- | ------------- |
| 0.3.x              | >=0.4.0                | >=3.0         |
| 0.2.x              | >=0.2.1                | >=2.0, <3.0   |
| 0.1.x              | >=0.2.1                | >=1.1.3, <2.0 |
