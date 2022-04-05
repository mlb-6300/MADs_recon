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

## Usage
  - To run reconciliation Flask service run either `flask run` or `python app.py` while in `MADs-reconcile` directory. 
  - With OpenRefine running and a project opened, run the following steps: 
     1. Select a column containing indirect names
     2. Click reconcile
     3. Click start reconciling (Proceed to Step 5 if service is already added)
     4. Select "Add Standard Service" and supply the following URL `http://127.0.0.1:5000/reconcile/mads`. 
     5. Select "MADs Reconciliation Service"
     6. Supply max # of candidates to return (default is 3)
     7. Select "Start Reconciling..."

## Notes
  - This project is based off of source code from [mphilli's](https://github.com/mphilli) [LoC Reconcilation](https://github.com/mphilli/LoC-reconcile) project. Please see [License](https://github.com/mlb-6300/mads_recon/blob/main/LICENSE)
