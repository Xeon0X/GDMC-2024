# GDMC-2024
A procedural city generator for Minecraft as part of the GDMC 2024 competition. 

## Run

Install required packages using `pip`:
```bash
pip install -r requirements.txt
```

Run `main.py`.

## Dev 

First, setup your virtual environment using Python's built-in venv.

Install `pipreqs`:
```bash
pip install pipreqs
```

Run `pipreqs --ignore .venv --force` to generate an updated list of dependencies for the project in requirements file. Note that you should then change `skimage==...` by `scikit-image==0.23.2`.