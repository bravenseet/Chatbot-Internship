from spire.doc import *
from spire.doc.common import *
from pprint import pprint

def extracting():
    # Copy text from document
    document = Document()
    document.LoadFromFile("guide.docx")

    text = document.GetText()

    # Split heading tag
    t1 = text.split('<heading>')
    t1.pop(0)
    comps = len(t1)

    g = 1
    lc = [] # List of components (dictionary)
    for i in range(comps):
        csub = [] # Subs
        cpoi = [] # Pointers
        t2 = t1[i]
        comp_s = t2.split('\r\n')

        # Classifying the components
        cname = comp_s[0]
        comp_s.pop(0)
        for j in comp_s:
            if j == '':
                comp_s.remove(j)
        
        # Making the list into a string for splitting and joining for <sub>
        s1 = ' '.join(comp_s).split('<sub>')
        checkDesc = 0
        for k in s1: # Getting description
            if "<desc>" in k:
                cdesc = k.split("<desc>")[-1]
                s1.remove(k)
                checkDesc = 1
            elif k == '':
                s1.remove(k)
            
        length = len(s1)
        for l in s1: # Getting sub & pointers
            s2 = l.split('* ')
            csub.append(s2[0])
            s2.pop(0)
            cpoi.append(s2)

        if checkDesc == 0:
            cdesc = ''
        

        # Adding components together
            
        dict = {
            "Component": cname,
            "Description": cdesc
        }

        for el in range(length):
            dict[csub[el]] = cpoi[el]

        lc.append(dict)

    return lc

if __name__ == "__main__":
    li = extracting()
    pprint(li)