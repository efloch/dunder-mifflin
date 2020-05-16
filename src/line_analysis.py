from src.params import *
from src.config import *
from src.extract_script import *


def get_sentiment_score(line):
    """

    Args:
        line (str):

    Returns:
        Sentiment score between -1 and 1 using textblob sentiment lexicon
    """
    score = textblob.TextBlob(line).sentiment.polarity
    score = round(float(score), 2)
    return score


def extract_mentions(line_tokens, names_list=NAMES_LIST+NICKNAMES):
    mentions = []
    for name in names_list:
        name_lo = name.lower()
        if name_lo in line_tokens:
            mentions.append(name)
    return mentions


def line_analysis(df):
    df['word_count'] = df['tokenized_line'].apply(len)
    df['sentiment_score'] = df['clean_line'].apply(get_sentiment_score)
    df['mentions'] = df['tokenized_line'].apply(extract_mentions)
    return df


if __name__ == '__main__':
    prep_df = load_script()
    analysis_df = line_analysis(prep_df)
    #print(analysis_df.head().to_string())
    #analysis_df.to_csv('../data/processed/analyzed_lines.csv', index=False, sep=';')
    for char in NAMES_LIST:
        print('Top 10 mentions from', char)
        df = analysis_df[analysis_df.speaker == char]
        mentions_agg = [m for l in df.mentions for m in l]
        print(pd.Series(mentions_agg).value_counts()[:10], '\n')