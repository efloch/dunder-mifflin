from src.config import *
from src.params import *
import src.extract_script as input
import src.process_lines as process

SCOPE_ID_COLS = {'id_episode': ['speaker', 'season', 'id_episode'],
                 'season': ['speaker', 'season'],
                 'all': 'speaker'}


def filter_script(df_script, filters):
    """
    Takes in a df and queries only the values specified in the
    filter dictionary
    Args:
        filter (dict): dict of filters
                    {column_to_filter -> list_of_values_to_keep}
                    ex. {'season' :[1,2,3], 'speaker':['Jim']}
    """
    if filters:
        for key in filters:
            # Make sure filter column are in the dataframe
            assert key in df_script, f"Cannot filter by {key}"
            df_script = df_script[df_script[key].isin(filters[key])]
    return df_script


def add_normalized_count(df_aggregated, scope, method):
    """
    Takes in a script df, with <method> aggregated by <scope> and speaker
    Add a the normalized count of word or line by episode or season
    Args:
        df_script (pd.DataFrame): table with the script aggregated by speaker
        scope (int): column to group line or words by
                    'id_episode' or 'season' or None for all series
        method (int): 'word' or 'line'
    Returns:
        pd.DataFrame: df with added normalized column
    """

    if scope in ['id_episode', 'season']:
        df_total_by_scope = df_aggregated.groupby(scope, as_index=False)[f'{method}_count'].sum()
        df_total_by_scope.rename(
            columns={f'{method}_count': f'total_{method}_count_{scope}'}, inplace=True)
        df_aggregated = df_aggregated.merge(df_total_by_scope, on=scope)
        df_aggregated[f'norm_{method}_count'] = df_aggregated[f'{method}_count'] / \
            df_aggregated[f'total_{method}_count_{scope}']
    else:
        df_aggregated[f'total_{method}_series'] = df_aggregated[f'{method}_count'].sum()
        df_aggregated[f'norm_{method}_count'] = df_aggregated[f'{method}_count'] / \
            df_aggregated[f'total_{method}_series']

    return df_aggregated


def aggregate_script(df_script, scope='season',
                     method='word', filter=None):
    """
    Aggregate lines or words by season, episode or across all series

    Args:
        df_script (pd.DataFrame): dataset containing one line per row
        scope (int): column to group line or words by
                    'id_episode' or 'season' or 'all' for all series
        method (int): 'word' or 'line'
        filter (dict): dict of filters
                        {column_to_filter -> list_of_values_to_keep}
                        ex. {'season' :[1,2,3], 'speaker':['Jim']}
    Returns:
        pd.DataFrame: aggregated and filtered DataFrame

    """
    # Mapping from scope to column to group by
    to_group_by = SCOPE_ID_COLS[scope]

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

    df_normalized_agg = add_normalized_count(df_aggregated, scope, method)

    df_results = filter_script(df_normalized_agg, filter)

    return df_results


def get_all_counts(df_script):

    df_speakers = df_script[['speaker', 'season',
                             'id_episode']].drop_duplicates()

    for scope in ['id_episode', 'season', 'all']:
        for method in ['word', 'line']:
            df_agg = aggregate_script(
                df_script, scope, method)
            df_agg.to_csv(os.path.join(DATA_PATH, f'processed/{scope}_{method}_counts.csv'))

            df_agg.rename(columns={f'{method}_count': f'{method}_count_{scope}',
                                   f'norm_{method}_count': f'n_{method}_count_{scope}'},
                          inplace=True)

            df_speakers = df_speakers.merge(
                df_agg, on=SCOPE_ID_COLS[scope])

    return df_speakers


if __name__ == '__main__':
    df_script = input.load_script(no_spoil_season=7, no_spoil_episode=16)
    df_episode = aggregate_script(
        df_script, scope='id_episode', method='word')

    df = get_all_counts(df_script)
    df.to_csv(os.path.join(DATA_PATH, 'processed/all_counts.csv'))
    print(df.head(5))
