import os
import verb_forms_finder as vff

folder = 'realec_0516'
patterns = set() # сет предложений для теста
corrections = set() # сет правильных форм

def correction(lines, ID):
    right_part = ''
    for line in lines:
        if 'AnnotatorNotes' in line and ID in line and 'lemma' not in line:
            right_part = ' '.join(line.split()[3:])
            if 'OR' in right_part:
                right_part = right_part[:right_part.find('OR')]
    if right_part is not None:
        return right_part

for f in os.listdir(folder):
    if '.ann' in f:
        with open(os.path.join(folder, f), encoding = 'utf-8') as annotation:
            lines = annotation.readlines()
            twin = f.split('.')[0] + '.txt'
        with open(os.path.join(folder, twin), encoding = 'utf-8') as text:
            words = text.read()

        for item in lines:
            if 'Voice_choice' in item:
                left_border, right_border = int(item.split()[2]), int(item.split()[3])
                correction_id = item.split()[0]
                wrong_part = words[left_border : right_border]
                sentence = wrong_part + ' '
                i = left_border - 1
                u = right_border

                while words[i] != '.': # конечно, можно было бы просто найти в множестве sentences объект, содержащий строку с ошибкой, но это рискованно, потому что не исключена омонимия
                    sentence = words[i] + sentence
                    i -= 1
                if 'although' in sentence:
                    break
                else:
                    while words[u] != '.' and words[u] != '?' and words[u] != '!':
                        u += 1
                        sentence = sentence + words[u] # проверяем предложение на соответствие условию из Blank51
                        sentence.replace(wrong_part, correction(lines, correction_id))
                        patterns.add(sentence.strip())


           
for pattern in patterns:
    lemmas = pattern.split()
    for lemma in lemmas:
        if vff.find_verb_forms(lemma):
            for key, val in vff.find_verb_forms(lemma).items():
                lemma   
    
#{'3SG': 'closes', 'gerund': 'closing', '2nd': 'closed', '3rd': 'closed'}
