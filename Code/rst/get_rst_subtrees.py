import pandas as pd
from collections import Counter
import ast
import numpy as np


def to_consecutive(df_notcon):
    paragraph_id_list = df_notcon['paragraph_id'].tolist()
    id_counter = -1
    new_paragraph_id_list = []
    for index, element in enumerate(paragraph_id_list):

        if not isinstance(paragraph_id_list[index], (int, np.integer)):
            new_paragraph_id_list.append(id_counter+1)
        elif not isinstance(paragraph_id_list[index-1], (int, np.integer)):
            new_paragraph_id_list.append(id_counter+1)
        elif paragraph_id_list[index-1] == paragraph_id_list[index]:
            new_paragraph_id_list.append(id_counter)
        elif paragraph_id_list[index-1] != paragraph_id_list[index]:
            id_counter += 1
            new_paragraph_id_list.append(id_counter)

    return new_paragraph_id_list


def find_common_path(listi):
    if len(listi) == 1:
        return listi[0]
    global_common = [0] * max([len(x) for x in listi])
    for li in listi:
        reverse_li = li[::-1]
        for lj in listi:
            reverse_lj = lj[::-1]
            assert reverse_li[0] == reverse_lj[0]
            local_common = []
            shortest_list = min(len(reverse_li), len(reverse_lj))
            for i in range(shortest_list):
                if reverse_li[i] == reverse_lj[i]:
                    local_common.append(reverse_li[i])
                else:
                    break
            if len(local_common) < len(global_common):
                global_common = local_common
    #if [0] * len(global_common) == global_common:
    #    print("Only one edu in paragraph, no subtree.")
    return global_common[::-1]


def get_truncated_paths(listi, p):
    truncated_paths = []
    for li in listi:
        assert li[len(li) - len(p):] == p
        truncated_path = li[:len(li) - len(p) + 1]
        truncated_paths.append(truncated_path)
    return truncated_paths


def flatten_comprehension(matrix):
    return [item for row in matrix for item in row]


def get_subtrees_per_paragraph(df):
    # input: prepared dataframe
    # update paragraph_ids, take nodeid_chain and relation_chain and shorten them to subtrees (per paragraph)
    # get sat value for speech and paragraph trees, will be used for NM
    # output: dataframe with subtrees and sat values
    paragraph_consec_list = []
    list_nodeid_subtree = []
    list_rstree_rel = []
    list_rstree_li = []
    list_paragraph_index_chain_big = []

    list_sat_value = []
    list_sat_value_subtree = []

    # include columns for paragraph id
    new_paragraph_id_list = to_consecutive(df)
    df['paragraph_id_consecutive'] = new_paragraph_id_list
    filenames = df['filename'].drop_duplicates().tolist()
    new_paragraph_id_list_per_file = []
    for filename in filenames:
        df_fn = df[df['filename'] == filename]
        list_consecutive_fn = to_consecutive(df_fn)
        new_paragraph_id_list_per_file.append(list_consecutive_fn)
    new_paragraph_id_list_per_file = flatten_comprehension(new_paragraph_id_list_per_file)
    assert len(new_paragraph_id_list_per_file) == len(new_paragraph_id_list)
    df['paragraph_id_consecutive_per_file'] = new_paragraph_id_list_per_file


    # iterate over apragraphs and compute over list of relations
    paragraph_idxs = df['paragraph_id_consecutive'].drop_duplicates().tolist()
    for paragraph_index in paragraph_idxs:
        df_p = df[df['paragraph_id_consecutive'] == paragraph_index]
        list_paragraph_index_chain = []

        for index, row in df_p.iterrows():
            # get df['rstree_nodeid_chain'] row from str to lists
            #y_str = row['rstree_nodeid_chain']
            y = row['rstree_nodeid_chain']
            #y = ast.literal_eval(y_str)
            list_paragraph_index_chain.append(y)

            # get df['rstree_relation_chain'] row from str to lists
            #z_str = row['rstree_relation_chain']
            z = row['rstree_relation_chain']
            #z = ast.literal_eval(z_str)
            list_rstree_rel.append(z)
            sum_edges = len(z)
            list_rstree_li.append(sum_edges)  # get sum of edges from leave to root
            # get sat value which are all satelite relation from leave to root
            assert len(y) == sum_edges

            counter = Counter(z)
            sum_rstree_nucl_value = counter[None] + counter['span'] + counter['sameunit'] + counter['list'] + counter[
                'joint'] + counter['contrast'] + counter['sequence'] + counter['textual-organization']
            assert sum_edges == sum(counter.values())

            sat_value = sum_edges - sum_rstree_nucl_value
            list_sat_value.append(sat_value)

        list_paragraph_index_chain_big.append(list_paragraph_index_chain)

        assert len(list_rstree_li) == len(list_sat_value)

        common_path = find_common_path(list_paragraph_index_chain)
        para_lst = get_truncated_paths(list_paragraph_index_chain, common_path)
        assert df_p.shape[0] == len(para_lst)
        list_nodeid_subtree.append(para_lst)

    list_paragraph_index_chain_big = flatten_comprehension(list_paragraph_index_chain_big)
    list_nodeid_subtree = flatten_comprehension(list_nodeid_subtree)
    assert len(list_nodeid_subtree) == len(list_rstree_rel) == len(list_rstree_li) == len(list_paragraph_index_chain_big)

    # get len list for each list in list_nodeid_subtree,
    list_subtree_li = [len(x) for x in list_nodeid_subtree]
    # slice df['rstree_relation_chain'] lists to len(para_lst)
    lst_para_rel_subtree = []
    for i, r in enumerate(list_subtree_li):
        sublist = list_rstree_rel[i][:r]
        counter2 = Counter(sublist)
        lst_para_rel_subtree.append(sublist)
        sum_subtree_nucl_value = counter2[None] + counter2['span'] + counter2['sameunit'] + counter2['list'] + counter2[
            'joint'] + counter2['contrast'] + counter2['sequence'] + counter2['textual-organization']
        sat_value_subtree = len(sublist) - sum_subtree_nucl_value
        list_sat_value_subtree.append(sat_value_subtree)

    assert len(lst_para_rel_subtree) == len(list_nodeid_subtree) == len(list_sat_value_subtree)

    df['rstree_edges'] = list_rstree_li
    df['sat_value_rstree'] = list_sat_value

    df['rstree_nodeid_chain_subtree'] = list_nodeid_subtree
    df['rstree_relation_chain_subtree'] = lst_para_rel_subtree
    df['rstree_edges_subtree'] = list_subtree_li

    df['sat_value_subtree'] = list_sat_value_subtree

    return df


