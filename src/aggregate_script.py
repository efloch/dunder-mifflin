from src.config import *
from src.params import *
import src.extract_script as input


def aggregate_script(df_script, scope='season',
                     method='word_count', filter=None):
    """

    Args:
        scope (int): column to group line by
                    'id_episode' or 'season' or None if across all episodes
        method (int): 'word_count' or 'line'
    Returns:
        pd.DataFrame: aggregated and filtered DataFrame

    """
    if scope:
        to_group_by = ['speaker', scope]
    else:
        to_group_by = 'speaker'

    if method == 'word_count':
        df_aggregated = df_script.groupby(by=to_group_by, as_index=False)[
            'word_count'].sum()
        df_aggregated.rename(
            columns={'word_count': 'word_count'}, inplace=True)

    else:
        df_aggregated = df_script.groupby(by=to_group_by, as_index=False)[
            'line_text'].count()
        df_aggregated.rename(columns={'line_text': 'line_count'}, inplace=True)

    if filter:
        for key in filter:
            assert key in df_aggregated, f"Cannot filter by {key}"
            df_aggregated = df_aggregated[df_aggregated[key].isin(filter[key])]

    return df_aggregated


if __name__ == '__main__':
    df_script = input.load_script(no_spoil_season=7, no_spoil_episode=16)
    df = aggregate_script(
        df_script, scope='season', method='line',
        filter={'season': [1, 2, 3, 4, 5, 6, 7], 'speaker': ['Pam', 'Jim']})
    print(df)
