from src.params import *
from src.utils import *
# from src.extract_script import load_script
logger = get_logger(__name__)


def get_sentiment_score(line):
    """
    Get sentiment score for the line
    Args:
        line (str): text of the line
    Returns:
        Sentiment score between -1 and 1 using textblob sentiment lexicon
    """
    score = textblob.TextBlob(line).sentiment.polarity
    score = round(float(score), 2)
    return score


def extract_mentions(line_tokens, names_list=NAMES_LIST+NICKNAMES):
    """
    Get characters mentioned in the line
    Args:
        line (str): text of the line in tokens
    Returns:
        list(str): list of character mentioned
    """
    mentions = []
    for name in names_list:
        name_lo = name.lower()
        if name_lo in line_tokens:
            mentions.append(name)
    return mentions


def line_analysis(df):
    """
    Analyze the lines by getting the charcter mentionned and the sentiment
    score of each line
    Args:
        df (DataFrame): Dataframe that contains the columns
                            ['tokenized_line', 'clean_line']

    Returns:
        list(str): list of character mentioned
    """
    logger.info(f"Analyzing lines")
    df['word_count'] = df['tokenized_line'].apply(len)
    logger.info(f"Getting sentiment scores")
    df['sentiment_score'] = df['clean_line'].apply(get_sentiment_score)
    logger.info(f"Extracting mentions")
    df['mentions'] = df['tokenized_line'].apply(extract_mentions)
    return df
