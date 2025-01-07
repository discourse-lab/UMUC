# UMUC: UP Multilayer UNSC Corpus


The *UP Multilayer UNSC Corpus (UMUC)* is a corpus for the analysis of diplomatic speeches given in the UN Security Council (UNSC).
Our corpus contains a small subset of speeches selected from the original [UN Security Council Debates Corpus](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/KGVSYH) containing over 25 years of digitizing meeting notes.

We preprocessed the speeches deleting unnecessary line breaks, removed text that are not the speech, and segmented the texts into either Elementary Discourse Units or sentences.
In addition to the raw texts, we present annotations for different phenomena: verbal Conflicts, discourse structures using Rhetorical Structure Theory, and automatic average Sentiments using a dictionary-based approach.

The section "Other Projects" list some links to other projects (Argumentation Mining, NER, Knowledge Graph) done with other parts of the UNSC Debates Corpus which were developed in cooperation with/at our AngCL group at Potsdam Univeristy.

For more information about this work, please see our papers.

* Karolina Zaczynska, Peter Bourgonje, and Manfred Stede. [How Diplomats Dispute: The UN Security Council Conflict Corpus.](https://aclanthology.org/2024.lrec-main.716/) In Proceedings of the Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024). Turin, Italy, 2024. [GitHub](https://github.com/linatal/UNSCon), [Bibtex](https://angcl.ling.uni-potsdam.de/projects/trajectories.html), [PDF](https://aclanthology.org/2024.lrec-main.716.pdf)
* Karolina Zaczynska and Manfred Stede. [Rhetorical Strategies in the UN Security Council: Rhetorical Structure Theory and Conflicts.](https://aclanthology.org/2024.sigdial-1.2/) In Proceedings of the SIGDIAL 2024 conference. Kyoto, 2024. [GitHub](https://github.com/linatal/rhetorical_UNSC), [Bibtex](https://angcl.ling.uni-potsdam.de/projects/trajectories.html), [PDF](https://aclanthology.org/2024.sigdial-1.2.pdf)


## Corpus Structure and Speeches Selection for UMUC

The dataset contains 87 speeches taken and preprocessed from the *UN Security Debates Corpus*. We organize our corpus into three sub-corpora, organized into two csv files and rs3 files.

We selected two topics with different expected potential for conflicts. The first agenda
is the _Ukraine_ conflict in 2014 after the annexation of Crimea (and before the
Minsk II agreement). The second agenda is the Women, Peace and Security (_WPS_) agenda. For both topics we selected debates such that they further maximize the probability of finding expressions
of conflict in the speeches. We focused on speeches from permanent members of the UNSC, and for some debates included 
additionally speeches from countries having more than one contribution to the debate. 

## Raw Data

### [Raw](Corpora%2FRaw)
Directories containing selected raw speeches (one .txt file per speech) from the original UN Security Debates Corpus.
### [Preproc_Text](Corpora%2FRaw%2FPreproc_Text)
Directories containing one .txt file per speech preprocessed with [02_preprocess.py](Code%2Fcorpus_preprocessing%2F02_preprocess.py).
### [EDUs](Corpora%2FRaw%2FEDUs) and [Sentences](Corpora%2FRaw%2FSentences) 
Directories containing one .txt file per speech with preprocessed, newline-seperated EDUs / sentences.

### [main_edus.csv](Corpora%2FRaw%2Fmain_edus.csv)
CSV-Table with one EDU per row.
* **filename**: filename in `/EDUs` directory with countryname
* **fileid**: Basename of file (without .txt) as given in the original *UN Security Debates Corpus*.
* **char_start_offset_edu**: Character offset start of EDU
* **char_start_offset_edu**: Character offset end of EDU
* **speech_sentence_id**: Counter ID for sentence inside the speech
* **paragraph_id**: Counter ID for paragraph inside the speech
* **speech_edu_id**: Counter ID for EDU inside the speech
* **text_edu**: EDU string from speech

### [main_sents.csv](Corpora%2FRaw%2Fmain_sents.csv)
CSV-Table with one sentence per row.
  * **filename** and **fileid** same as in `main_edus.csv`
  * **char_start_offset**: Character offset start of sentence
  * **char_end_offset**: Character offset end of sentence
  * **text**: Sentence string from speech
  * **tokenized**: Tokenized sentence from speech

### [main_para.csv](Corpora%2FRaw%2Fmain_para.csv) 
CSV-Table with one pragraph per row.
  * **filename**: Filename in /Preprocess folder with countryname
  * **fileid**: Basename of file (without .txt) as given in the original *UN Security Debates Corpus*
  * **char_start_offset**: Character Offset Start of Paragraph
  * **char_end_offset**: Character Offset End of Paragraph
  * **paragraph_id**: Counter ID for paragraph inside the speech 
  * **text**: Paragraph string from speech

## Annotated Data

### UNSCon: UNSC Conflicts Corpus

A dataset of 87 speeches given in the UNSC with annotations for (verbal) conflicts, specifically tailored to diplomatic 
language. We define a conflict as an expression of critique  or distancing from the positions or actions of another 
country present at the Council during the debate. 
There are four main types of conflicts annotated: 
* Direct Negative Evaluation: Describe Conflicts where the speaker directly directs the critique to another country.
* Indirect Negative Evaluation: Describe Conflicts where some intermediate entity serving as a proxy is criticized instead of the other country directly.
* Challenge: Challenging statements accuse another coun try of not telling the truth.
* Correction: Corrections rectify the allegedly false statement.

For more information on the annotation guidelines, see our [paper](https://aclanthology.org/2024.lrec-main.716.pdf).
This repository includes a corrected version of the original Conflicts corpus ([github](https://github.com/linatal/UNSCon)).

### [main_conflicts.csv](Corpora%2FAnnotated%2FConflicts%2Fmain_conflicts.csv)

Metadata:
* **filename, fileid, char_start_offset_edu, char_end_offset_edu, speech_edu_id, text_edu** same as in `main_edus.csv`

Conflict Annotations:
* **A0_Negative_Evaluation**: Conflict labels _Indirect_Negeval_ or _Direct_NegEval_
* **A2_Target_Council**: Council Target Types (_Speaker or Speech_, _Country_, _Group of Countries_, _UNSC_, _Self-targeting_, _Underspecified_)
* **A3_Target_Intermediate**: Intermediate Target Types (_Policy or Law_, _Person_, _UN-Organization_, _NGO_, _Other_)
* **A4_Country_Name**: Name of Target Country
* **B1_ChallengeType**: Conflict labels _Challenge_ or _Correction_
* **B2_Target_Challenge**: Council Target Types
* **B3_Country_Name**: Name of Target Country

Taken from `main_edus.csv`:
* **char_start_offset_edu_original** and **char_end_offset_edu_original**: Character offset taken from `main_edus.csv`
* **speech_sentence_id** and **paragraph_id**: taken from `main_edus.csv`

### [main_conflicts_sents.csv](Corpora%2FAnnotated%2FConflicts%2Fmain_conflicts_sents.csv)

EDU-based Conflict annotations mapped to sentences. For overlapping labels, we simply used the first label for the sentence.

### UNSC-RST: Rhetorical Structures
87 speeches given in the UNSC analyzed from the perspective of Rhetorical Structure Theory
(RST) (Mann and Thompson, 1988) to study study rhetorical style in diplomatic speech. RST aims to capture the structure of a text by
combining its elementary discourse units (EDUs) into one single, hierarchical tree structure.

For more information on the annotation guidelines, see our 
[paper](https://aclanthology.org/2024.lrec-main.716.pdf).
This repository includes a corrected version of the original RST corpus ([github](https://github.com/linatal/rhetorical_UNSC)), as well as versions mapped to other RST relation sets, namely to the RST-DT and GUM relation classes.

### [RST_original](Corpora%2FAnnotated%2FRST_original)
Folder with rs3 file per speech, using annotation labels as described in our paper.

### [RST_RSTDT-relations](Corpora%2FAnnotated%2FRST_RSTDT-relations) and [RST_GUM-relations](Corpora%2FAnnotated%2FRST_GUM-relations)
Folder with rs3 file per speech, automatically mapped to RST-DT classes and RST-GUM relations using [mapping_relations.py](Code%2Frst%2Fmapping_relations.py).

## Code

### Prequirements
To reproduce ownload the requirements by typing in your terminal:
`pip -r requirements.txt`

For SpaCy, download language model:
`python -m spacy download en_core_web_lg`

### [03_corpus_structure.py](Code%2Fcorpus_preprocessing%2F03_corpus_structure.py)
Script that takes the raw texts and output files `main_sents.csv` and `main_para.csv`. `main_edus.csv` was created using output from Inception annotation tool.

### [rst](Code%2Frst)
Scripts to map RST relations for out project to RST-DT classes and GUM relations. 

## Other Projects on the UNSC Debates corpus


### UNSC-NE
UNSC-NE is a Named Entity (NE) add-on to the UNSC Debates corpus using DBpedia-spotlight. 
The [code](https://github.com/glaserL/unsc-ne) and 
[dataset](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/OV1FLX) is described in the article:

Luis Glaser, Ronny Patz, and Manfred Stede (2022). [UNSC-NE: A Named Entity Extension to the UN Security Council Debates Corpus](https://jlcl.org/article/view/229). In: Journal for Language Technology and Computational Linguistics 35.2, pp. 51–67.

### UNSC-Graph
With the UNSC-Graph we presented an extensible knowledge graph for the UNSC corpus.
It was created with SWI-Prolog and currently consists of the sets of facts described in:

Stian Rødven-Eide et al. (Sept. 2023). [The UNSC-Graph: An Extensible Knowledge Graph
for the UNSC Corpus](https://codeberg.org/Stian/UNSC-Graph). In: Proceedings of the 3rd Workshop on Computational Linguistics
for the Political and Social Sciences.

The code and dataset are available [here](https://codeberg.org/Stian/UNSC-Graph).

The graph combines previously disconnected data sources including from the UNSC Repertoire, the UN Library, 
Wikidata, and from metadata extracted from the speeches themselves like topics and participants.
The graph also includes country mentions in a speech, geographical neighbours of countries mentioned, as well as 
sentiment scores. By linking the graph to Wikidata, the graph includes additional geopolitical information and extract various country name  aliases to 
extend the coverage of country mentions beyond existing NER-based approaches.

### Political Argument Mining
This project is focused on argumentation mining framed through the tasks of argument detection (predict whether the utterance is an argument or not) and argument component identification (predict whether the argumentative utterance is a claim or a premise).
As part of the project, a novel corpus of argument annotations was created based on diplomatic speeches given during gatherings of the UNSC. The corpus contains 144 speeches from 2014 to 2018, dedicated to the conflict in Ukraine, named UC(Ukraine Conflict)-UNSC. The speeches were annotated analogically to USElecDeb and the labels include claims, premises or none of these.

The dataset and code are available [here](https://github.com/mpoiaganova/political-argument-mining).
