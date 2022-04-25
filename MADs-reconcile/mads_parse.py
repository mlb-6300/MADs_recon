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


        for name in soup.find_all("mads:mads"):
            #l_var = soup.find("mads:variant", type="family")
            #f_var = soup.find("mads:variant", type="given")

            # use this for things
            uri = (name.find('mads:authority')).find('mads:name').get("valueURI")
            if uri is None:
                continue

            l = (name.find('mads:authority').find('mads:name', type="personal")).find('mads:namePart', type='family').get_text()
            try:
                l2 = (name.find('mads:variant').find('mads:name', type="personal")).find('mads:namePart', type='family').get_text()
            except:
                l2 = ""
            
            f = (name.find('mads:authority').find('mads:name', type="personal")).find('mads:namePart', type="given").get_text()

            try:
                f2 = (name.find('mads:variant').find('mads:name', type="personal")).find('mads:namePart', type='given').get_text()
            except:
                f2 = ""
            
            # clean up names here
            f = re.sub(r'\([^)]*\)', '', f)
            f = f.rstrip()

            
            """
            uri = name.get("valueURI")

            # if someone does not have a uri, they simply should not be in the dict (imo). when we go to reconcile, no uri will pop up, as it should be
            if (uri == None):
                continue
        
            # grabbing first and last name
            l = name.find('mads:namePart', type="family")
            f = name.find('mads:namePart', type="given")

            # maybe store value as a tuple? tuple1 will be the first name
            # second tuple will be the related/variant names

            # then when checking in search() compare against both? gonna have duplicate code more than likely

            # if i run find on the tags again, will it grab the same stuff? or does it move on?
            
            # if empty family field (more so the field doesn't exist), continues in the loop 
            if l is None:
                continue
            
            # can boil all this down to one line of code, clean later 
            lastname = l.get_text()
            firstname = f.get_text()
            
            #l2 = name.find('mads:namePart', type="family")
            #f2 = name.find('mads:namePart', type="given")

            #lastname2 = l2.get_text()
            #firstname2 = f2.get_text()
    
            # for people with parans, ex. Susan C. (Susan Carol), gets rid of that, and strips extra whitespace
            firstname = re.sub(r'\([^)]*\)', '', firstname)
            firstname = firstname.rstrip()

            #firstname2 = re.sub(r'\([^)]*\)', '', firstname2)
            #firstname2 = firstname2.rstrip()


            # need to my_strip hyphenated names, replace with whitespace
            lastname = lastname.replace("-", " ")
            lastname = unidecode(lastname)
            firstname = unidecode(firstname)

            #lastname2 = lastname2.replace("-", " ")
            #lastname2 = unidecode(lastname2)
            #print(lastname + ", " + firstname)
            #print(uri)

            # adding pair to dict, uri as key and name as value
            # store name as Last, First        
            
            # not lists, tuple two names together
            # if lastname and firstname are empty, just empty strings

            self.uris_names[uri] = ((lastname+ ", " + firstname), variants[counter])
            """
            

        #print(variants)
        #self.uprint()

    def uprint(self):
        for k,v in self.uris_names.items():
            print(v)
        
    # returns name with hyphens and commas stripped from string
    def my_strip(self, name):
        return unidecode(name.replace("-", " ").replace(".", ""))

    # given a name from OpenRefine, search the dict for the name in the value, return a list of URIs
    def search(self, name, query_type=''):
        uris = []

        for k,v in self.uris_names.items():
            # v will now be a tuple here. check if the second (v[1]) is equal to "", if not, there's a variant
            # should search make comparisons to both. not sure how yet
            if self.my_strip(name) in self.my_strip(v) or self.my_strip(v) in self.my_strip(name):
                # after checking if name is in v or v is in name, perform anyother check for if v (from mads)
                # is in name, if it ISN'T non-perfect score because non-perfect match
                if self.my_strip(v) in self.my_strip(name):
                    uris.append({
                        "id": k,
                        "name": name,
                        "score": 1,
                        "match": True
                    })
                else:
                    uris.append({
                        "id": k,
                        "name": name,
                        "score": .80,
                        "match": False
                    })
            
            # if no perfect match, checks for last name prescence. Just last name match is a score of .5
            elif (re.split('\s|, ', self.my_strip(name)))[0] in (re.split('\s|, ', self.my_strip(v))):
                uris.append({
                    "id": k,
                    "name": v,
                    "score": .5,
                    "match": False
                })
            
                # split after comma, tokenize the rest of the name
                tokens = ((self.my_strip(name))).split(',', 1)[-1].lstrip()
                tokens = tokens.split()
                # want to exclude middle initials
                for string in tokens[:]:
                    if len(string) == 1:
                        tokens.remove(string)

                # checking for presence of first name or full middle name, increases match score to .75
                if any(ext in v for ext in tokens):
                    uris[-1].update({"score":.75})
                    # if you want scores of .75 to auto match, uncomment this out
                    # uris[-1].update({"match":True})

                # maybe if just first name, .25? 
            
        # if there is only one match in the list, will automatch 
        if (len(uris) == 1):
            uris[-1].update({"match":True})
        
        # if there's only two matches in the list, will automatch on the highest score
        if (len(uris) == 2):
            if (uris[0].get("score") > uris[1].get("score")):
                uris[0].update({"match":True})
            elif (uris[0].get("score") < uris[1].get("score")):
                uris[1].update({"match":True})


        return uris
        """
        out = open("problemNames.txt", "a")
        name = name + "\n"
        out.write(unidecode(name))
        out.close()
        """

if __name__ == "__main__":
    parse = MADsParser()
