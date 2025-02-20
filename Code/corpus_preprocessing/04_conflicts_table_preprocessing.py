from pathlib import Path
import pandas as pd


# TODO: eventually replace _ and with None
def prepare_dataframe(original_confl_table):
    # input: dataframe output from 01_align_rst_conflict.py
    # create a conflict column, correct values in paragraph and sentence id, keep only columns needed, sort dataframe,
    # return prepared dataframe
    df_conflicts = pd.read_csv(original_confl_table, index_col=0)

    merge_columns = {
        ("A0_Negative_Evaluation", "B1_ChallengeType"): "Conflict_Type",
        ("A2_Target_Council", "B2_Target_Challenge"): "Conflict_Target",
        ("A2_Target_Council_2", "B2_Target_Challenge_2"): "Conflict_Target_2",
        ('A4_Country_Name', 'B3_Country_Name'): 'Target_Country_Name',
        ('A4_Country_Name_2', 'B3_Country_Name_2'): 'Target_Country_Name_2'
    }
    # merging
    for (col1, col2), new_col in merge_columns.items():
        df_conflicts[[col1, col2]] = df_conflicts[[col1, col2]].replace("_", "") # replace underscore entries with empty str
        df_conflicts[[col1, col2]] = df_conflicts[[col1, col2]].replace("-NONE-", "Underdefined")  # replace -None_ entries with Undersecified
        df_conflicts[new_col] = df_conflicts[col1] + df_conflicts[col2] # concat values
        df_conflicts.drop([col1, col2], axis=1, inplace=True) # drop old columns
        df_conflicts[new_col] = df_conflicts[new_col].replace("", "_") # replace empty str entries with underscore

    # rename Target_Intermediate column
    df_conflicts = df_conflicts.rename(columns={'A3_Target_Intermediate': 'Conflict_Target_Intermediate',
                                                'A3_Target_Intermediate_2': 'Conflict_Target_Intermediate_2'})

    # re-order dataframe columns order
    columns_to_move = ["Conflict_Type", 'Conflict_Target', 'Target_Country_Name', 'Conflict_Target_2',
                       'Target_Country_Name_2', 'Conflict_Target_Intermediate', 'Conflict_Target_Intermediate_2']
    for x in reversed(columns_to_move):
        column_to_move = df_conflicts.pop(x)
        df_conflicts.insert(6, x, column_to_move)

    df_sent_sm = df_conflicts.sort_values(['filename', 'speech_sentence_id'], ascending=[True, True])

    return df_sent_sm





def main():
    conflicts_df = Path('../../Corpora/Annotated/Conflicts/main_conflicts_not_preprocessed.csv')
    df_sent = prepare_dataframe(conflicts_df) # prepare conflicts csv (merge Conflict Labels)
    df_sent.to_csv(Path('../../Corpora/Annotated/Conflicts/main_conflicts.csv'))

if __name__== '__main__':
    main()