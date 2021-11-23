import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db_generator import Base, FileData, MetaData, WindExtreme
from cli_parser import parser
from logger import getgglogger


logger = getgglogger(__name__)


def file_already_processed(hash_digest):
    return dbsession.query(FileData).filter(FileData.hash_digest == hash_digest).count() == 1


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        # session.commit()
        return instance


if __name__ == "__main__":
    # capture filenames and options from cli
    args = parser.parse_args()

    engine = create_engine(f"sqlite+pysqlite:///{os.path.join(args.db_path, args.db_filename)}", echo=False, future=True)
    log_folder = args.log_folder

    Base.metadata.create_all(engine)

    dbsession = Session(engine)

    from datfile_reader import DatFile, filetype_re_rule

    # cycles all logfiles in log_folder
    for filename in os.listdir(log_folder):
        logger.debug(f'Reading {filename}')
        filetype_re = filetype_re_rule.match(filename)

        metadata_object = get_or_create(
            dbsession, MetaData,
            instrument_model='Wind Extreme',
            serial='',
            location='testa grigia',
            firmware_rev='',
            software_rev=''
        )

        if filetype_re:
            logger.debug(f'processing {filename}')
            datfile = DatFile(
                os.path.join(log_folder, filename),
            )
            if not file_already_processed(datfile.hash_digest):
                logger.debug(f'{filename} not already processed')
                file_header, data = datfile.file_header, datfile.data
                # look for MetaData, and add if not present
                # for each line in data, add a EDM264_C entry
                file_data = FileData(filename=filename, hash_digest=datfile.hash_digest)
                dbsession.add(file_data)
                dbsession.flush()

                for data_row in data:
                    data_row_instance = WindExtreme(
                        datetime=data_row[0],
                        file_data=file_data.id,
                        data_metadata=metadata_object.id,

                        speed=data_row[1],
                        direction=data_row[2],
                        state=data_row[3],
                    )
                    dbsession.add(data_row_instance)
    dbsession.commit()