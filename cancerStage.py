import re
import nltk
import processing
from helpers import ages_keywords as age
from helpers import cancer_keywords as cancer
from helpers import gender_keywords as gender
from helpers import stages_keywords as stage

stemmer = nltk.stem.PorterStemmer()
staged_list = {}
staged_TMN_list = {}

def get_cancer_stage(tweet):
    if (any(word.lower() in tweet for word in cancer.mylist)
            or any(stemmer.stem(word) in tweet for word in cancer.mylist)):

        no_links_text, links = processing.strip_links(tweet)
        pure_text = processing.strip_all_entities(no_links_text)

        if (any(word.lower() in tweet for word in stage.stage_0)
                or any(stemmer.stem(word) in tweet for word in stage.stage_0)):

            if ('stage_0' in staged_list):
                    # increment that topic
                staged_list['stage_0'] += 1
            else:
                # add topic to list
                staged_list['stage_0'] = 1

        if (any(word.lower() in tweet for word in stage.stage_1)
                or any(stemmer.stem(word) in tweet for word in stage.stage_1)):

            if ('stage_1' in staged_list):
                    # increment that topic
                staged_list['stage_1'] += 1
            else:
                # add topic to list
                staged_list['stage_1'] = 1

        if (any(word.lower() in tweet for word in stage.stage_2)
                or any(stemmer.stem(word) in tweet for word in stage.stage_2)):

            if ('stage_2' in staged_list):
                    # increment that topic
                staged_list['stage_2'] += 1
            else:
                # add topic to list
                staged_list['stage_2'] = 1

        if (any(word.lower() in tweet for word in stage.stage_3)
                or any(stemmer.stem(word) in tweet for word in stage.stage_3)):

            if ('stage_3' in staged_list):
                    # increment that topic
                staged_list['stage_3'] += 1
            else:
                # add topic to list
                staged_list['stage_3'] = 1

        if (any(word.lower() in tweet for word in stage.stage_4)
                or any(stemmer.stem(word) in tweet for word in stage.stage_4)):

            if ('stage_4' in staged_list):
                    # increment that topic
                staged_list['stage_4'] += 1
            else:
                # add topic to list
                staged_list['stage_4'] = 1

        # TNM Match
        match = re.findall(r'[T]+[1-4]', tweet)
        if match:
            for i in match:
                if (i in staged_TMN_list):
                    # increment that topic
                    staged_TMN_list[i] += 1
                else:
                    # add topic to list
                    staged_TMN_list[i] = 1

        match = re.findall(r'[N]+[1-4]', tweet)
        if match:
            for i in match:
                if (i in staged_TMN_list):
                    # increment that topic
                    staged_TMN_list[i] += 1
                else:
                    # add topic to list
                    staged_TMN_list[i] = 1

        match = re.findall(r'[M]+[1-4]', tweet)
        if match:
            for i in match:
                if (i in staged_TMN_list):
                    # increment that topic
                    staged_TMN_list[i] += 1
                else:
                    # add topic to list
                    staged_TMN_list[i] = 1

def return_lists():
    return staged_list