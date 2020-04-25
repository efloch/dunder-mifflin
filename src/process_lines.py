from src.params import *
from src.config import *
import src.extract_script as input


def clean_line(line):
    """
    Add
    """
    return line


def tokenize_line(line):
    """
    Takes in line and count words
    """
    return line


def token_non_stop_words(tokenized_line):
    return tokenized_line


def process_lines(df_script):
    """
    Takes in Dataframe script and process "line" column which
    contains the text of each lines
    - Clean the text (column clean_line)
    - Tokenize it (tokenized_line)
    - Add word count (word_count)
    - Get non stop words (tokenized_non_stop)
    """
    return df_script


if __name__ == '__main__':
    df_script = input.load_script()
    df = process_lines(df_script)
    print(df)
