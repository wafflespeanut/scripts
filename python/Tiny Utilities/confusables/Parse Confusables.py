# Characters were robbed from http://www.unicode.org/Public/security/revision-06/confusables.txt
# and filtered using Daniel's awesome suggestion for 'printable' ASCII replacements (https://github.com/rust-lang/rust/issues/25957#issuecomment-107812945)
# egrep -v '^[ ]*#' confusables.txt | egrep -v '^[ ]+$|^$' | egrep '00(2[1-9A-F]|3[A-F]|40|5[BCDF]|7[BCD])' | egrep ';[^0-9A-F]00.. ;' | egrep -v '^00' > CONFUSABLES.txt

def const_array_of_strings(name, type_spec = "&'static str"):
    return [unicode("const %s: &'static [%s] = &[" % (name, type_spec))]

arrays = [const_array_of_strings('ASCII_ARRAY', "(char, &'static str)"),
          const_array_of_strings('UNICODE_ARRAY', 'char'),
          const_array_of_strings('SUB_ARRAY', "(usize, &'static str)"),]
lengths = map(lambda arr: len(arr[0]), arrays)

def format_for_type(thing):
    if type(thing) is unicode or type(thing) is str:
        if len(thing) == 1 or (thing.startswith('\\') and len(thing) == 2):
            return u"'%s'" % thing
        return u'"%s"' % thing
    return u'%s' % thing

def put_into_list(list_at_work, initial_len, stuff, limit = 100):
    if len(stuff) > 1:
        uni_str = u'(' + u', '.join([format_for_type(thing) for thing in stuff]) + '), '
    else:
        uni_str = format_for_type(stuff[0]) + u', '
    if len(list_at_work[-1] + uni_str) >= limit:
        list_at_work.append(u'\n' + u' ' * initial_len + uni_str)
    else:
        list_at_work[-1] += uni_str

with open('CONFUSABLES.txt', 'rb') as file_data:
    uni_list, ascii_list = [], []
    for line in file_data.readlines():
        stuff = line.decode('utf-8').split(u'\u2192')
        char_vals = stuff[0].split(';')
        u_char, sub_char = str(char_vals[0].rstrip()), str(char_vals[1].strip())
        u_name = str(stuff[1][(stuff[1].find(')')):].strip(') ')).title()
        sub_name = str(stuff[2][:stuff[2].find('#')].strip()).title()

        uni_char = unichr(int(u_char, 16))
        if uni_char not in uni_list:        # too many duplicates really
            uni_list.append(uni_char)
            put_into_list(arrays[1], lengths[1], [uni_char])
            ascii_char = unichr(int(sub_char, 16))
            ascii_char = '\\' + ascii_char if ascii_char in '\'"\\' else ascii_char
            try:
                idx = ascii_list.index((ascii_char, sub_name))
                put_into_list(arrays[2], lengths[2], [idx, u_name])
            except ValueError:
                put_into_list(arrays[2], lengths[2], [len(ascii_list), u_name])
                ascii_list.append((ascii_char, sub_name))
                put_into_list(arrays[0], lengths[0], [ascii_char, sub_name])

arrays = map(lambda arr: u''.join(arr) + u'];' , arrays)
with open('unicode_chars.rs', 'wb') as file_data:
    file_data.write(u'\n\n'.join(arrays).encode('utf-8'))
