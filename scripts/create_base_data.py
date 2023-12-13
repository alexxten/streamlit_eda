import os

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import *
from vars import ROOT_DIR
from vars.envars import DB_PASSWORD, DB_NAME, DB_USER, POSTGRES_PORT, POSTGRES_HOST

if __name__ == '__main__':
    engine = create_engine(
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}',
    )
    Session = sessionmaker(engine)
    with Session() as session:
        query = session.query(
            t_d_target,
            t_d_clients,
            t_d_salary,
            t_d_loan,
            t_d_close_loan,
        )
        query = query.join(t_d_clients, t_d_target.c.id_client == t_d_clients.c.id)
        query = query.join(t_d_salary, t_d_target.c.id_client == t_d_salary.c.id_client)
        query = query.outerjoin(t_d_loan, t_d_target.c.id_client == t_d_loan.c.id_client)
        query = query.outerjoin(
            t_d_close_loan,
            t_d_loan.c.id_loan == t_d_close_loan.c.id_loan,
        )
        records = query.all()
    records = [r._asdict() for r in records]
    df = pd.DataFrame(records)
    df.columns = map(str.upper, df.columns)
    df.to_csv(
        os.path.join(ROOT_DIR, 'datasets', 'prepared', 'base_data.csv'),
        index=False,
    )

