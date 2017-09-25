# 9.Если в предложении есть глагол в прошедшем времени или в форме used to DO,
# а дальше после запятой идет but now, то для первого глагола надо дать три варианта:
# used to DO, would DO, had DONE

import os
import re
import verb_forms_finder as vff

folder = 'realec_0516'
questions = list()
answers = list()
verbs = list()
marks = list()
words = ''

for f in os.listdir(folder):
    if '.txt' in f:
        with open(os.path.join(folder, f), encoding = 'utf-8') as text:
            sentences = text.read()
            sentences = sentences.replace('?', '.')
            sentences = sentences.replace('!', '.')
            sentences = sentences.split('.')

            reg = re.compile(' used to [a-yA-y]+, but now')

            for sentence in sentences:
                if re.search(reg, sentence):
                    maybe_verb = re.search(reg, sentence).group()
                    maybe_verb = maybe_verb.split()[2]
                    if vff.find_verb_forms(maybe_verb):
                        verb = maybe_verb
                        verbs.append(verb)
                        answers.append(sentence)
                        questions.append(sentence.replace(verb, '?'))

