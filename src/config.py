from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
# nltk.download("stopwords")
import textblob


dirname, filename = os.path.split(os.path.abspath(__file__))
DATA_PATH = os.path.join(dirname, '../data/')
