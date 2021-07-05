"""
Use SQLAlchemy to access DB and run query as text.
"""

from sqlalchemy import create_engine, text
import logging
import os
import tempfile
from faker import Faker

logging.basicConfig(level = os.getenv("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

DB_FILE = None
TOTAL_RECORD = 5
CREATE_TABLE = """
CREATE TABLE TEST ( ID int, NAME string, SALARY int)
"""
INSERT_QUERY = """
INSERT INTO TEST VALUES ({0}, '{1}', {2})
"""
SELECT_QUERY = """
SELECT * FROM TEST
"""

def create_db(db_file=DB_FILE):

    if not db_file:
        db_file = tempfile.NamedTemporaryFile().name + ".db"

    try:
        log.info(f"Creating database in location {db_file}.")
        eng = create_engine(f"sqlite:///{db_file}", echo=False)
        return eng
    except Exception as e:
        log.error("Error in creating DB.")
        log.error(e)
        return None

def create_table(engine=None, sql=CREATE_TABLE):

    if not engine:
        log.error("No valid SQLAlchemy engine passed.")
        raise Exception("No valid SQLAlchemy engine passed.")

    log.info(f"Executing query - {sql}")
    r = engine.execute(text(sql))
    log.info(r)

def insert_data(engine=None):

    if not engine:
        log.error("No valid SQLAlchemy engine passed.")
        raise Exception("No valid SQLAlchemy engine passed.")

    f = Faker()
    for i in range(TOTAL_RECORD):
        engine.execute(
            text(
                INSERT_QUERY.format(i, f.name(), f.random_int())
            )
        )

def show_data(engine=None):

    if not engine:
        log.error("No valid SQLAlchemy engine passed.")
        raise Exception("No valid SQLAlchemy engine passed.")

    r = engine.execute(
            text(
                SELECT_QUERY
            )
        )

    result_set = r.fetchall()
    log.info(f"Total row fetched is {len(result_set)}.")

    log.info("Fetching rows by position.")
    # Positional fetch
    for sr in result_set:
        log.info(f"{sr[0]}, {sr[1]}, {sr[2]}")

    log.info("Fetching rows by name.")
    # Named fetch
    col_lst = ['id', 'name', 'salary']
    for sr in result_set:
        nm_row = dict(zip(col_lst, sr))
        log.info(nm_row)


if __name__ == '__main__':

    engine = create_db()
    if not engine:
        log.error("Unsuccessful in DB creation thus no action.")
    else:
        log.info("Successfully created DB.")
        try:
            create_table(engine)
            result = insert_data(engine)
            show_data(engine)
        except Exception as e:
            log.error("Exception occured while processing.")
            log.error(e)


