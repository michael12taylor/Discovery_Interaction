from query import get_character_passages, extract_character_data, get_document_name

answers = [
    'My hair is red',
    'I like waffles',
    'I am rich',
    'I hate school',
    'I am lesbian',
    'I like milk chocolate'
]

data = []
for ans in answers:
    print('Getting results for "%s"' % ans)
    response = get_character_passages(ans)
    char_data = extract_character_data(response)
    if len(char_data) > 0:
        a = {}
        a['answer'] = ans
        a['doc_id'] = char_data[0][0]
        a['filename'] = get_document_name(char_data[0][0])
        a['passage_score'] = char_data[0][1]
        a['passage_text'] = char_data[0][2]
        data.append(a)
    else:
        print('"%s" has zero results' % ans)

print('\n\nFINAL RESULTS\n\n')
print(*data, sep='\n\n')