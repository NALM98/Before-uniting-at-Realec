# 10.	Тэг Preposition с исправленным вариантом before/since/until -
# дать другие варианты из этой тройки.

import os

folder = 'realec_0516'
questions = list()
answers = list()
marks = list()
   
for f in os.listdir(folder):
    if '.ann' in f:
        with open(os.path.join(folder, f), encoding = 'utf-8') as annotation:
            lines = annotation.readlines()
            twin = f.split('.')[0] + '.txt'
        with open(os.path.join(folder, twin), encoding = 'utf-8') as text:
            words = text.read()

        for line in lines:
            if 'Prepositions ' in line and ('since' in line or 'until' in line or 'before' in line):
                left_border, right_border = int(line.split()[2]), int(line.split()[3])
                correction_id = line.split()[0] # тип ошибки, который потом ищем в аннотированном тексте
                wrong_part = words[left_border : right_border]
                i = left_border - 1
                u = right_border

                for item in lines:
                    if 'AnnotatorNotes' in item and correction_id in item.split() and 'lemma' not in item:
                        right_part = ' '.join(item.split()[3:])
                sentence = right_part + ' '

                while words[i] != '.' and words[i] != '?' and words[i] != '!': # конечно, можно было бы просто найти в множестве sentences объект, содержащий строку с ошибкой, но это рискованно, потому что не исключена омонимия
                    sentence = words[i] + sentence
                    i -= 1
                while words[u] != '.' and words[u] != '?' and words[u] != '!':
                        u += 1
                        sentence = sentence + words[u] # проверяем предложение на соответствие условию из Blank51
                        
                questions.append((sentence.replace(right_part, '?')))
                answers.append((sentence))

for i in range(len(answers)):
    marks.append(0)

for i in range(len(questions)):
    print(questions[i], end = '\n')
    answer = questions[i].replace('?', input()) # эта строка не соответствует идее Multiple choice, но здесь нужно решить вопрос через интерфейс Moodle
    if answer == answers[i]:
        print('Correct answer')
        marks[i] = 1
    else:
        print('Wrong_answer')
        print(answers[i])
               
total_result = 0

for j in len(marks):
    if marks[j] == 0:
        print('Wrong answer to question ', j)
    else:
        print('You answered correctly to question ', j)
    total_result += marks[j]









