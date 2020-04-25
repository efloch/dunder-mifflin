from src.params import *
from src.config import *
import src.extract_script as input
import src.aggregate_script as script


def speakers_with_most_presence(df_script, most_of='line', top_speakers=10
                                scope=None, filter=None):
    """
    Get the top speakers, ranked by the count of line or word

    Args:
        df_script (pd.DataFrame): dataset containing one line per row
        scope (int): column to group line or words by
                    'id_episode' or 'season' or None for all series
        most_of (int): what measure to rank based on, 'word' or 'line'
        top_n (int) : number of speaker to return
        filter (dict): dict of filters
                        {column_to_filter -> list_of_values_to_keep}
                        ex. {'season' :[1,2,3], 'speaker':['Jim']}

    Returns:
        pd.DataFrame: top speakers with respective count of line or words
    """

    df_agg = script.aggregate_script(
        df_script, scope=scope, method=most_of, filter=filter)
    df_agg = df_agg.sort_values(by=f'{most_of}_count', ascending=False)
    return df_agg.head(top_n)


def ep_or_season_with_most_presence_for(df_script, speaker, scope=None, filter=None):
    """
    Get the episode or season, ranked by the count of line or word
    for one speaker

    Args:
        df_script (pd.DataFrame): dataset containing one line per row
        scope (int): 'id_episode' or 'season'
        most_of (int): what measure to rank based on, 'word' or 'line'
        filter (dict): dict of filters
                        {column_to_filter -> list_of_values_to_keep}
                        ex. {'season' :[1,2,3], 'speaker':['Jim']}

    Returns:
        pd.DataFrame: aggregated and filtered DataFrame
    """
    df_agg = script.aggregate_script(
        df_script, scope=scope, method=most, filter=filter)
    df_agg = df_agg.sort_values(by=scope, ascending=False)
    return df_agg


if __name__ == '__main__':
    df_script = input.load_script(no_spoil_season=7, no_spoil_episode=15)
    speaker_with_most_presence(
        df_script, scope='season', filter={'season': [4]})
