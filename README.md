# MADs Reconciliation Project

## File Listing
### MADs-reconcile
  - app.py 
    - Flask application home. 
  - mads_parse.py
    - Parses XML file for faculty names and URIs and stores in an internal list. Contains functions for searching for a URI.
  - requirements.txt
    - Python module requirements
### source_files
  - ETD-NAF_mads_20220222.xml
    - Contains committee member names and URIs
  - pdfdata_names_2021Su.dsv
    - Pipe delimited file containing committee member names, roles, and associated thesis/dissertation PDFs. Was used for testing purposes

## Requirements
  - Application module requirements are specified in `requirements.txt`.
  - Run the following command to install all required packages: `pythom -m pip install -r requirements.txt`
  - An additional requirement is that the XML file to be parsed for names and URIs must be in the same format as the ETD-NAF... file, as the parser is looking for specific tags in the file. 

## Usage
  - To run reconciliation Flask service run `python app.py` while in `MADs-reconcile` directory. If passing in XML document as command line argument, run with `python app.py <xml file>`. Make sure XML document is in the same directory as the application. Additonally, do not run with `flask run`, as it messes up command line arguments.
  - With OpenRefine running and a project opened, run the following steps:
      1. Select a column containing names in indirect order, ex. Smith, John L.
      2. Click reconcile
      3. Click start reconciling (Proceed to Step 5 if service is already added)
      4. Select "Add Standard Service" and supply the following URL `http://127.0.0.1:5000/reconcile/mads`. 
      5. Select "MADs Reconciliation Service"
      6. Supply max # of candidates to return (default is 3)
      7. Select "Start Reconciling..."

  - After the reconciliation service finishes, perfect matches with a score of 1.0 will be automatched to their correponding cell. Matches with a score of .75 are not exact matches, but pretty close, more than likely matching on the last name and the first name. Matches with a score of .5 only matched on the last name, so confidence is pretty low that these are the correct matches. Matches with a non-perfect score must be manually reviewed to select the best match. 

## Notes
  - This project is based off of source code from [mphilli's](https://github.com/mphilli) [LoC Reconcilation](https://github.com/mphilli/LoC-reconcile) project. Please see [License](https://github.com/mlb-6300/mads_recon/blob/main/LICENSE)
