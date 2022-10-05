import datetime
import os
from pathlib import Path

from git import Repo, Actor

if os.getenv('WORKING_DIRECTORY'):
    os.chdir(str(Path(os.getenv('WORKING_DIRECTORY')).resolve()))

if not Path('.git').exists():
    Repo.init('.').close()

with Repo('.') as repo:
    author = Actor(
        os.getenv("GIT_ACTOR_NAME", "GitHub Action"),
        os.getenv("GIT_ACTOR_EMAIL", "action@github.com"))

    index = repo.index
    files = [str(p) for p in Path('.').glob('*') if not p.name.startswith('.')]
    if files:
        index.add(files)
        index.commit(f'auto commit {datetime.datetime.utcnow().isoformat()}', author=author, skip_hooks=True)
