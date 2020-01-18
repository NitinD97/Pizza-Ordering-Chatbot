from nltk.chat import Chat, util
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import string


lem = WordNetLemmatizer()
reflections = util.reflections


def prepare_data(sentence, stop_words=()):
    tokens_list = word_tokenize(sentence)
    tokens_list = [lem.lemmatize(token) for token in tokens_list]
    tokens_list = pos_tag(tokens_list)
    lemmatized_tokens = []
    for (word, tag) in tokens_list:
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_tokens.append(lem.lemmatize(word, pos))

    punc_less_list = []
    for token in lemmatized_tokens:
        if token not in string.punctuation and token.lower() not in stop_words:
            punc_less_list.append(token.lower())
    return punc_less_list


def get_bot_response(text):
    pairs = return_pairs_list()
    chat = Chat(pairs, reflections)
    sentences = text.split('.')
    bot_response = []
    for sentence in sentences:
        data = prepare_data(sentence, stopwords.words('english'))
        res = ' '.join(data)
        bot_response.append(chat.respond(res))
    return bot_response


def coupons():
    return 'No discount Coupons as of yet'

def order_stat():
    return 'Order is out for delivery'


def return_pairs_list():
    return [
        [
            r"hi|hey|hello",
            ["Hello, How are you today ?", ]
        ],
        [
            r"(work)(.*)",
            ["Well its a nice place!", ]
        ],
        [
            r"want|need (refund)",
            ["Redirecting to customer service", ]
        ],
        [
            r"wrong order|order wrong|wrong item|item wrong",
            ["Can you tell me the exact items that were wrong!", ]
        ],
        [
            r"replace order|order replace",
            ["Please keep the old order as a proof. The delivery person will recieve it", ]
        ],
        [
            r"food cold|cold food",
            ["Sorry for the inconvinence. This won't happen the next time.", ]
        ],
        [
            r"item present|missing item",
            ["Can you tell me the exact items that were missing!", ]
        ],
        [
            r"eta|time|wait|arrive",
            ["The food will arrive in some time.", ]
        ],
        [
            r"order|status|deivered|deliver|food|recieve|receive",
            [order_stat()]
        ],
        [
            r"coupon work|discount work|coupon apply|discount apply",
            ["Sorry, can you please send me the coupon code!", ]
        ],
        [
            r"coupon|discount",
            ["Currently no coupon code is available!", ]
        ],
        [
            r"(.*)",
            ["Sorry, Did not get you!", ]
        ],

    ]
