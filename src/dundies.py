from src.params import *
from src.config import *
import src.extract_script as input
import src.aggregate_script as script


def speaker_with_most_line_or_word(df_script, most_of='line', scope=None, filter=None):
    df_agg = script.aggregate_script(
        df_script, scope=scope, method=most_of, filter=filter)
    df_agg = df_agg.sort_values(by=f'{most_of}_count', ascending=False)
    print(df_agg.head(10))


def ep_or_seas_with_most_line_for(df_script, speaker, scope=None, filter=None):
    df_agg = script.aggregate_script(
        df_script, scope=scope, method=most, filter=filter)
    df_agg = df_agg.sort_values(by=scope, ascending=False)
    print(df_agg.head(10))


def season_with_most_line_for(df_script, scope=None, filter=None):
    pass


if __name__ == '__main__':
    df_script = input.load_script(no_spoil_season=7, no_spoil_episode=15)
    speaker_with_most_line_or_word(
        df_script, scope='season', filter={'season': [4]})
