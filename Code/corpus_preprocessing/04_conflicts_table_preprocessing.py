from pathlib import Path
import pandas as pd
from collections import Counter
import ast
import numpy as np



# TODO: maybe also merge Target_Challenge and Target_Council and rename other columns
def prepare_dataframe(original_confl_table):
    # input: dataframe output from 01_align_rst_conflict.py
    # create a conflict column, correct values in paragraph and sentence id, keep only columns needed, sort dataframe,
    # return prepared dataframe
    df = pd.read_csv(original_confl_table, index_col=0)
    df['A0_Negative_Evaluation'] = df['A0_Negative_Evaluation'].replace("_", "")
    df['B1_ChallengeType'] = df['B1_ChallengeType'].replace("_", "")
    df["Conflict_Type"] = df['A0_Negative_Evaluation'] + df['B1_ChallengeType']
    df["Conflict_Type"] = df["Conflict_Type"].replace("Direct_NegEvalChallenge", "Challenge")
    df["Conflict_Type"] = df["Conflict_Type"].replace("Indirect_NegEvalChallenge", "Challenge")
    df["Conflict_Type"] = df["Conflict_Type"].replace("", "_")
    df['paragraph_id'] = df['paragraph_id'].astype("Int64")
    df['speech_sentence_id'] = df['speech_sentence_id'].astype("Int64")
    # rename Conflicts columns
    df = df.drop('A0_Negative_Evaluation', axis=1)
    df = df.drop('B1_ChallengeType', axis=1)
    column_to_move = df.pop("Conflict_Type")
    # insert column with insert(location, column_name, column_value)
    df.insert(6, "Conflict_Type", column_to_move)
    df_sent_sm = df.sort_values(['filename', 'speech_sentence_id'], ascending=[True, True])

    return df_sent_sm





def main():
    conflicts_df = Path('../../Corpora/Annotated/Conflicts/main_conflicts_not_preprocessed.csv')
    df_sent = prepare_dataframe(conflicts_df) # prepare conflicts csv (merge Conflict Labels)
    df_sent.to_csv(Path('../../Corpora/Annotated/Conflicts/main_conflicts.csv'))

if __name__== '__main__':
    main()