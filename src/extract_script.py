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


def _val_episode(x):
    str_episode = str(x).split('/')
    return str_episode[0]


def get_extracted_script():
    """
    Takes in extracted info about all episodes and
    exract the character and text of each line and clean the string

    Returns clean dataframe with all line in order
    """
    df = get_script_data()
    df['id_episode'] = df['season'].astype(
        str) + df['episode'].apply(_val_episode)
    df = df.set_index(['id_episode', 'season', 'episode', 'title'])
    df_script = df.stack().reset_index()
    df_script.rename(columns={'level_3': 'order', 0: 'text'}, inplace=True)
    line = df_script['text'].str.split(r':', n=1, expand=True)
    df_script['character'] = line[0].str.rstrip(',')
    df_script['text'] = line[1].replace(
        ',"', '', regex=True).replace('"', '', regex=True).str.rstrip(',')
    return df_script


def load_script(no_spoil_season=9, no_spoil_episode=23):
    df = pd.read_csv(os.path.join(
        DATA_PATH, 'raw/the_office_scene.csv'))

    if no_spoil_episode:
        df['id_episode'] = df['season'].astype(str) + df['episode'].astype(str)
        id_last_episode = df[(df['season'] == no_spoil_season)
                             & (df['episode'] == no_spoil_episode)].id_episode.values[0]
        df = df[df['id_episode'] <= id_last_episode]
    return df


if __name__ == '__main__':
    # To clean old csv :
    # df_clean = get_extracted_script()
    # outpath = os.path.join(DATA_PATH, 'intermediary/')
    # if not os.path.exists(outpath):
    #     os.makedirs(outpath)
    # df_clean.to_csv(os.path.join(outpath, 'script_clean.csv'), index=False)

    # To load pre-cleaned csv
    df = load_script(no_spoil_season=7, no_spoil_episode=15)
    print(df)
