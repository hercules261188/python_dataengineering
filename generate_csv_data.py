"""
Generate random data with Faker and save as CSV. You can specify list of rows and type.
The data type should be valid provider from Faker library.
Faker Library: https://faker.readthedocs.io/en/master/index.html

"""
from faker import Faker
import csv
import os
import logging
import tempfile

logging.basicConfig(level = os.getenv("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

# Specify data schema as column name and Faker type as tuple
SCHEMA = [ ("name", "name"), ("company", "company"), ("phone", "phone_number") ]
TOTAL_RECORDS = 5
OUTFILE_HOME = None
OUTFILE_NAME = None
OUTFILE_HOME = "/Users/apple/TEST/DataEngineeringPython/01"
OUTFILE_NAME = "sample.csv"

def generate(schema=SCHEMA, total_rcords=TOTAL_RECORDS, output_file_name=OUTFILE_NAME, output_home=OUTFILE_HOME):
    """
    Generate random dataset.
    :param schema:
    :param total_rcords:
    :param output_file_name:
    :param output_home:
    :return: File name
    """
    output_file = tempfile.NamedTemporaryFile().name + ".csv"
    if output_file_name and output_home :
        output_file = os.path.join(output_home, output_file_name)
    if os.path.isfile(output_file):
        log.warning(f"File {output_file} already exists, thus deleting it.")
        os.remove(output_file)

    log.info(f"Creating CSV data in file {output_file}.")
    log.debug(f"Schema: {schema}.")
    log.debug(f"Total records: {total_rcords}.")
    f = Faker()

    try:
        fh = open(output_file, 'w')
        csvw = csv.writer(fh)
        hdr = [k for k, v in schema]
        hdr.insert(0, "id")
        log.debug(f"Header {hdr}")
        csvw.writerow(hdr)
        for i in range(total_rcords):
            row = [i]
            for k, v in schema:
                row.append(f.__getattr__(v)())
            log.debug(f"Row: {row}")
            csvw.writerow(row)
    except Exception as e:
        log.error("Operation failed")
        log.error(e)
        output_file = None
    finally:
        log.info(f"Complete!")
        fh.close()
    return output_file

def read_csv(file_name):
    """
    Read a csv file
    :param file_name:
    :return: None
    """

    if not os.path.isfile(file_name):
        log.error(f"File {file_name} does not exist.")

    fh = open(file_name)
    fr = csv.DictReader(fh)
    log.info(f"Starting to read csv file {file_name}.")
    hdr = fr.fieldnames
    log.info(f"Schema found: {hdr}")
    for r in fr:
        row = []
        for i in range(len(hdr)):
            c = hdr[i]
            log.debug(f"{c}: {r[c]}")
            row.append(f"{c}: {r[c]}")
        log.info(row)

if __name__ == '__main__':

    file_nm = generate()
    read_csv(file_nm)






