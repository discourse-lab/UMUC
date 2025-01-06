"""01 Files preprocessing: delete linebreaks, delete first part of txt (speaker, country),
 add country name to filename, create speaker-Metadata table for sub-corpus
 input: ./Corpora/Raw/Raw_Text, ./Corpora/Metadata/speaker.tsv
 output:  ./Corpora/Raw/Preproc_Text, ./Corpora/Metadata/speaker_03_preproc.tsv
"""

import os
import re
import pandas as pd
from utils import create_dir
from pathlib import Path


def delete_linebreaks(orig_string):
    # delete unnecessary line breaks
    substitute = re.sub("(?<=[^\.])(\n\n)", " ", orig_string)
    substitute = re.sub("(?<=[\w\;\:\,])\n", " ", substitute)
    substitute = re.sub("(?<=[\-])\n", "", substitute)
    explicit_str = repr(substitute) #for debugging
    return substitute


def slice_speech(input_string):
    # delete everything until first column
    output_string = re.sub(r"(.*?: )", "", input_string, count=1)
    return output_string


def preprocess_str_main(orig_path, output_path, speaker_meta_path, unscon_meta_table):
    fname = [] #filenames
    fpath_raw_sel = []
    fpath_preproc = []

    speakers_df = pd.read_csv(speaker_meta_path, sep='\t', header=0)
    country_dict = list(zip(speakers_df['filename'], speakers_df['country']))

    create_dir(output_path)

    for root, dirs, files in os.walk(orig_path):
        for name in files:
            if name.endswith(".txt"):
                filepath = root + os.sep + name
                fpath_raw_sel.append(filepath) #list for Metadata file
                debate_dir = os.path.basename(os.path.dirname(filepath)) #last dir (debate)
                fname.append(name) #filenames
                
                with open(filepath, 'r+') as opened_f:
                    read_f = opened_f.read()
                    str_no_linebreaks = delete_linebreaks(read_f)
                    str_only_speech = slice_speech(str_no_linebreaks)
                    output_dir_folder = debate_dir + "_preproc"
                    output_dir = output_path / output_dir_folder
                    create_dir(output_dir) 
                    
                    for filename, country in country_dict:
                        country2 = country.replace(" ", "_")
                        if name == filename:
                            new_filename = os.path.splitext(name)[0] + "_" + country2 + ".txt"

                            output_fpath = output_dir / new_filename
                            fpath_preproc.append(output_fpath) # list for Metadata
                            with open(output_fpath, "w") as text_file:
                                text_file.write(str_only_speech)
    speakers_df["fileid"] = [w[:-4] for w in speakers_df["filename"].tolist()]
    create_metadata(speakers_df, fname, unscon_meta_table, fpath_raw_sel)


def create_metadata(df_sp, fnames, unscon_meta_table, fpath_raw_sel):
    """
    input: speaker_metadata (tsv file), fnamkes (list)
    write sm_speakers_df into file, save in /Metadata
    """
    sm_df_sp = df_sp[(df_sp["filename"].isin(fnames))]
    sm_df_sp["filepath_raw"] = fpath_raw_sel

    # reorder columns
    column_to_move1 = sm_df_sp.pop("filename")
    column_to_move2 = sm_df_sp.pop("fileid")
    sm_df_sp.insert(len(sm_df_sp.columns), "filename", column_to_move1)
    sm_df_sp.insert(len(sm_df_sp.columns), "fileid", column_to_move2)

    sm_df_sp.to_csv(unscon_meta_table, sep="\t")


if __name__ == "__main__":

    input_path = Path("../../Corpora/Raw/Raw_Text")
    speaker_meta_path = Path("../../Corpora/Metadata/speaker.tsv")
    output_path = Path("../../Corpora/Raw/Preproc_Text")
    unscon_meta_table = Path("../../Corpora/Metadata/speaker_UNSCon_metadata.tsv")

    preprocess_str_main(input_path, output_path, speaker_meta_path, unscon_meta_table)


    

