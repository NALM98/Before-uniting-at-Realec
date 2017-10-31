# 8.	Если при тэге Choice of voice в исправленном варианте стоит одна 3форма глагола,
# а перед ней в предложении стоит слово although,
# то вторым вариантом надо дать форму ...ing, а третьим was + 3 форма.

import os
import verb_forms_finder as vff

folder = 'realec_0516'
patterns = set() # сет предложений для теста
corrections = set() # сет правильных форм

def correction(lines, ID):
    right_part = ''
    for line in lines:
        if 'AnnotatorNotes' in line and ID in line and 'lemma' not in line: # Пометка AnnotatorNotes обозначает замены неправильных единиц правильными
            right_part = ' '.join(line.split()[3:]) # замены идут после 3 элемента
            if 'OR' in right_part:
                right_part = right_part[:right_part.find('OR')] # OR помечает 2 равнозначных варианта замены
    if right_part is not None:
        return right_part

for f in os.listdir(folder):
    if '.ann' in f: # проходим по аннотированным файлам
        with open(os.path.join(folder, f), encoding = 'utf-8') as annotation:
            lines = annotation.readlines() # строки аннотации, в которых осуществляется поиск
            twin = f.split('.')[0] + '.txt' # находим соответствующий аннотированному сырой файл
        with open(os.path.join(folder, twin), encoding = 'utf-8') as text:
            words = text.read() # текст из сырого файла

        for item in lines:
            if 'Voice_choice' in item: # поиск нужной ошибки по аннотированным строкам
                left_border, right_border = int(item.split()[2]), int(item.split()[3]) # в строках аннотации 2 и 3 объект строки - координаты ошибки в соответствующем текстовом файле
                correction_id = item.split()[0] # 0 элемент строки аннотации уникален и связывает пометки ошибок с исправлениями
                wrong_part = words[left_border : right_border] # часть предложения, содержащая ошибку
                sentence = wrong_part + ' '
                i = left_border - 1
                u = right_border

                while words[i] != '.' and words[i] != '?' and words[i] != '!': # конечно, можно было бы просто найти в множестве sentences объект, содержащий строку с ошибкой, но это рискованно, потому что не исключена омонимия
                    sentence = words[i] + sentence
                    i -= 1
                if 'although' not in sentence:
                    break
                else:
                    while words[u] != '.' and words[u] != '?' and words[u] != '!':
                        u += 1
                        sentence = sentence + words[u] # проверяем предложение на соответствие условию из Blank51
                        sentence.replace(wrong_part, correction(lines, correction_id))
                        corrections.add(correction(lines, correction_id)) # добавляем исправление в сет исправлений, чтобы потом было удобней искать исправленные места в готовых предложениях
                        patterns.add(sentence.strip())

for pattern in patterns:
    variants = set() # сет для хранения 3 вариантов ответа в каждом случае
    lemmas = pattern.split() # разбиваем предложения из нашего сета на словоформы
    for lemma in lemmas:
        if lemma in corrections:
            variants.add(lemma) # добавляем правильный ответ
            variants.add(vff.find_verb_forms(lemma)['gerund']) # добавляем как вариант ответа инговую форму
            variants.add('was' + vff.find_verb_forms(lemma)['3rd']) #  добавляем вариант ответа на was + 3 форму
    with open('variants_8.txt', 'w', encoding = 'utf-8') as output_file:
        output_string = pattern # правильное предложение
        for variant in variants:
            output_string += ', ' + variant # правильное предложение со всеми вариантами ответа
        output_file.write(output_string, end = '\n')
