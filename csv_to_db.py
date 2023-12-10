import os

import pandas as pd
from sqlalchemy import create_engine

from envars import DB_PASSWORD, DB_NAME, DB_USER, POSTGRES_PORT, POSTGRES_HOST


if __name__ == '__main__':
    datasets_dir = 'datasets'
    datasets = [f for f in os.listdir(datasets_dir) if '.csv' in f]
    engine = create_engine(
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}',
    )
    for f in datasets:
        df = pd.read_csv(f'{datasets_dir}/{f}', sep=',')
        df.to_sql(f'{f.split(".")[0].lower()}', engine)
