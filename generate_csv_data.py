"""
Generate random data with Faker and save as CSV.
"""
from faker import Faker
import csv
import os
import logging

logging.basicConfig(level = os.getenv("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

# Specify data schema as column name and Faker type as tuple
SCHEMA = [ ("name", "name"), ("company", "company"), ("phone", "phone_number") ]
TOTAL_RECORDS = 5
OUTFILE_HOME = "/Users/apple/TEST/DataEngineeringPython/01"
OUTFILE_NAME = "sample_data_01.csv"

def generate(schema=SCHEMA, total_rcords=TOTAL_RECORDS, output_file_name=OUTFILE_NAME, output_home=OUTFILE_HOME):
    """
    Generate random dataset.
    :param schema:
    :param total_rcords:
    :param output_file_name:
    :param output_home:
    :return: None
    """
    output_file = os.path.join(output_home, output_file_name)
    if os.path.isfile(output_file):
        log.warning(f"File {output_file} already exists, thus deleting it.")
        os.remove(output_file)


    log.info(f"Creating CSV data in file {output_file}.")
    log.debug(f"Schema: {schema}.")
    log.debug(f"Total records: {total_rcords}.")
    f = Faker()

    fh = open(output_file, 'w')
    csvw = csv.writer(fh)
    hdr = [ k for k, v in schema]
    log.debug(f"Header {hdr}")
    csvw.writerow(hdr)
    try:
        for i in range(total_rcords):
            row = [i]
            for k, v in schema:
                log.debug(f"Column {k}, Value: {f.__getattr__(v)()}.")
                row.append(f.__getattr__(v)())
            log.info(f"Row: {row}")
            csvw.writerow(row)
    finally:
        log.info(f"Completed operation.")
        fh.close()


if __name__ == '__main__':

    generate()






