import nltk


'''
2. Write a tag pattern to match noun phrases containing plural 
head nouns, e.g. "many/JJ researchers/NNS", "two/CD weeks/NNS", 
"both/DT new/JJ positions/NNS". Try to do this by generalizing 
the tag pattern that handled singular noun phrases.
'''
brown = nltk.corpus.brown

grammar1 = r"""
  NP: {<DT|PP\$|CD>?<JJ>*<NNS>}   
      {<NNS>+} 
"""

cp = nltk.RegexpParser(grammar1)
sentence = [("Rapunzel", "NNS"), ("let", "VBD"), ("down", "RP"),
            ("her", "PP$"), ("weeks", "NNS"), 
                 ("two", "CD"),  ("weeks", "NNS"), 
                 ("both", "DT")
                 , ("new", "JJ"), ("positions", "NNS")]

print(cp.parse(sentence))

'''
3. Pick one of the three chunk types in the CoNLL corpus. 
Inspect the CoNLL corpus and try to observe any patterns in 
the POS tag sequences that make up this kind of chunk. 
Develop a simple chunker using the regular expression 
chunker nltk.RegexpParser. Discuss any tag sequences 
that are difficult to chunk reliably.
'''
from nltk.corpus import conll2000
grammarChunk = r"NP: {<[CDJNP].*>+}"
    
grammarChunk = r"""
  NP: {<DT|PP\$|CD>?<JJ>*<NN>}   
      {<DT|PP\$|CD>?<JJ>*<NNS>} 
      {<DT|PP\$|CD>?<JJ>*<NNP>} 
      {<NN>+} 
      {<NNS>+} 
      {<NNP>+} 
      {<PRP|WP|CD|DT|WDT|JJ>}  
"""

cpChunk = nltk.RegexpParser(grammarChunk)
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
print(cpChunk.evaluate(test_sents))

'''
5. Write a tag pattern to cover noun phrases that contain 
gerunds, e.g. "the/DT receiving/VBG end/NN", 
"assistant/NN managing/VBG editor/NN". Add these patterns 
to the grammar, one per line. Test your work using some 
tagged sentences of your own devising
'''

from nltk.corpus import mac_morpho

grammar2 = r"""
  NP: {<DT|PP\$|CD>*<VBG><NN|NNS|NNP>}  
"""
cp = nltk.RegexpParser(grammar2)

sentence = [("Podemos", "NN"), ("opens", "VB"), ("debate", "VB"),
            ("on", "IN"), ("legalizing", "VBG"), ("marijuana", "NN"),  
            ("in", "IN"), ("Spain", "NN"), ("The", "DT"), 
            ("drug", "NN"), ("became", "VB"), 
            ("legal", "NN"), ("in", "CC"), ("Canada", "NN")
            , ("the", "DT"), ("anti-austerity", "NN"), ("party", "NN")
            , ("organized", "VBP"), ("a", "AT"), ("forum", "NN")
            , ("to", "IN"), ("support", "VB"), ("decriminalizing", "VBG")
            , ("cultivation", "NN"), (",", ","), ("sale", "NN")
            , ("and", "CC"), ("consumption", "NN") ]

print(cp.parse(sentence))


'''
6. Write one or more tag patterns to handle coordinated 
noun phrases, e.g. "July/NNP and/CC August/NNP", 
"all/DT your/PRP$ managers/NNS and/CC supervisors/NNS", 
"company/NN courts/NNS and/CC adjudicators/NNS".
'''
brown = nltk.corpus.brown
grammar = r"""
  NP: {<DT|PP\$|PRP\$>*<JJ>*<NN|NNS|NNP>+<CC><DT|PP\$|PRP\$>*<JJ>*<NN|NNS|NNP>+}   
                        
"""

cp = nltk.RegexpParser(grammar)

sentence = [("Rapunzel", "NNP"), ("let", "CC"), ("down", "NNP"),
            ("her", "PP$"), ("weeks", "NNS"), 
                 ("two", "DT"),  ("weeks", "PRP"), 
                 ("both", "NNS")
                 , ("new", "CC"), ("positions", "NNS")
                 ,("her", "PP$")
                 , ("new", "NN"), ("positions", "NNS")
                 , ("new", "CC"), ("positions", "NNS")
                 , ("positions", "NN")
                 , ("all", "DT")
                 , ("your", "PRP$")
                 , ("managers", "NNS")
                 , ("and", "CC")
                 , ("supervisors", "NNS")
                 
                 ]

print(cp.parse(sentence))
        
