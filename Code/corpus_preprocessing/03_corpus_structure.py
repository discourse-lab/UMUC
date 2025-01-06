import spacy
import os
import pandas as pd
import re
from pathlib import Path

nlp = spacy.load('en_core_web_lg')

class Speech:
    def __init__(self, filename: str, text: str):
        self.filename = filename
        self.filename_base = os.path.basename(filename)
        self.text = text
        self.paragraphs = self.get_paragraphs()
        self.consistency_checks()
        self.fileid = re.search(r'(UNSC).*spch\d\d\d\d?', self.filename_base).group()

    def consistency_checks(self):
        paragraphs = []
        sentences = []
        tokens = []
        for pi, p in enumerate(self.paragraphs):
            assert p.text == self.text[p.start_char:p.end_char]
            assert pi == p.par_id
            paragraphs.append(p)
            for si, s in enumerate(p.sentences):
                assert s.text == self.text[s.start_char:s.end_char]
                assert si == s.par_sent_id
                sentences.append(s)
                for ti, t in enumerate(s.tokens):
                    assert t.text == self.text[t.start_char:t.end_char]
                    assert ti == t.sent_token_id
                    tokens.append(t)

        for i, p in enumerate(paragraphs):
            assert i == p.par_id
        for i, s in enumerate(sentences):
            assert i == s.sent_id
        for i, t in enumerate(tokens):
            assert i == t.speech_token_id

    def get_paragraphs(self):
        char_offset = 0
        parts = re.split(r"((?<=\.)\n{2,})", self.text)
        sent_id_offset = 0
        token_id_offset = 0
        paragraphs = []
        for i, part in enumerate(parts):
            start = char_offset
            end = char_offset + len(part)
            p = Paragraph(part, start, end, i, sent_id_offset, token_id_offset)
            char_offset += len(part)
            sent_id_offset = p.sent_id_offset
            token_id_offset = p.token_id_offset
            paragraphs.append(p)
        return paragraphs


class Paragraph:
    def __init__(self, text, start_char, end_char, par_id, par_start_sent_id, start_token_id):
        self.text = text
        self.start_char = start_char
        self.end_char = end_char
        self.par_id = par_id
        self.sentences = self.get_sentences(start_char, par_start_sent_id, start_token_id)
        self.sent_id_offset = self.get_last_sent_id() + 1
        self.token_id_offset = self.get_last_token_id() + 1

    def get_last_token_id(self):
        ltid = 0
        if self.sentences:
            last_sent = self.sentences[-1]
            if last_sent.tokens:
                ltid = last_sent.tokens[-1].speech_token_id
        return ltid

    def get_last_sent_id(self):
        lsid = 0
        if self.sentences:
            lsid = self.sentences[-1].sent_id
        return lsid

    def get_sentences(self, start_char_par, par_start_sent_id, start_token_id):
        doc = nlp(self.text)
        sentences = []
        speech_token_offset = start_token_id
        for i, sent in enumerate(doc.sents):
            s = Sentence(sent.text,
                         start_char_par,
                         sent.start_char + start_char_par,  # start char inside the sent, plus that of the host parargraph
                         sent.end_char + start_char_par,  # end char of the sent, plus that of the host paragraph
                         i + par_start_sent_id,  # sent id speech-wide (not just inside this paragraph)
                         i,
                         sent, speech_token_offset)
            speech_token_offset = s.tokens[-1].speech_token_id + 1
            sentences.append(s)
        return sentences


class Sentence:
    def __init__(self, text, par_char_start, start_char, end_char, sent_id, par_sent_id, tokenspan, start_token_id):
        self.text = text
        self.start_char = start_char
        self.end_char = end_char
        self.par_sent_id = par_sent_id
        self.sent_id = sent_id
        self.tokens = []
        for i, token in enumerate(tokenspan):
            # offset of token start, plus that of its host sentence/paragraph
            # offset of token end, plus that of its host sentence/paragraph
            # token offset, plus that of its host sentence
            t = Token(token.text, par_char_start + token.idx, par_char_start + token.idx+len(token.text), i, i +
                      start_token_id)
            self.tokens.append(t)


class Token:
    def __init__(self, text, start_char, end_char, sent_token_id, speech_token_id):
        self.text = text
        self.start_char = start_char
        self.end_char = end_char
        self.sent_token_id = sent_token_id
        self.speech_token_id = speech_token_id
        #self.tok_string = str(tok_string)


def dump_table(speech, data_para, data_sents):
    for par in speech.paragraphs:
        data_para.append([os.path.basename(speech.filename), speech.fileid, par.start_char, par.end_char, par.par_id, par.text])
        for sent in par.sentences:
            data_sents.append([os.path.basename(speech.filename), speech.fileid, sent.start_char, sent.end_char, sent.sent_id, sent.par_sent_id,
                               par.par_id, sent.text.strip(), [t.text for t in sent.tokens]])

    return data_para, data_sents


def main():
    # input path
    main_dirpath = Path("../../Corpora/Raw/Preproc_Text")

    # output paths
    output_table_para = Path("../../Corpora/Raw/main_para.csv")
    output_table_sents = Path("../../Corpora/Raw/main_sents.csv")
    data_para = []
    data_sents = []
    """ input is dir with speeches txt files"""
    if not os.path.exists(main_dirpath):
        print("WARNING: directory at input path does not exist.")
    for dirs, subdir, fs in os.walk(main_dirpath):
        for file in fs:
            if file.endswith(".txt"):
                join_fn = os.path.join(dirs, file)
                s = Speech(join_fn, open(join_fn).read())
                dump_table(s, data_para, data_sents)

    df_para = pd.DataFrame(data_para, columns=['filename', 'fileid', 'char_start_offset', 'char_end_offset', 'paragraph_id', 'text'])
    df_sents = pd.DataFrame(data_sents, columns=['filename', 'fileid', 'char_start_offset', 'char_end_offset', 'speech_sentence_id', 'paragraph_sentence_id', 'paragraph_id', 'text', 'tokenized'])
    df_para.to_csv(output_table_para, sep=",")
    df_sents.to_csv(output_table_sents, sep=",")


if __name__ == '__main__':
    main()
