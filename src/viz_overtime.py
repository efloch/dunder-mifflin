from src.params import *
from src.config import *
import src.extract_script as input
import src.aggregate_script as script


def line_plot(df_script, speaker_list, scope, to_plot='line'):
    """
    Create line plot for the word count or line count by speaker_list

    Args:
        df_script (pd.DataFrame): table with all lines
        speaker_list (list(str)): list of speaker to plot
        scope (str): 'season' or 'id_episode' or None for all series
        to_plot (str): 'line' for number of lines, 'word' for number of words
    """
    # Aggregate lines or words by speaker
    df_agg = script.aggregate_script(df_script, scope=scope, method=to_plot,
                                     filter={'speaker': speaker_list})

    # Plot one line per speaker
    for speaker in speaker_list:
        data = df_agg[df_agg['speaker'] == speaker]
        sns.lineplot(x=scope, y=f"{to_plot}_count", data=data, label=speaker)
    plt.ylabel(f"Count of {to_plot} by {scope}")
    plt.xticks(rotation=20)
    plt.show()


if __name__ == '__main__':
    df_script = input.load_script(no_spoil_season=7, no_spoil_episode=15)
    line_plot(df_script, ['Jim', 'Pam', 'Dwight'], to_plot='word',
              scope='id_episode')

    line_plot(df_script, ['Jim', 'Pam', 'Dwight'], to_plot='line',
              scope='id_episode')
