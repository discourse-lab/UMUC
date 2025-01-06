# RST-DT labels to Classes
# RST-DT Manual: classes p.32; all relations p.42
# RST-DT: Multinuclear Relations are in uppercase (the first letter):
# e.g. comparison (Mononuclear - satellite); Comparison (Multinuclear)
class2rel = {'attribution': ['attribution', 'attribution-e', 'attribution-n', 'attribution-negative'],
    'background': ['background', 'background-e', 'circumstance', 'circumstance-e'],
    'cause': ['cause', 'Cause-Result', 'result', 'result-e',
              'Consequence', 'consequence', 'consequence-n-e', 'consequence-n', 'consequence-s-e', 'consequence-s'],
    'comparison': ['Comparison', 'comparison', 'comparison-e', 'preference', 'preference-e',
                   'Analogy', 'analogy', 'analogy-e', 'proportion', 'Proportion'],
    'condition': ['condition', 'condition-e', 'hypothetical', 'contingency', 'otherwise', 'Otherwise'],
    'contrast': ['Contrast', 'concession', 'concession-e', 'antithesis', 'antithesis-e'],
    'elaboration': ['elaboration-additional', 'elaboration-additional-e', 'elaboration-general-specific',
                    'elaboration-general-specific-e', 'elaboration-part-whole', 'elaboration-part-whole-e',
                    'elaboration-process-step', 'elaboration-process-step-e', 'elaboration-object-attribute-e',
                    'elaboration-object-attribute', 'elaboration-set-member', 'elaboration-set-member-e', 'example',
                    'example-e', 'definition', 'definition-e'],
    'enablement': ['purpose', 'purpose-e', 'enablement', 'enablement-e'],
    'evaluation': ['evaluation', 'evaluation-n', 'evaluation-s-e', 'evaluation-s', 'Evaluation',
                   'interpretation', 'interpretation-n', 'interpretation-s-e', 'interpretation-s', 'Interpretation',
                   'conclusion', 'Conclusion', 'comment', 'comment-e'],
    'explanation': ['evidence', 'evidence-e', 'explanation-argumentative', 'explanation-argumentative-e', 'Reason', 'reason',
                    'reason-e'],
    'joint': ['List', 'Disjunction'],
    'manner-means': ['manner', 'manner-e', 'means', 'means-e'],
    'topic-comment': ['problem-solution', 'problem-solution-n', 'problem-solution-s', 'Problem-Solution',
                      'Question-Answer', 'question-answer', 'question-answer-n', 'question-answer-s',
                      'Statement-Response', 'statement-response-n', 'statement-response-s',
                      'Topic-Comment', 'Comment-Topic', 'rhetorical-question'],
    'summary': ['summary', 'summary-n', 'summary-s', 'restatement', 'restatement-e'],
    'temporal': ['temporal-before', 'temporal-before-e', 'temporal-after', 'temporal-after-e', 'Temporal-Same-Time', 'temporal-same-time',
                 'temporal-same-time-e', 'Sequence', 'Inverted-Sequence'],
    'topic-change': ['topic-shift', 'topic-drift', 'Topic-Shift', 'Topic-Drift'],
    'textual-organization': ['TextualOrganization'],
    'span': ['span'],
    'same-unit': ['Same-Unit', 'same-unit']}

# key RST-DT, value UNSCRhet
unsc2rstdt = {'attribution': ['attribution'],
    'background': ['background', 'circumstance'],
    'cause': ['cause', 'result'],
    #'Comparison': ['Comparison', 'comparison', 'comparison-e', 'preference', 'preference-e',
                   #'Analogy', 'analogy', 'analogy-e', 'proportion', 'Proportion'],
    'condition': ['condition', 'unless', 'otherwise'],
    'contrast': ['antithesis', 'concession', 'contrast'],
    'elaboration': ['e-elaboration', 'elaboration', 'interpretation'],
    'enablement': ['purpose', 'enablement'],
    'evaluation': ['evaluation-n', 'evaluation-s'],
    'explanation': ['reason-s', 'reason-n', 'evidence', 'motivation'],
    'joint': ['joint', 'list', 'conjunction'],
    'manner-means': ['means'],
    'topic-comment': ['topic-comment', 'solutionhood'],
    'temporal': ['sequence'],
    #'Topic-Change': ['Joint'], #??
    'textual-organization': ['textual-organization', 'preparation'],
    'span': ['span'],
    'same-unit': ['sameunit'],
    'summary': ['summary', 'restatement']}

# we don't have a mapping for UNSCRhet-'Topic-Change'. 'Joint" would be the closest choice but the label is already mapped.

unsc2gum = {
    'adversative': ['antithesis', 'concession', 'contrast'],
    'attribution': ['attribution'],
    'context-background': ['background'],
    'causal': ['cause', 'result'],
    'contingency-condition': ['condition', 'unless', 'otherwise'],
    'context-circumstance' : ['circumstance'],
    'elaboration': ['elaboration-e', 'e-elaboration', 'elaboration', 'interpretation'],
    'evaluation-comment': ['evaluation-n', 'evaluation-s'],
    'explanation': ['reason-s', 'reason-n', 'evidence', 'motivation', 'enablement'],
    'joint': ['joint', 'list', 'conjunction','sequence'],
    'mode': ['means'],
    'restatement': ['restatement', 'summary'],
    'purpose': ['purpose'],
    'topic': ['topic-comment', 'solutionhood'],
    'organization': ['textual-organization', 'preparation'],
    'same-unit': ['sameunit'],
    'span': ['span']}



# GUM 'topic-question' in 'topic' cannot be mapped for every case because we re-defined how to annotate questions
# UNSCRhet 'enablement'(makes it easier for the reader to perform the action) is not exactly explanation but close to
# 'motivation' (attempts to trigger an action on the part of the reade) which is mapped to explanation
# UNSCRhet 'interpretation' (S shifts the content of N to a different conceptual frame) is hard to map to both RST-DT
# and GUM labels, we chose the more general "elaboration" as mapping, even if it does not 100% fit
