from src.config import *
from src.params import *
import src.extract_script as input
import src.process_lines as process


def aggregate_script(df_script, scope='season',
                     method='word', filter=None):
    """
    Aggregate lines or words by season, episode or across all series

    Args:
        df_script (pd.DataFrame): dataset containing one line per row
        scope (int): column to group line or words by
                    'id_episode' or 'season' or None for all series
        method (int): 'word' or 'line'
        filter (dict): dict of filters
                        {column_to_filter -> list_of_values_to_keep}
                        ex. {'season' :[1,2,3], 'speaker':['Jim']}
    Returns:
        pd.DataFrame: aggregated and filtered DataFrame

    """

    if scope:
        # If scope is season or episode, will group by speaker and scope
        to_group_by = ['speaker', scope]
    else:
        # If no scope, group over all series (grouping only speaker in this case)
        to_group_by = 'speaker'

    if method == 'word':
        # Sum total number of words across all lines
        df_aggregated = df_script.groupby(by=to_group_by, as_index=False)[
            'word_count'].sum()
        df_aggregated.rename(
            columns={'word_count': 'word_count'}, inplace=True)

    else:
        # Count number of lines
        df_aggregated = df_script.groupby(by=to_group_by, as_index=False)[
            'line_text'].count()
        df_aggregated.rename(columns={'line_text': 'line_count'}, inplace=True)

    if filter:
        # If filters are specified
        for key in filter:
            # Make sure filter column are in the dataframe
            assert key in df_aggregated, f"Cannot filter by {key}"
            df_aggregated = df_aggregated[df_aggregated[key].isin(filter[key])]

    return df_aggregated


if __name__ == '__main__':
    df_script = input.load_script(no_spoil_season=7, no_spoil_episode=16)
    df = aggregate_script(
        df_script, scope='season', method='word',
        filter={'season': [1, 2, 3, 4, 5, 6, 7], 'speaker': ['Pam', 'Jim']})
    print(df)
