import re
from num2words import num2words
from yargy.pipelines import morph_pipeline
from yargy.tokenizer import MorphTokenizer
from yargy.interpretation import fact, attribute


import yargy.interpretation as interp
from yargy.relations import number_relation
from yargy.predicates import (
    eq, in_,
    type, normalized,
    dictionary,
    gte, lte, gram
)
from yargy import (Parser,   or_, rule)

from razdel import sentenize

import pymorphy2
import pprint



morph = pymorphy2.MorphAnalyzer()
pp = pprint.PrettyPrinter(indent=4).pprint


def replace_facts(rule, func,  lines):
    parser = Parser(rule)
    res = []
    for line in lines:
        matches = parser.findall(line)
        matches = sorted(matches, reverse=True, key=lambda _: _.span)
        if matches:
            facts = matches #[_.fact for _ in matches]
            nstr = line
            for fact in facts:
                nstr = nstr[:fact.span.start]+func(fact.fact)+nstr[fact.span.stop:]
            res.append(nstr)
        else:
            res.append(line)
    return res


INT = type('INT')
NOUN = gram('NOUN')
ADJF = gram('ADJF')
PRTF = gram('PRTF')
GENT = gram('gent')
DOT = eq('.')

TOKENIZER = MorphTokenizer()

def normalize_float(value):
    value = re.sub('[,.]+', '.', value)
    value = re.sub('[\s]+', '', value)
    return float(value)


def normalize_int(value):
    value = re.sub('[\s]+', '', value)
    return int(value)

DIGIT =  rule(
    rule('-').optional(),
    INT
).interpretation(
    interp.custom(normalize_int)
)

FLOAT = rule(
    rule('-').optional(),
    INT,
    in_('.,'),
    INT
).interpretation(
    interp.custom(normalize_float)
)



GRADUS = or_(
    rule(normalized('градус'), normalized('Цельсия').optional()),
    rule('°','C')
)

Temperature = fact(
    'Temperature',
    ['amount', 'unit']
)


TEMPERATURE = rule(
    or_(FLOAT,DIGIT).interpretation(Temperature.amount),
    GRADUS.interpretation(Temperature.unit)
).interpretation(Temperature)

def Temp2Str(Temp):
    g = morph.parse('градус')[0]
    mnt = int(round(Temp.amount))
    grad = g.make_agree_with_number(abs(mnt)).word
    c = num2words(mnt, lang='ru')
    return c + ' ' + grad


def NormText(text):
    lis = [_.text for _ in sentenize(text)]

    lines = replace_facts(TEMPERATURE, Temp2Str, lis)
    return ' '.join(lines)


