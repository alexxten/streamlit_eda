from sqlalchemy import BigInteger, Column, Double, MetaData, Table, Text
from sqlalchemy.orm.base import Mapped

metadata = MetaData()


t_d_clients = Table(
    'd_clients', metadata,
    Column('id', BigInteger),
    Column('age', BigInteger),
    Column('gender', BigInteger),
    Column('education', Text),
    Column('marital_status', Text),
    Column('child_total', BigInteger),
    Column('dependants', BigInteger),
    Column('socstatus_work_fl', BigInteger),
    Column('socstatus_pens_fl', BigInteger),
    Column('reg_address_province', Text),
    Column('fact_address_province', Text),
    Column('postal_address_province', Text),
    Column('fl_presence_fl', BigInteger),
    Column('own_auto', BigInteger)
)


t_d_close_loan = Table(
    'd_close_loan', metadata,
    Column('id_loan', BigInteger),
    Column('closed_fl', BigInteger)
)


t_d_job = Table(
    'd_job', metadata,
    Column('gen_industry', Text),
    Column('gen_title', Text),
    Column('job_dir', Text),
    Column('work_time', Double(53)),
    Column('id_client', BigInteger)
)


t_d_last_credit = Table(
    'd_last_credit', metadata,
    Column('credit', Double(53)),
    Column('term', BigInteger),
    Column('fst_payment', Double(53)),
    Column('id_client', BigInteger)
)


t_d_loan = Table(
    'd_loan', metadata,
    Column('id_loan', BigInteger),
    Column('id_client', BigInteger)
)


t_d_pens = Table(
    'd_pens', metadata,
    Column('id', BigInteger),
    Column('flag', BigInteger),
    Column('comment', Text)
)


t_d_salary = Table(
    'd_salary', metadata,
    Column('family_income', Text),
    Column('personal_income', Double(53)),
    Column('id_client', BigInteger)
)


t_d_target = Table(
    'd_target', metadata,
    Column('agreement_rk', BigInteger),
    Column('id_client', BigInteger),
    Column('target', BigInteger)
)


t_d_work = Table(
    'd_work', metadata,
    Column('id', BigInteger),
    Column('flag', BigInteger),
    Column('comment', Text)
)
