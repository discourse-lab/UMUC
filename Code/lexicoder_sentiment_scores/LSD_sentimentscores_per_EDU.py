import pandas as pd
pd.options.mode.chained_assignment = None
import os
import re
import sys
from tqdm import tqdm




def preprocess(text: str):
    """Remove punctuation, transform to lower case."""
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

def find_sentiment_entries(string, df_lsd):
    """Get the sentiment words in a input string.
    Check the words in the string that are contained in the sentiment dictionary.
    Return the string and the words and their polarity.
    The polarities are negative|positive|neg_negative|neg_positive.

    Args
    ----
    edu (str): input string
    entry (list): list with LSD lexEntry, nrOfTokens, isPrefix, polarity

    Return
    ------
    str, list(tuple(str, str)): the preproc sentence, the sentiment words and their polarities.
    """
    out_entries = []
    edu_pp = preprocess(string)
    edu_pp_separated = edu_pp.split()

    for row in df_lsd.values:
        entry = row.tolist()
        # lex entry is single token
        if entry[1] == 1:
            # lex entry is not a prefix
            if entry[2] == 0:
                out_entries.extend([(entry[0], entry[3]) for t in edu_pp_separated if entry[0] == t])
            else:
            # if lex entry is a prefix
                out_entries.extend([(entry[0], entry[3]) for t in edu_pp_separated if t.startswith(entry[0])])
        else:
            # lex entry is not a prefix
            if entry[2] == 0:
                pattern_in_sent = entry[0] + " "
                out_entries.extend([(entry[0], entry[3]) for i in range((len(edu_pp.split(pattern_in_sent)) - 1))])
                if edu_pp.endswith(entry[0]):
                    out_entries.append((entry[0], entry[3]))
                else:
                    out_entries.extend([(entry[0], entry[3]) for i in range((len(edu_pp.split(entry[0])) - 1))])

    return edu_pp, out_entries

def calc_sentiment_score(sentence: str, pol_words):
    """Calculate the sentiment score of a sentence.
    The score is in [-1,1] and score = (n_positive_words - n_negative_words) / n_words.

    Args
    ----
    sentence (str): The sentence.
    pol_words (list(tuple(str, str)) or list(str)): The words and their polarities or just polarites.

    Return
    ------
    core (float): sentiment score.
    pol_words (list): extracted polarity words.
    """
    neg = sum([1 for t in pol_words if "negative" in t])
    neg_neg = sum([1 for t in pol_words if "neg_negative" in t])
    pos = sum([1 for t in pol_words if "positive" in t])
    neg_pos = sum([1 for t in pol_words if "neg_positive" in t])
    pos = pos - neg_pos + neg_neg
    neg = neg - neg_neg + neg_pos
    score = pos - neg
    if score != 0:
        score = score / len(sentence.split())
    return pol_words, score


def lexicoder_info_to_df(df, polarity_words, scores):
    df['lexicoder_words_polarity'] = polarity_words
    df['lexicoder_score'] = scores
    df['lexicoder_score_binary'] = (df['lexicoder_score'] < 0).astype(int)
    return df



def main():
    #UNSC_data = "./Corpora/Annotated/Conflicts/main_conflicts.csv"
    UNSC_data = "./Corpora/Annotated/Conflicts/main_conflicts_sents.csv" # for sentences
    df = pd.read_csv(UNSC_data, index_col=0)
    #TODO move to sentence creation script
    df = df[df["text"].notna()]
    df = df.reset_index(drop=True) # drop all nan in text column and resets index

    lexicoder_data = "./Code/lexicoder_sentiment_scores/LSDdata/lsd.tsv"
    df_lsd = pd.read_csv(lexicoder_data, sep="\t")

    pol_word_list = []
    score_list = []
    #for line_text in tqdm(df["text_edu"], desc="Processing sentiment score for each EDU"):
    for line_text in tqdm(df["text"], desc="Processing sentiment score for each SENTENCE"):
        line_preprocessed, out_entries = find_sentiment_entries(line_text, df_lsd)
        pol_words, score = calc_sentiment_score(line_preprocessed, out_entries)

        pol_word_list.append(pol_words)
        score_list.append(score)
    #new_dataframe=df[["file_id", "sentence_text", "A0", "B1"]]

    #categorical_dataframe = categorigal_df(new_dataframe, pol_word_list, score_list)
    categorical_dataframe = lexicoder_info_to_df(df, pol_word_list, score_list)
    #output = "./Corpora/Annotated/Conflicts/lexicoder_sentimentscores/main_conflicts_lexicoder_sentimentscores.csv"
    output = "./Corpora/Annotated/Conflicts/lexicoder_sentimentscores/main_conflicts_sents_lexicoder_sentimentscores.csv" # for sentences
    categorical_dataframe.to_csv(output, index=False)
    print()




if __name__ == "__main__":
    # Determine the script directory and ensure the working directory is set correctly
    script_dir = os.path.dirname(os.path.abspath(__file__)) # '/Users/karolinazaczynska/Documents/Potsdam/code/UMUC/Code/lexicoder_sentiment_scores'
    umuc_dir = os.path.dirname(os.path.dirname(script_dir)) # '/Users/karolinazaczynska/Documents/Potsdam/code/UMUC/Code'
    #corpus_dir = os.path.join(umuc_dir, 'Corpora')

    # Set the current directory to where this script resides
    os.chdir(umuc_dir) # Uncomment if you need to change the current working directory

    # Ensure 'Corpus' directory exists as expected
    if not os.path.exists(umuc_dir):
        print("Error: Main directory not found.")
        sys.exit(1)
    main()
