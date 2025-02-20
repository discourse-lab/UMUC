from pathlib import Path
import pandas as pd
import numpy as np


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

    df_sort = df_conflicts.sort_values(['filename', 'speech_sentence_id'], ascending=[True, True])

    df_para = create_paragraph_ids(df_sort)
    df_out = append_conflict_id(df_para)

    return df_out


def get_values(row):
    return (
        row["Conflict_Type"],
        row["paragraph_id_consecutive_per_file"],
        row["Conflict_Target"],
        row["Target_Country_Name"],
        row["Conflict_Target_Intermediate"]
    )

def append_conflict_id(df):
    listi = []
    counter = 0
    for i in range(len(df)):
        current_values = get_values(df.loc[i])

        # check if this is the last row
        if i == len(df) - 1:
            # append value for the last row:
            if current_values[0] == "_":
                listi.append(np.nan)
            else:
                listi.append(counter)
            break
        next_values = get_values(df.loc[i + 1])
        # Compare current and next values
        if current_values[0] == None:
            listi.append(np.nan)
        elif current_values == next_values:
            listi.append(counter)
        else:
            listi.append(counter)
            counter += 1
    # assign result list to a new column in the dataframe
    assert len(listi) == df.shape[0]
    df['Conflict_IDs'] = listi

    return df


def create_paragraph_ids(df):
    # create both consecutive paragraph ids for dataset and per file
    df['speech_sentence_id'] = df['speech_sentence_id'].astype("Int64")

    # add columns consecutive paragraph ids for dataset with mo skip
    paragraph_id_list = df['paragraph_id'].tolist()
    id_counter = -1
    new_paragraph_id_list = []
    for index, element in enumerate(paragraph_id_list):

        if not isinstance(paragraph_id_list[index], (int, np.integer)):
            new_paragraph_id_list.append(id_counter + 1)
        elif not isinstance(paragraph_id_list[index - 1], (int, np.integer)):
            new_paragraph_id_list.append(id_counter + 1)
        elif paragraph_id_list[index - 1] == paragraph_id_list[index]:
            new_paragraph_id_list.append(id_counter)
        elif paragraph_id_list[index - 1] != paragraph_id_list[index]:
            id_counter += 1
            new_paragraph_id_list.append(id_counter)
    df['paragraph_id_consecutive'] = new_paragraph_id_list

    # add columns consecutive paragraph ids per file
    df['paragraph_id_consecutive_per_file'] = 0
    for filename in df['filename'].unique():
        mask = df[
                   'filename'] == filename  # creates a Boolean mask that allows for direct modification of df using .loc[]
        # df.loc[mask... extracts only the rows corresponding to the current filename in the loop
        df.loc[mask, 'paragraph_id_consecutive_per_file'] = (
                df.loc[mask, 'paragraph_id_consecutive'].rank(method='dense').astype(int) - 1)
        # .rank() function assigns ranks to unique values in the selected column; method='dense' ensures that if there
        # are repeating values, they get the same rank, and the next unique value gets the next consecutive rank
        # astype converts the ranks to integer type; - 1 ensures that the numbering starts from 0

    df = df.sort_values(['filename', 'speech_sentence_id'], ascending=[True, True])
    return df

def main():
    conflicts_df = Path('../../Corpora/Annotated/Conflicts/main_conflicts_not_preprocessed.csv')
    df_sent = prepare_dataframe(conflicts_df) # prepare conflicts csv (merge Conflict Labels)
    df_sent.to_csv(Path('../../Corpora/Annotated/Conflicts/main_conflicts.csv'))

if __name__== '__main__':
    main()