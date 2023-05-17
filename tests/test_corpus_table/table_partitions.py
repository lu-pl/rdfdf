"""corpusTable row partitions for isolated testing
"""

import pandas as pd

corpus_table = pd.read_excel("./corpusTable_prep.xlsx", engine="openpyxl")

# partitions
rem_partition = corpus_table.loc[corpus_table["corpusAcronym"] == "ReM"]

greekdracor_partition = corpus_table.loc[corpus_table["corpusAcronym"] == "GreekDraCor"]

fredracor_partition = corpus_table.loc[corpus_table["corpusAcronym"] == "FreDraCor"]
