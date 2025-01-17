''' Creates table with RST annotations and flat RST labels "main_conflicts_aligned.csv".
Input: folder with rst files /data/07_rst, conflicts table ../data/main_conflicts.csv
Output: aligned conflicts-rst table'''
import lxml.etree
from pathlib import Path
import pandas as pd
import spacy
from get_rst_subtrees import get_subtrees_per_paragraph, ids_to_consecutive

nlp = spacy.load('en_core_web_lg')
xmlp = lxml.etree.XMLParser(strip_cdata=False, resolve_entities=False, encoding='utf-8', remove_comments=True)


def get_root_path(node, tree, path):
    if 'parent' in node.attrib:
        parent_id = node.get('parent')
        parent_node = [x for x in tree.getroot().find('.//body') if x.get('id') == parent_id]
        assert len(parent_node) == 1

        path.append(parent_node[0])
        get_root_path(parent_node[0], tree, path)
    return path


def get_relation_chain(rootpath, rstree):
    """
    Constructs a relation chain based on the `rootpath` and `rstree`.
    Args:
        rootpath (list): A list of elements representing the root path.
        rstree (lxml.etree.ElementTree): The RST tree structure.
    Returns:
        tuple: A tuple containing the relation chain (list) and the first relation (str).
    """
    relation_chain = []

    for x in rootpath:
        relname = x.get('relname')

        if relname != "span":
            # if relname is None, append root relation, else append relname
            relation_chain.append('root' if relname is None else relname)
        else:  # relname == "span"
            relation_id = x.get('id')

            # Find all child elements of the current span
            elements = rstree.xpath(".//segment[@parent='" + relation_id + "']") \
                       + rstree.xpath(".//group[@parent='" + relation_id + "']")
            # Check if these are all multinuc or other rels
            #if len(elements) != 1:
            #    print([elem.get('relname') for elem in elements])

            # Get the relname of the parent element
            if elements:
                relname_parent = elements[0].get('relname')

                # root relation is None, rename as root
                if relname_parent is None:
                    relation_chain.append("root")
                elif relname_parent == "span":
                    # Handle multi-nucleus spans or relations that originate from a side string and are not directly
                    # parent relations
                    for i, elem in enumerate(elements[1:], start=1):
                        relname_parent_n = elem.get('relname')
                        if relname_parent_n == "span":
                            continue
                        relation_chain.append(f"{relname_parent_n}_nucleus")
                        break
                    else:
                        relation_chain.append("span_nucleus")
                else:
                    relation_chain.append(f"{relname_parent}_nucleus")

    # Retrieve the first relation in the chain
    relation = relation_chain[0] if relation_chain else None
    return relation_chain, relation


def align(csvf, rst_dir):
    df = pd.read_csv(csvf, index_col=0)
    df = df.sort_values(["filename", "speech_edu_id"])
    path = Path(rst_dir)
    listi = [i for i in path.glob('**/*.rs3')]
    listi.sort()
    big_list_id = []
    big_list_relation = []
    big_list_id_chain = []
    big_list_relation_chain = []

    # get files that are not annotated with rst but conflicts, and filter those from df, create "_selected" corpus
    list_fileids_confl = df["fileid"].drop_duplicates().to_list()
    list_fileids_rst = [i.name[:26] for i in path.glob('**/*.rs3')]
    temp = [x for x in list_fileids_confl if x not in list_fileids_rst]
    df_f = df[~df['fileid'].isin(temp)]

    for rstf in listi:
        name = rstf.name[:26]
        # get rows in df for file
        df_file = df_f[df_f.fileid == name]
        if len(df_file):
            rstree = lxml.etree.parse(str(rstf), parser=xmlp)
            count_rst_segements = len(rstree.getroot().findall('.//segment'))

            # assert df_file.shape[0] == count_rst_segements, name
            if df_file.shape[0] != count_rst_segements:
                print("For file", name, "there is an inconsistency of EDUs.\n Conflicts num EDUs: ", df_file.shape[0],
                      "\n RST num EDUs: ", count_rst_segements)
                break
            # messing up from here
            for segment in rstree.getroot().findall('.//segment'):
                rootpath = get_root_path(segment, rstree, [segment])
                id_chain = [x.get('id') for x in rootpath]
                id_rel = id_chain[0]
                relation_chain, relation = get_relation_chain(rootpath, rstree)

                assert len(id_chain) == len(relation_chain), 'Problem l. 72'

                big_list_id_chain.append(id_chain)
                big_list_id.append(id_rel)
                big_list_relation_chain.append(relation_chain)
                big_list_relation.append(relation)

        elif df_file.shape[0] != count_rst_segements and len(df_file):
            print(name, "num conflict edus:", df_file[0], "num rst edus:", count_rst_segements)
        else:
            print("File: ", name, "file is missing in Conflicts csv.")

    assert len(big_list_id) == len(big_list_id_chain) == len(big_list_relation_chain), 'Problem l. 86'

    df_f['rstree_nodeid'] = big_list_id
    df_f['rstree_nodeid_chain'] = big_list_id_chain
    df_f['rstree_relation_leaf'] = big_list_relation
    df_f['rstree_relation_chain'] = big_list_relation_chain
    df_f = df_f.reset_index(drop=True)

    df_f['paragraph_id'] = df_f['paragraph_id'].astype("Int64")
    df_f['speech_sentence_id'] = df_f['speech_sentence_id'].astype("Int64")
    return df_f


def get_tokens(df_aligned):
    # tokenize edus
    list_edutexts = df_aligned['text_edu'].tolist()
    big_tokenized_list = []
    big_len_tok_list = []
    for text in list_edutexts:
        processed_text = nlp(text)
        tokenized_list = [i.text for i in processed_text]
        len_tok_list = len(tokenized_list)
        big_tokenized_list.append(tokenized_list)
        big_len_tok_list.append(len_tok_list)
    df_aligned['tokenized_edus'] = big_tokenized_list
    df_aligned['len_tokens_edus'] = big_len_tok_list
    return df_aligned


def main():
    rst_dir = Path('../Corpora/Annotated/RST_original')
    csvf = Path('../Corpora/Annotated/Conflicts/main_conflicts.csv')
    output_file = Path('../Corpora/Annotated/conflicts_rst_aligned.csv')
    df_aligned = align(csvf, rst_dir)
    df_tokens = get_tokens(df_aligned)

    # get paragraph-based relations
    df_consec = ids_to_consecutive(df_tokens)
    df_sub = get_subtrees_per_paragraph(df_consec)
    df_sub.to_csv(output_file)


if __name__ == '__main__':
    main()
