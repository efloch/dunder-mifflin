import pandas as pd
import numpy as np
import os
import re
import string
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords

dirname, filename = os.path.split(os.path.abspath(__file__))
DATA_PATH = os.path.join(dirname, '../data/')
