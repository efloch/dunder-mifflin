import src.aggregate_script as agg
import src.line_analysis as line
from src.params import *
from src.config import *
import src.process_lines as process
<< << << < HEAD
== == == =
>>>>>> > 08762344ed28b456112b89596fc94f86a50b8bc0


def get_episode_info(save=False):
    """
    Reads in script data file, extract season, episode number, episodes
    title, and each line.

    Returns extracted info in pd.DataFrame
    """
    df_script = pd.read_csv(os.path.join(
        DATA_PATH, 'raw/office_transcript.csv'), header=None, sep='\n')

    # Extract episode info
    df_episodes_info = (df_script[0].str.extract(
        r'(?P<season>\d*)x(?P<episode>[^-]*) - (?P<title>[^;]*);')
        .set_index(['season', 'title']))
    df_episodes_info.episode = df_episodes_info.episode.str.split('/').tolist()
    df_episodes_info = df_episodes_info.explode('episode')
    df_episodes_info.reset_index(inplace=True)

    df_episodes_info['id_episode'] = df_episodes_info['season'].astype(
        str) + df_episodes_info['episode'].apply(_val_episode)

    if save:
        df_script.to_csv(os.path.join(
            DATA_PATH, 'intermediary/episode_info.csv'), index=False)
    return df_episodes_info


def _val_episode(x):
    if '/' in x:
        x = str(x).split('/')[0]
    return x.zfill(2)


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


def load_script(no_spoil_season=9, no_spoil_episode=23,
                process_lines=True, analysis=True):
    """
    Reads in csv with one row per line

    Args:
        no_spoil_season (int): Last season seen
        no_spoil_episode (int): Last episode seen
        process_lines (bool): If true, enrich tables with cleaned lines,
                                tokenized line and word counts
    Returns:
        pd.DataFrame: dataset, filtered and/or enriched
    """
    df = pd.read_csv(os.path.join(
        DATA_PATH, 'raw/the_office_scene.csv'))

    df['id_episode'] = df['season'].astype(
        str).apply(str.zfill, args=(2,)) + df['episode'].astype(str).apply(str.zfill, args=(2,))

    df_episodes_info = get_episode_info()[['id_episode', 'title']]

    if no_spoil_episode:
        # Keep data only about the episode seen
        id_last_episode = df[(df['season'] == no_spoil_season)
                             & (df['episode'] == no_spoil_episode)].id_episode.values[0]
        df = df[df['id_episode'] <= id_last_episode]

    df = df.merge(df_episodes_info, on='id_episode')

    df = df[df['speaker'].isin(NAMES_LIST)]

    if process_lines:
        df = process.process_lines(df)
        if analysis:
            df = line.line_analysis(df)

            df = df.explode('mentions')

    return df


if __name__ == '__main__':
    # To load pre-cleaned csv
<< << << < HEAD
df = load_script(
    process_lines=True, analysis=True)
== == == =
df = load_script()
>>>>>> > 08762344ed28b456112b89596fc94f86a50b8bc0
df.to_csv(os.path.join(DATA_PATH, 'processed/processed_script.csv'))
print(df)
