import nltk
from collections import Counter
from chicksexer import predict_gender
from helpers import ages_keywords as age
from helpers import cancer_keywords as cancer
from helpers import gender_keywords as gender


staged_list_stomach = {"male": 0, "female": 0}
staged_list_breast = {"male": 0, "female": 0}
staged_list_skin = {"male": 0, "female": 0}
staged_list_bone = {"male": 0, "female": 0}
staged_list_pediatric = {"male": 0, "female": 0}
staged_list_brain = {"male": 0, "female": 0}
staged_list_head_neck = {"male": 0, "female": 0}
staged_list_blood = {"male": 0, "female": 0}
staged_list_lung = {"male": 0, "female": 0}

staged_list = {}
staged_gender_total = []

stemmer = nltk.stem.PorterStemmer()


def get_cancer_type(tweet, name):
    if (any(word.lower() in tweet for word in cancer.blood)
            or any(stemmer.stem(word) in tweet for word in cancer.blood)):

        if ('blood' in staged_list):
            # increment that topic
            staged_list['blood'] += 1
        else:
            # add topic to list
            staged_list['blood'] = 1

        detect_age(tweet, 'blood')
        result = prepare_username(name)

        if result['male'] > result['female']:
            staged_list_blood['male'] += 1
        else:
            staged_list_blood['female'] += 1

    if (any(word.lower() in tweet for word in cancer.breast)
            or any(stemmer.stem(word) in tweet for word in cancer.breast)):

        if ('breast' in staged_list):
            # increment that topic
            staged_list['breast'] += 1
        else:
            # add topic to list
            staged_list['breast'] = 1

        detect_age(tweet, 'breast')
        result = prepare_username(name)

        if result['male'] > result['female']:
            staged_list_breast['male'] += 1
        else:
            staged_list_breast['female'] += 1

    if (any(word.lower() in tweet for word in cancer.stomach)
            or any(stemmer.stem(word) in tweet for word in cancer.stomach)):

        if ('stomach' in staged_list):
            # increment that topic
            staged_list['stomach'] += 1
        else:
            # add topic to list
            staged_list['stomach'] = 1

        detect_age(tweet, 'stomach')
        result = prepare_username(name)

        if result['male'] > result['female']:
            staged_list_stomach['male'] += 1
        else:
            staged_list_stomach['female'] += 1

    if (any(word.lower() in tweet for word in cancer.lung)
            or any(stemmer.stem(word) in tweet for word in cancer.lung)):

        if ('lung' in staged_list):
            # increment that topic
            staged_list['lung'] += 1
        else:
            # add topic to list
            staged_list['lung'] = 1

        detect_age(tweet, 'lung')
        result = prepare_username(name)

        if result['male'] > result['female']:
            staged_list_lung['male'] += 1
        else:
            staged_list_lung['female'] += 1

    if (any(word.lower() in tweet for word in cancer.skin)
            or any(stemmer.stem(word) in tweet for word in cancer.skin)):

        if ('skin' in staged_list):
            # increment that topic
            staged_list['skin'] += 1
        else:
            # add topic to list
            staged_list['skin'] = 1

        detect_age(tweet, 'skin')
        result = prepare_username(name)

        if result['male'] > result['female']:
            staged_list_skin['male'] += 1
        else:
            staged_list_skin['female'] += 1

    if (any(word.lower() in tweet for word in cancer.head_neck)
            or any(stemmer.stem(word) in tweet for word in cancer.head_neck)):

        if ('head_neck' in staged_list):
            # increment that topic
            staged_list['head_neck'] += 1
        else:
            # add topic to list
            staged_list['head_neck'] = 1

        detect_age(tweet, 'head_neck')
        result = prepare_username(name)

        if result['male'] > result['female']:
            staged_list_head_neck['male'] += 1
        else:
            staged_list_head_neck['female'] += 1

    if (any(word.lower() in tweet for word in cancer.brain)
            or any(stemmer.stem(word) in tweet for word in cancer.brain)):

        if ('brain' in staged_list):
            # increment that topic
            staged_list['brain'] += 1
        else:
            # add topic to list
            staged_list['brain'] = 1

        detect_age(tweet, 'brain')
        result = prepare_username(name)

        if result['male'] > result['female']:
            staged_list_brain['male'] += 1
        else:
            staged_list_brain['female'] += 1

    if (any(word.lower() in tweet for word in cancer.bone)
            or any(stemmer.stem(word) in tweet for word in cancer.bone)):

        if ('bone' in staged_list):
            # increment that topic
            staged_list['bone'] += 1
        else:
            # add topic to list
            staged_list['bone'] = 1

        detect_age(tweet, 'bone')
        result = prepare_username(name)

        if result['male'] > result['female']:
            staged_list_bone['male'] += 1
        else:
            staged_list_bone['female'] += 1

    if (any(word.lower() in tweet for word in cancer.pediatric)
            or any(stemmer.stem(word) in tweet for word in cancer.pediatric)):

        if ('pediatric' in staged_list):
            # increment that topic
            staged_list['pediatric'] += 1
        else:
            # add topic to list
            staged_list['pediatric'] = 1

        detect_age(tweet, 'pediatric')
        result = prepare_username(name)

        if result['male'] > result['female']:
            staged_list_pediatric['male'] += 1
        else:
            staged_list_pediatric['female'] += 1


def return_lists():
    return staged_list


def genderize(words):

    mwlen = len(gender.MALE_WORDS.intersection(words))
    fwlen = len(gender.FEMALE_WORDS.intersection(words))
    if mwlen > 0 and fwlen == 0:
        return gender.MALE
    elif mwlen == 0 and fwlen > 0:
        return gender.FEMALE
    elif mwlen > 0 and fwlen > 0:
        return gender.BOTH
    else:
        return gender.UNKNOWN


def count_gender(sentences):

    sents = Counter()
    words = Counter()
    for sentence in sentences:
        gender = genderize(sentence)
        sents[gender] += 1
        words[gender] += len(sentence)
    return sents, words


def detect_age(text, cancer_type):

    list_name = 'staged_age_%s' % cancer_type
    print(list_name)
    if (any(word.lower() in text for word in age.set_13_18) or any(stemmer.stem(word) in text for word in age.set_13_18)):
        if ('set_13_18' in eval(list_name)):
            # increment that topic
            eval(list_name)['set_13_18'] += 1
        else:
            # add topic to list
            eval(list_name)['set_13_18'] = 1

    if (any(word.lower() in text for word in age.set_19_22) or any(stemmer.stem(word) in text for word in age.set_19_22)):
        if ('set_19_22' in eval(list_name)):
            # increment that topic
            eval(list_name)['set_19_22'] += 1
        else:
            # add topic to list
            eval(list_name)['set_19_22'] = 1

    if (any(word.lower() in text for word in age.set_23_29) or any(stemmer.stem(word) in text for word in age.set_23_29)):
        if ('set_23_29' in eval(list_name)):
            # increment that topic
            eval(list_name)['set_23_29'] += 1
        else:
            # add topic to list
            eval(list_name)['set_23_29'] = 1

    if (any(word.lower() in text for word in age.set_30_65) or any(stemmer.stem(word) in text for word in age.set_30_65)):
        if ('set_30_65' in eval(list_name)):
            # increment that topic
            eval(list_name)['set_30_65'] += 1
        else:
            # add topic to list
            eval(list_name)['set_30_65'] = 1


def prepare_username(name):

    # Filtering unknown characters
    result = name.replace("_", "")
    result = result.replace("*", "")
    result = result.replace("-", "")
    result = result.replace("+", "")
    result = result.replace("(", "")
    result = result.replace(")", "")
    result = result.replace("^", "")
    result = result.replace("%", "")
    result = result.replace("$", "")
    result = result.replace("@", "")
    result = result.replace("!", "")
    result = result.replace("&", "")
    result = result.replace(",", "")
    result = result.replace("#", "")
    result = result.replace("|", "")
    result = result.replace("\\", "")
    result = result.replace("/", "")
    result = result.replace("\"\"", "")
    result = result.replace("\"", "")
    result = predict_gender(name)
    print(result)
    return result
