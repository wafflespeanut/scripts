HTML_ESCAPE_DECODE_TABLE = { "#39"   : "\'",
                             "quot"  : "\"",
                             "#34"   : "\"",
                             "amp"   : "&",
                             "#38"   : "&",
                             "lt"    : "<",
                             "#60"   : "<",
                             "gt"    : ">",
                             "#62"   : ">",
                             "nbsp"  : " ",
                             "#160"  : " "   }

def translate_html(html_fragment):
    txt = ""
    parser_reg=""
    parser_state = "TEXT"
    
    for x in html_fragment:
        parser_reg += x     
        if parser_state == "TEXT":
            if x == '<':
                parser_state = "TAG"
            elif x == '&':
                parser_state = "ESCAPE"
            else:
                txt += x
                parser_reg = ""
        elif parser_state == "TAG":
            if x == '>':
                parser_state = "TEXT"

                tag = parser_reg

                if tag[1:-1] == "br" or tag[1:4] == "br ":
                    txt += "\n"
                elif tag == "</table>":
                    txt += "\n"
                elif tag == "<p>":
                    txt += "\n\n"

                parser_reg = ""
                
        elif parser_state == "ESCAPE":
            if x == ';':
                parser_state = "TEXT"

                esc = parser_reg[1:-1]
                
                if esc in HTML_ESCAPE_DECODE_TABLE:
                    txt += HTML_ESCAPE_DECODE_TABLE[esc]
                else:
                    txt += " "
                    
                parser_reg = ""

    if type(txt) is unicode:
        txt = unicode_to_ascii(txt)
        
    return txt

def unicode_to_ascii(s):
    ret = ""
    for ch in s:
        try:
            ach = str(ch)
            ret += ach
        except UnicodeEncodeError:
            ret += "?"
    return ret
