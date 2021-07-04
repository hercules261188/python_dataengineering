"""
Generate random data with Faker and save as JSON. You can specify list of rows and type.
The data type should be valid provider from Faker library.
Faker Library: https://faker.readthedocs.io/en/master/index.html

"""
from faker import Faker
import json
import os
import logging
import tempfile

logging.basicConfig(level = os.getenv("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

# Specify data schema as column name and Faker type as tuple
SCHEMA = [ ("name", "name"), ("city", "city"), ("salary", "random_int") ]
TOTAL_RECORDS = 5
OUTFILE_HOME = None
OUTFILE_NAME = None
OUTFILE_HOME = "/Users/apple/TEST/DataEngineeringPython/01"
OUTFILE_NAME = "sample.json"

def generate(schema=SCHEMA, total_rcords=TOTAL_RECORDS, output_file_name=OUTFILE_NAME, output_home=OUTFILE_HOME):
    """
    Generate random dataset.
    :param schema:
    :param total_rcords:
    :param output_file_name:
    :param output_home:
    :return: File name
    """
    output_file = tempfile.NamedTemporaryFile().name + ".json"
    if output_file_name and output_home :
        output_file = os.path.join(output_home, output_file_name)
    if os.path.isfile(output_file):
        log.warning(f"File {output_file} already exists, thus deleting it.")
        os.remove(output_file)

    log.info(f"Creating JSON data in file {output_file}.")
    log.debug(f"Schema: {schema}.")
    log.debug(f"Total records: {total_rcords}.")
    f = Faker()

    try:
        fh = open(output_file, 'w')
        jsn = {}
        jsn["data"] = []
        for i in range(total_rcords):
            do = { "id": i }
            for k, v in schema:
                do[k] = f.__getattr__(v)()
            log.debug(f"Object: {do}")
            jsn["data"].append(do)
        log.debug(jsn)
        json.dump(jsn, fh)
    except Exception as e:
        log.error("Operation failed")
        log.error(e)
        output_file = None
    finally:
        log.info(f"Complete!")
        fh.close()
    return output_file

def read_json(file_name, schema=SCHEMA):
    """
    Read a JSON file
    :param file_name:
    :param schema:
    :return: None
    """

    if not os.path.isfile(file_name):
        log.error(f"File {file_name} does not exist.")

    log.info(f"Starting to read JSON file {file_name}.")
    fh = open(file_name)
    jd = json.load(fh)
    for d in jd['data']:
        row = []
        for se in schema:
            row.append(d[se[0]])
        log.info(f"Row: {row}")


if __name__ == '__main__':

    file_nm = generate()
    read_json(file_nm)






