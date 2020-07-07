from src.params import *
from src.utils import load_raw
import src.process_script.aggregate_script as agg
import src.process_script.line_analysis as line
import src.process_script.process_lines as process
logger = get_logger(__name__)


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
    logger.info(f"Processing script until S{no_spoil_season}E{no_spoil_episode}")

    df = load_raw('the_office_scene.csv')

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
