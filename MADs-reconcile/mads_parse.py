from bs4 import BeautifulSoup
import collections
import re

class MADsParser: 
    collections.Callable = collections.abc.Callable
    dict = {}
    
    def get_dict():

        # ../source_files/ETD-NAF_mads_20220222.xml
        # ../source_files/source_pdfdata_2021Su.xml
        with open("../source_files/ETD-NAF_mads_20220222.xml", "rb") as fp:
            soup = BeautifulSoup(fp, "xml")

        # lookup will be done by value, return multiple keys if value occurs more than once
        # will be left to choose in openrefine
        
        for name in soup.find_all("mads:name"):
            # ignores duplicate names! such as preferred names
            if "variant" in name:
                continue
            if "related" in name:
                continue
            uri = name.get("valueURI")
            # dict this stuff. create an entry with the uri as the key, full name as the value
            # if the URI for someone does not exist, dont know what to do rn, needs to be unique. make one up? no.
            # if someone does not have a uri, they simply should not be in the dict (imo). when we go to reconcile, no uri will pop up, as it should be
            l = name.find('mads:namePart', type="family")
            f = name.find('mads:namePart', type="given")
            if l is None:
                continue
            lastname = l.get_text()
            firstname = f.get_text()
            
            # handle no uri here. 
            if (uri == None):
                continue
            
            # value uris are either from loc or lib.fsu. the ones at lib.fsu are not real links. intentional?
            # for people with parans, ex. Susan C. (Susan Carol), gets rid of that, and strips extra whitespace
            firstname = re.sub(r'\([^)]*\)', '', firstname)
            firstname = firstname.rstrip()
            dict[uri] = firstname + " " + lastname

    def search_dict(name):
        return
