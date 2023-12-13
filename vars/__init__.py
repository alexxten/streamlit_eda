import os

ROOT_DIR = os.path.abspath(os.curdir)

DATA_PREPARED = os.path.join(ROOT_DIR, 'datasets', 'prepared', 'data.csv')
STATIC = os.path.join(ROOT_DIR, 'static')
MODEL_WEIGHTS = os.path.join(ROOT_DIR, 'utils', 'model.pickle')
