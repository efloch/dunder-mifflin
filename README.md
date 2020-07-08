## Module to clean and analyze The Office (U.S.) scripts

### How to use 

Download the raw scripts from this link https://docs.google.com/spreadsheets/d/18wS5AAwOh8QO95RwHLS95POmSNKA2jjzdt0phrxeAE0/edit#gid=747974534
into the data/raw/ folder 

In the root folder, run 
'python -m run'


The script will be loaded, analyses and key statistics will be saved into the data/processed/ folder.

### The process 

- The data is first loaded and episode name are added to the raw table (process_script.py)
- Then each line is broken down into tokens, and words are counted (breakdown_line.py)
- Each line is processed to extract its sentiment score and the characters mentioned (analyze_line.py)
- The processed and anaylzed line are saved in "processed_script.csv"
- Finally, word and line counts are aggregated into different files and one master table is saved under "all_counts.csv"

