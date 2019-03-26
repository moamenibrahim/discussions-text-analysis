import json
import nltk
import shlex
import subprocess
import enchant
from nltk.tag import StanfordNERTagger
from nltk.tag import StanfordPOSTagger
from nltk.corpus import wordnet as wn
from IBM.ibmNLPunderstanding import AlchemyNLPunderstanding

dictionary= enchant.Dict("en_US")
NLP_understanding = AlchemyNLPunderstanding()

def get_stanford_pos(tweet):
    """
    part of speech tagging extraction
    """
    path_to_model = 'cancer/stanford/stanford-postagger/models/english-bidirectional-distsim.tagger'
    path_to_jar = 'cancer/stanford/stanford-postagger/stanford-postagger.jar'
    st = StanfordPOSTagger(path_to_model, path_to_jar=path_to_jar)
    result = st.tag(tweet.split())
    return result


def get_hyponyms(tweet):
    """ 
    hyponyms extraction and checking the topics list 
    """
    entities = {}
    words = tweet.split()
    for word in words:
        for i, syn in enumerate(wn.synsets(word)):
            if(i > 3):
                pass
            else:
                entities["Hyponyms"] = []
                for hyponym in syn.hyponyms():
                    for lemma in hyponym.lemmas():
                        entities["Hyponyms"].append(lemma.name())
    return entities


def get_stanford_named_entity(tweet):
    """ 
    get named entity recognition and check if words have entry in lexical database 
    """
    stanford_dir = 'cancer/stanford/stanford-nertagger'
    jarfile = stanford_dir + '/stanford-ner.jar'
    modelfile = stanford_dir + '/classifiers/english.muc.7class.distsim.crf.ser.gz'
    st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)
    result = st.tag(tweet.split())
    return result


def get_topic(input_str):
    """ 
    Topic extraction from text using LDA (Latent Dirichet Allocation): 
    It classifies the text according to whether it is family, friend, money related
    """
    try:
        topic = lda.generate_topic(input_str)
        return topic

    except:
        print("Failed to get topic")
        return False


def get_translate(input_str, lang):
    """ using googletrans to translate text from any language to English """
    if(lang != 'und'):
        try:
            translated = translator.translate(
                input_str, dest='en', src=lang)
            return translated.text
        except:
            return False


def get_sentiment(input_str):
    """ Get sentiment analysis when needed, the used API is IBM watson's """
    return NLP_understanding.get_response(input_str)


''' Fetching information about users (tweeps) '''
def analyze_location(fileName):
    """ Method to analyze file by file and calls all other methods """
    staged_location = {}
    for line in fileName.readlines():

        tweet_data = json.loads(line)
        location = tweet_data['user']['location']
        if (location != ''):
            if (location in staged_location):
                staged_location[location] += 1  # increment that location
            else:
                staged_location[location] = 1  # add location to list
    return


def analyze_user(fileName):
    """ Method to analyze file by file and calls all other methods """
    staged_users = {}
    for line in fileName.readlines():

        tweet_data = json.loads(line)
        user = tweet_data['user']['id']
        if (user != ''):
            if (user in staged_users):
                # increment that user
                staged_users[user] += 1
            else:
                # add user to list
                staged_users[user] = 1
    return


def check_dictionary(tweet):
    """Making sure that the translated text is in dictionary 
    to verify the translation of tweets"""
    in_dict = 0
    not_in_dict = 0
    text = nltk.word_tokenize(str(tweet))
    for word in text:
        result = dictionary.check(word)
        if result == True:
            in_dict += 1
        else:
            not_in_dict += 1
    return in_dict/(in_dict+not_in_dict)


def get_human_names(text):
    """Catching human names from tweets"""
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:  # Avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
    return (person_list)


def RateSentiment(sentiString):
    """Senti Strength java software to get sentiment from tweets"""
    # open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar cancer/SentiStrength.jar stdin explain sentidata cancer/SentiStrength_Data/"),
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(
        sentiString.replace(" ", "+").encode("utf-8"))
    if stderr_text != None:
        print("Error running sentistrength")
    # remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.decode("utf-8").rstrip().replace("\t", "")
    return stdout_text[0], stdout_text[1:3]
