import argparse

parser = argparse.ArgumentParser(description='Process wind extreme logfiles into a sqlite database')

parser.add_argument("-l", "--log-folder", dest="log_folder",
                    help="log folder", type=str, default='log_folder')
parser.add_argument("-p", "--db-path", dest="db_path",
                    help="database path (could be relative to the working folder or absolute)", type=str, default='database/')
parser.add_argument("-f", "--db-filename", dest="db_filename",
                    help="database filename", type=str, default='db.sqlite')
