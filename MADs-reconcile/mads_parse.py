from bs4 import BeautifulSoup
import collections
import re
from unidecode import unidecode

class MADsParser: 
    collections.Callable = collections.abc.Callable
    uris_names = {}
    
    # default constructor initializes the iternal dict of uri/name pairs. 
    def __init__(self):
        counter = 0

        # inits BeautifulSoup parse object with the etd-naf_mads source file
        with open("../source_files/ETD-NAF_mads_20220222.xml", "rb") as fp:
            soup = BeautifulSoup(fp, "xml")

        # lookup will be done by value, return multiple keys if value occurs more than once
        # will be left to choose in openrefine
        
        # iterating through the name tags 
        for name in soup.find_all("mads:name"):
            # ignores duplicate names! such as preferred names
            if "variant" in name:
                continue
            # ignores related names as well
            if "related" in name:
                continue

            # grabbing the uri
            uri = name.get("valueURI")

            # if someone does not have a uri, they simply should not be in the dict (imo). when we go to reconcile, no uri will pop up, as it should be
            if (uri == None):
                continue
        
            # grabbing first and last name
            l = name.find('mads:namePart', type="family")
            f = name.find('mads:namePart', type="given")
            
            # if empty family field (more so the field doesn't exist), continues in the loop 
            if l is None:
                continue
            

            lastname = l.get_text()
            firstname = f.get_text()
            
            # for people with parans, ex. Susan C. (Susan Carol), gets rid of that, and strips extra whitespace
            firstname = re.sub(r'\([^)]*\)', '', firstname)
            firstname = firstname.rstrip()

            # need to strip hyphenated names, replace with whitespace
            lastname = lastname.replace("-", " ")
            lastname = unidecode(lastname)
            firstname = unidecode(firstname)

            # maybe check to see if a lastname is two words?
            # if it is, strip the first part and add to first name?
            # consistency issues with hyphenated last names, need to get all edge cases

            #print(lastname + ", " + firstname)
            #print(uri)

            # adding pair to dict, uri as key and name as value
            # store name as Last, First        
            self.uris_names[uri] = lastname +", " + firstname


    # given a name from OpenRefine, search the dict for the name in the value, return a list of URIs
    
    def search(self, name, query_type='', limit=3):
        uris = []
        for k,v in self.uris_names.items():
            # try catch, if name is not in v, try stripping the comma, index the first element (lastname), check 
            # if in v again, if it, multiple matches? 
            if unidecode(name.replace("-", " ")) in v:
                uris.append({
                    "id": k,
                    "name": name,
                    "score": 1, 
                    "match": True
                })
                return uris

        out = open("problemNames.txt", "a")
        name = name + "\n"
        out.write(unidecode(name))
        out.close()

        return 

if __name__ == "__main__":
    parse = MADsParser()
