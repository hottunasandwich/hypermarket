# HYPER MARKET
a place for trading goods p2p.

## Install
1. first step is to clone this repo `git clone https://github.com/hottunasandwich/hypermarket.git`
2. `cd hypermarket`
3. then you have to create a virtual environment with following commands -> for Windows `py -3 -m venv venv` for linux `python3 -m venv venv`
4. now install dependencies `pip3 install -e .`

now you are ready to go, just some minor configs left.

## Configuration
- create a `instace/config.py` file next to `setup.cfg` file as 
`ADMIN = {'USERNAME': 'PASSWORD'}] SECRET_KEY = 'A SECRET KEY'`
and replace *USERNAME*, *PASSWORD* and *SECRET_KEY* with what ever you want.
- create a `.gitignore` file in order not to push wrong stuff.

your _gitignore_ should look something like this.
```
venv/
*.pyc
__pycache__/
instance/
.cache/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.idea/
*.swp
*~
.vim
.gitignore
```