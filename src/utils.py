from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import os
import re
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
import textblob
import logging


dirname, filename = os.path.split(os.path.abspath(__file__))
DATA_PATH = os.path.join(dirname, '../data/')
RAW_PATH = os.path.join(DATA_PATH, 'raw/')
PROCESSED_PATH = os.path.join(DATA_PATH, 'processed/')


# ====== LOGGING ====================================

def get_logger(logger_name):
    root = logging.getLogger(logger_name)
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root


logger = get_logger(__name__)


def load_raw(filename):
    logger.info(f"Loading {filename}")
    inpath = os.path.join(RAW_PATH, filename)
    return pd.read_csv(inpath)


def save_processed(df, filename):
    logger.info(f"Saving {filename}")
    outpath = os.path.join(PROCESSED_PATH, filename)
    df.to_csv(outpath)
