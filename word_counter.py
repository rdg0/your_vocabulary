from typing import Dict, List, Tuple
import csv

INPUT_FILENAME = 's01e01.srt'
IRREGULAR_VERB = 'irregular_verbs.csv'
YOUR_VOCABULARY = 'my_dict.csv'
BLACKLIST = 'blacklist.csv'
OUTPUT = 'output.csv'


def get_clean_text() -> List:
    """Очищаем текст от всех лишних слов и символов."""
    alphabet = {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    }
    drop_symbols = [
        "'", ':', ';', '.', ',', '-', '#', ')', '(', '@', '%', '&', '*', '[',
        ']', '<', '>', '!', '?', '/', '\\', '0', '1', '2', '3', '4', '5', '6',
        '7', '8', '9', '"',
    ]
    with open(BLACKLIST, 'r', newline='') as f:
        table = list(csv.reader(f, delimiter=';'))
    drop_words = [word[0] for word in table]
    trans_table = str.maketrans(dict.fromkeys(drop_symbols, ' '))

    with open(INPUT_FILENAME, 'r', encoding='utf-8-sig') as f:
        text = f.read()

    word_list = text.translate(trans_table).lower().split()
    clean_word_list = []
    for word in word_list:
        if (len(word) < 3) or word in drop_words:
            continue
        clean_word_list.append(word)
    return clean_word_list


def replase_irregular_verbs(word_list: List) -> Tuple[List, List]:
    """Заменяем в тексте на базовую форму неправильные глаголы."""
    word_list_with_base_form = []
    irregular_verbs = []
    with open(IRREGULAR_VERB, 'r', newline='') as f:
        table = list(csv.reader(f, delimiter=';'))
    for word in word_list:
        is_irregular = False
        for row in table:
            if word in (row[1], row[2]):
                word_list_with_base_form.append(row[0])
                irregular_verbs.append(row[0])
                is_irregular = True
                break
        if is_irregular:
            continue
        word_list_with_base_form.append(word)
    print(f'Всего слов без всякой ерунды: {len(word_list_with_base_form)}')
    print(f'Неправильных глаголов: {len(set(irregular_verbs))}')
    return (word_list_with_base_form, irregular_verbs)


def get_count_world(world_list: List) -> Dict:
    """Считаем количество повторений слов."""
    count = {}
    for world in world_list:
        if count.get(world):
            count[world] += 1
        else:
            count[world] = 1
    sorted_values = sorted(count.items(), key=lambda tpl: tpl[1], reverse=True)
    return dict(sorted_values)


def get_out_of_vocabulary(words_dict: Dict) -> Tuple[List, List]:
    """ Получаем слова  """
    with open(YOUR_VOCABULARY, 'r', newline='') as f:
        table = list(csv.reader(f, delimiter=';'))
    new_words = {}
    vocabulary_words = {}
    for word in words_dict:
        in_vocabulary = False
        for row in table:
            if word == row[0]:
                vocabulary_words[word] = words_dict[word]
                in_vocabulary = True
                break
        if not in_vocabulary:
            new_words[word] = words_dict[word]
    with open(OUTPUT, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['word', 'qt', 'description'])
        for key, val in words_dict.items():
            if key in new_words:
                writer.writerow([key, str(val), 'new'])
            else:
                writer.writerow([key, str(val), 'vocabulary'])
    return (new_words, vocabulary_words)


def main() -> None:
    """Основная функция бота."""
    clean_text = get_clean_text()
    word_list_with_base_form, irregular_verbs = replase_irregular_verbs(clean_text)
    words_dict = get_count_world(word_list_with_base_form)
    new_words, vocabulary_words = get_out_of_vocabulary(words_dict)
    print(f'Всего слов без blacklist: {len(word_list_with_base_form)}')
    print(f'Уникальных слов в тексте: {len(words_dict)}')
    print(f'Новых слов {len(new_words)}: {new_words}')
    print(f'Из известных ранее {len(vocabulary_words)} слов.')
    print(f'Подробнее смотри в {OUTPUT}')


if __name__ == '__main__':
    main()
