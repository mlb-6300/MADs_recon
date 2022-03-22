
from flask import Flask
from bs4 import BeautifulSoup
import collections

app = Flask(__name__)

collections.Callable = collections.abc.Callable

# essentially want to parse the xml file (ETD-NAF...), extract the URI from the appropiate tags, get the the member's name from a tag,
# crawl the 

# hash map (dict) with the keys as the URIs and values as the name

# need to read more about how this is implemented with openrefine

# ../source_files/ETD-NAF_mads_20220222.xml
# ../source_files/source_pdfdata_2021Su.xml
with open("../source_files/ETD-NAF_mads_20220222.xml", "rb") as fp:
    soup = BeautifulSoup(fp, "xml")

# proper syntax test = soup.find('mads:name')['authorityuri']

# iterates through all the names and grabs the authority URI, main logic
# need to change it up, create a dict with the uris and names
for name in soup.find_all("mads:name"):
    # ignores duplicate names! such as preferred names
    if "variant" in name:
        continue
    uri = name.get("valueURI")
    firstName = name.find('mads:namePart')
    
    if (uri == None):
        continue
    # value uris are either from loc or lib.fsu. the ones at lib.fsu are not real links. intentional?

    print(firstName)
    #print(uri)


"""# gets all committee member names
names = soup.find_all('mads:name')
for name in names:
    print(name.text)"""


"""
@app.route("/test", methods=["GET"])
def test():
    return


if __name__ == "__main__":
    # defaults to localhost port 5000
    app.run(debug=True)
"""