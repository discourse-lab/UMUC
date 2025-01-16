from pathlib import Path
import pandas as pd




# TODO: maybe also rename labels, replace _ and NONE with None
def prepare_dataframe(original_confl_table):
    # input: dataframe output from 01_align_rst_conflict.py
    # create a conflict column, correct values in paragraph and sentence id, keep only columns needed, sort dataframe,
    # return prepared dataframe
    df_conflicts = pd.read_csv(original_confl_table, index_col=0)

    """
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
    
    # insert column with insert(location, column_name, column_value)
    df.insert(6, "Conflict_Type", column_to_move)
    """
    df_conflicts['Conflict_Type'] = df_conflicts['A0_Negative_Evaluation'].fillna(df_conflicts['B1_ChallengeType'])

    df_conflicts['Conflict_Target'] = df_conflicts['A2_Target_Council'].fillna(df_conflicts['B2_Target_Challenge'])
    df_conflicts['Conflict_Target_2'] = df_conflicts['A2_Target_Council_2'].fillna(df_conflicts['B2_Target_Challenge_2'])
    df_conflicts['Target_Country_Name'] = df_conflicts['A4_Country_Name'].fillna(df_conflicts['B3_Country_Name'])
    df_conflicts['Target_Country_Name_2'] = df_conflicts['A4_Country_Name_2'].fillna(df_conflicts['B3_Country_Name_2'])

    df_conflicts = df_conflicts.drop(
        ['A0_Negative_Evaluation', 'B1_ChallengeType', 'A2_Target_Council','A2_Target_Council_2', 'B2_Target_Challenge',
         'B2_Target_Challenge_2', 'A4_Country_Name', 'A4_Country_Name_2',
         'B3_Country_Name', 'B3_Country_Name_2'], axis=1)

    df_conflicts = df_conflicts.rename(columns={'A3_Target_Intermediate': 'Conflict_Target_Intermediate',
                                                'A3_Target_Intermediate_2': 'Conflict_Target_Intermediate_2'})
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