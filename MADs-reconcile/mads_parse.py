from bs4 import BeautifulSoup
import collections
import re
from unidecode import unidecode

class MADsParser: 
    collections.Callable = collections.abc.Callable
    uris_names = {}
    
    # constructor initializes the iternal dict of uri/name pairs. Has a default parameter of 
    # the following XML file. User can pass in any xml file through command line instead
    def __init__(self, xml_file="../source_files/ETD-NAF_mads_20220222.xml"):
        # inits BeautifulSoup parse object with the etd-naf_mads source file
        with open(xml_file, "rb") as fp:
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
            
            # can boil all this down to one line of code, clean later 
            lastname = l.get_text()
            firstname = f.get_text()
            
            # for people with parans, ex. Susan C. (Susan Carol), gets rid of that, and strips extra whitespace
            firstname = re.sub(r'\([^)]*\)', '', firstname)
            firstname = firstname.rstrip()

            # need to strip hyphenated names, replace with whitespace
            lastname = lastname.replace("-", " ")
            lastname = unidecode(lastname)
            #print(lastname + ", " + firstname)
            #print(uri)

            # adding pair to dict, uri as key and name as value
            # store name as Last, First        
            self.uris_names[uri] = lastname +", " + firstname

    # returns name with hyphens and commas stripped from string
    def strip(self, name):
        return unidecode(name.replace("-", " ").replace(".", ""))

    # given a name from OpenRefine, search the dict for the name in the value, return a list of URIs
    def search(self, name, query_type=''):
        uris = []

        for k,v in self.uris_names.items():
            # checks for perfect name match, works for almost all names
            if self.strip(name) in self.strip(v) or self.strip(v) in self.strip(name):
                uris.append({
                    "id": k,
                    "name": name,
                    "score": 1,
                    "match": True
                })
            
            # if no perfect match, checks for last name prescence. Just last name match is a score of .5
            elif (re.split('\s|, ', self.strip(name)))[0] in (re.split('\s|, ', self.strip(v))):
                uris.append({
                    "id": k,
                    "name": v,
                    "score": .5,
                    "match": False
                })
            
                # split after comma, tokenize the rest of the name
                tokens = ((self.strip(name))).split(',', 1)[-1].lstrip()
                tokens = tokens.split()
                # want to exclude middle initials
                for string in tokens[:]:
                    if len(string) == 1:
                        tokens.remove(string)

                # checking for presence of first name or full middle name, increases match score to .75
                if any(ext in v for ext in tokens):
                    uris[-1].update({"score":.75})

                # maybe if just first name, .25? 
                
        return uris
        """
        out = open("problemNames.txt", "a")
        name = name + "\n"
        out.write(unidecode(name))
        out.close()
        """

if __name__ == "__main__":
    parse = MADsParser()
