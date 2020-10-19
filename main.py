from glob import glob
from itertools import zip_longest
import configparser

import pandas as pd
import d6tstack.combine_csv
from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool


# load config
cfg = configparser.ConfigParser()
cfg.read('config.ini')

# db config
cfg_uri_psql = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(cfg["db"]["user"], cfg["db"]["passwd"], cfg["db"]["host"], cfg["db"]["port"], cfg["db"]["db"])

# function: group file_list in chunks
def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

# function: parse column datetime with pandas
def apply(dfg):
    dfg['timestamp'] = pd.to_datetime(dfg['timestamp'], cache=True, errors='coerce')
    return dfg

# funktion: parse csv and append to db
def combine_csv(files):
    d6tstack.combine_csv.CombinerCSV(
            files,
            sep=';',
            columns_select=['sensor_id','sensor_type','location','lat','lon','timestamp','P1','P2','temperature','humidity'],
            apply_after_read=apply,
            add_filename=False
        ).to_psql_combine(
            cfg_uri_psql, 
            'archive', 
            if_exists='append'
        )


if __name__ == '__main__':
    # select all csv files in folder and split it in chunks
    file_list = list(glob(cfg["data"]["folder"])) 
    filechunk_list = grouper(5000, file_list)
    
    # initalize pool
    pool = ThreadPool(6)
    
    # parse csv and append to db
    pool.map(combine_csv, filechunk_list)
    pool.close()
    pool.join()