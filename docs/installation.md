# Installation

## Simple installation

To set up `pyJudilibre`, you can install it from [PyPI](https://pypi.org/project/pyjudilibre).

```sh
pip install pyjudilibre
```

You can also install it directly from Github: 

```sh
git clone https://github.com/pauldechorgnat/pyJudilibre.git
cd pyJudilibre
pip install .
```

## Requirements

This library relies on:

- `pydantic>=2.10.2"`: [`pydantic` for typing](https://docs.pydantic.dev/latest/)
- `httpx==0.28.1`: [`httpx` for HTTP requests](https://www.python-httpx.org/)
- `tqdm==4.67.1`: [`tqdm` for progress bars](https://tqdm.github.io/)


## Extras

`pyJudilibre` comes with extras:

- `dev`: requirements to allow library development
- `build`: requirements to build the library
- `test`:  requirements to test the library
- `doc`: requirements to build the documentation of the library

For development purposes, it is advised to build a virtual environment called `venv`:

```sh
git clone https://github.com/pauldechorgnat/pyJudilibre.git
cd pyJudilibre

python3 -m venv venv
source venv/bin/activate

pip install '.[dev,build,test,doc]'
```

