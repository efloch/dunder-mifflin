from src.params import *
from src.config import *


def get_script_data(save=False):
    """
    Reads in script data file, extract season, episode number, episodes
    title, and each line.

    Returns extracted info in pd.DataFrame
    """
    df_script = pd.read_csv(os.path.join(
        DATA_PATH, 'raw/office_transcript.csv'), header=None, sep='\n')

    # Extract episode info
    df_episodes_info = df_script[0].str.extract(
        r'(?P<season>\d*)x(?P<episode>[^-]*) - (?P<title>[^;]*);')

    # Split episode into all episodes
    df_split_script = df_script[0].str.split(
        r'\d*x[^-]*- [^;]*;', expand=True)
    df_split_script.drop(0, 1, inplace=True)

    # Concat info and lines
    df_script = pd.concat([df_episodes_info, df_split_script], axis=1)
    if save:
        df_script.to_csv(os.path.join(
            DATA_PATH, 'intermediary/script_structure.csv'), index=False)
    return df_script


def clean_lines_data(df):
    """
    Takes in extracted info about all episodes and
    exract the character and text of each line and clean the string

    Returns clean dataframe with all line in order
    """
    df = df.set_index(['season', 'episode', 'title'])
    df_script = df.stack().reset_index()
    df_script.rename(columns={'level_3': 'order', 0: 'text'}, inplace=True)
    line = df_script['text'].str.split(r':', n=1, expand=True)
    df_script['character'] = line[0].str.rstrip(',')
    df_script['text'] = line[1].replace(
        ',"', '', regex=True).replace('"', '', regex=True).str.rstrip(',')
    return df_script


if __name__ == '__main__':
    df = get_script_data()
    df_clean = clean_lines_data(df)
    df_clean.to_csv(os.path.join(
        DATA_PATH, 'intermediary/script_clean.csv'), index=False)
