from src.process_script.process_script import load_script
from src.process_script.aggregate_script import get_all_counts
from src.utils import save_processed


def main():
    df_script = load_script(process_lines=True, analysis=True)
    save_processed(df_script, "processed_script.csv")

    df_agg = get_all_counts(df_script)
    save_processed(df_agg, "all_counts.csv")


if __name__ == "__main__":
    main()
