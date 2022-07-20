import re

#import code
#code.interact(local=locals())

#functions for replacing regex referenced in other functions

#This is a function that is escaped. Literal string search/replace. 
def literal_replace(full_string, original, replacement):
    escaped_original = re.escape(original)
    result = re.subn(escaped_original, replacement, full_string)
    return_string = result[0]
    occurrences = result[1]
    print(f"Replaced {original} {occurrences} times")
    return return_string

#This is a regex function. You may need to escape characters. 
def regex_replace(full_string, original, replacement):
    result = re.subn(original, replacement, full_string)
    return_string = result[0]
    occurrences = result[1]
    print(f"Replaced {original} {occurrences} times")
    return return_string

#Basic replacements to do some quick clean up on docs
#This one generates a report of what changed. 
def basic_replaces(data):
    data = data.replace('\n', '')
    startchar = len(data)
    #remove span tags
    data = literal_replace(data, '<span>','')
    data = literal_replace(data, '</span>','')    
    #if p tags capitalized, make lowercase
    data = literal_replace(data, '<P>','<p>')
    data = literal_replace(data, '</P>','</p>')
    #if div, replace with p tags
    data = literal_replace(data, '<div>','<p>')
    data = literal_replace(data, '</div>','</p>')
    #FIRST BATCH ONLY: hard linebreaks become spaces. 
    data = regex_replace(data, '<br />|<Br />|<br/>|<Br/>',' ')
    #if double nested p tags, reduce to one.
    data = literal_replace(data, '<p><p>','<p>')
    data = literal_replace(data, '</p></p>','</p>')
    #if nonbreaking space, make normal space
    data = literal_replace(data, "&nbsp;", " ")
    #if trailing space at end of p tag, remove. 
    data = literal_replace(data, ' </p>','</p>')
    print("-----Space trailing paragraph text.")
    #find and remove one or more spaces
    data = regex_replace(data, "\s+\s+", " ")
    print("-----Two or more sequential spaces.")
    #paragraph with leading space
    data = regex_replace(data, r"((\<p[^>]*>)\s+)", r'\2')
    print("-----Paragraph with leading space.")
    #join words separated by hyphen space style linebreak.
    data = regex_replace(data, r"([a-z])-\s+([a-z])", r'\1\2')
    print("-----Join words separated by linebreak.")

    #uncomment below to add newlines in between paragraphs.
    data = data.replace('</p><p','</p>\n<p')

    #finish the data with counting characters changed
    endchar = len(data)
    print(f"Starting character count is {startchar}, ending character count is {endchar}, so total change is {startchar - endchar} characters.")
    return data

#old control file from testing so I could get a good view of what changed.
def controlfile(data):
    data = data.replace('\n', '')
    data = data.replace('<P>','<p>')
    data = data.replace('</P>','</p>')
    data = data.replace('<Br />','<br />')
    data = data.replace('<br />',' ')
    data = data.replace('</p><p','</p>\n<p')
    return data

def pagenums():
    pass
    #This section is for adding page number formatting, in progress. 
    """
    #  <p>[3]&nbsp;&nbsp;</p> 
        data = regex_replace(data, r"((\<p[^>]*>)\[(\d{1,2})\]\s*\</p>)", r'<p class="text-align-right">\3</p>')
        print("-----Page numbers formatted like <p>[3]&nbsp;&nbsp;</p> or <p>[3]</p> ")
                    #Custom change text to remove running head:  <p>-3- general</p> 
        #data = regex_replace(data, r"((\<p[^>]*>)-(\d{1,2})-\s*\ general</p>)", r'<p class="text-align-right">\3</p>')
    # print("-----Page numbers formatted like <p>[3]&nbsp;&nbsp;</p> or <p>[3]</p> ")
    #<p>-3-</p> 
        data = regex_replace(data, r"((\<p[^>]*>)-(\d{1,2})-\s*\</p>)", r'<p class="text-align-right">\3</p>')
        print("-----Page numbers formatted like <p>-3-&nbsp;&nbsp;</p> or <p>-3-</p> ")
    #<p>- 3 -</p> 
        data = regex_replace(data, r"((\<p[^>]*>)-(\d{1,2})-\s*\</p>)", r'<p class="text-align-right">\3</p>')
        print("-----Page numbers formatted like <p>- 3 -&nbsp;&nbsp;</p> or <p>- 3 -</p> ")
    #Not sure that this one is doing anything: page numbers like <p>15<br />-10-</p>
        #data = regex_replace(data, r"((\<p[^>]*>)(\d{1,2})\s*\</p>)", r'<p class="text-align-right">\3</p>')
        #print("-----Page numbers formatted like <p>3&nbsp;&nbsp;</p> or <p>30</p> ")
    #More work required on the regex below:
        # page numbers with dup numbers and spaces
        #data = regex_replace(data, r"((\<p[^>]*>)(\d{1,2})[^>|^[a-z]]*</p>)", r'<p class="text-align-right">\3</p>')
        #print("-----Page numbers formatted like <p>3&nbsp;&nbsp;</p> or <p>30</p> ")
        #add whatever else. 
    """

#This takes uppercase text and provides some basic capitalization for starts of sentences. 
def fromupper(data):
    data = data.replace('\n', '')
    data = data.lower()
    data = re.sub("(^|[.?!]|<p[^>]*>)(<s>|<em>|<sup>|<i>|<b>|<strong>|<b>|\")*(\s)*([a-z])", lambda p: p.group(1) + (p.group(2) if p.group(2) is not None else '') + (p.group(3) if p.group(3) is not None else '') + p.group(4).upper(), data)
    #lowercase everything in angle brackets.
    #data = re.sub("(\<[^>]*>)", lambda p: p.group(0).lower(), data)
    data = data.replace('</p><p','</p>\n<p')
    return data

#Capitalize first letter of any words from an external list of words, caplist.txt
#Note that there is a list of words to never capitalize within this script, and words to always capitalize.
def capfix_fromlist(data):
    startchar = len(data)
    data = data.replace('\n', '')
    with open('support_files/caplist.txt', 'r') as file:
        cap_list = file.read().splitlines()
        nevercap = ['the','of','in', 'a', 'and', 'to', 'for', 'on', 'our']
        allcap = ['ii','iii','naacp','n.a.a.c.p.','u.s.','u.n.','cia','d.c.','gop',"un", "w.e.b.", 'adl','cbs','splc']
        for term in cap_list:
            print(term)
            match = term.lower()
            titlebuilder = []
            words = match.split()
            for word in words:
                if word in nevercap:
                    titlebuilder.append(word)
                elif word in allcap:
                    titlebuilder.append(word.upper())
                else:
                    titlebuilder.append(word.capitalize())

            newcap = ' '.join(titlebuilder)
            newcap = newcap.replace('\\','')
            print(newcap)
            match = re.escape(match)
            #data = re.sub(rf"(^|\s|\"|\'|\(|>)({match})(?![a-z])(\s|:|\.|,|\"|\'|;|<|$)", lambda p: p.group(1) + newcap + p.group(3), data)
            data = regex_replace(data,rf'(^|\s|\"|\'|\(|>)({match})(?![a-z])(\s|:|\.|,|\"|\'|;|<|$)', lambda p: p.group(1) + newcap + p.group(3))
        data = data.replace('</p><p','</p>\n<p')
        endchar = len(data)
        print(f"Starting character count is {startchar}, ending character count is {endchar}, so total change is {startchar - endchar} characters.")
        return data