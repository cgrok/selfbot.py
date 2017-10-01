

def paginate(text: str, maxlen: int):
    '''Simple generator that paginates text.'''
    last = 0
    for curr in range(0, len(text)+maxlen, maxlen):
        if last == curr:
            continue
        else:
            yield text[last:curr]
            last = curr


def shlex_split(body):
    '''Function that splits on spaces while retaining quoted peices of text'''

    curr = ''
    is_quoted = False
    is_first = False
    args = []

    for index, char in enumerate(body):

        if char == '"':
            if body[index-1] != '\\': # escapes
                is_quoted = True
                is_first = False if is_first else True
                    
        if is_quoted:
            curr += char
            if not is_first:
                args.append(curr)
                curr = ''
                is_quoted = False
        else:
            if char.isspace():
                args.append(curr)
                curr = ''
            else:
                curr += char

        if index+1 == len(body):
            if is_first:
                curr = curr.split()
                args.extend(curr)
            else:
                args.append(curr)

    args = list(filter(lambda x: x.strip(), args)) # takes out spaces

    for i, arg in enumerate(args):
        arg = arg.replace('\\"', '"') # escapes
        if arg.count(' '):
            arg = arg.strip('"') # removes the quotes
        args[i] = arg

    return args




