# Report Generation

Python project for automatic report generation from Hamilton measurements.

## Prerequisities

Use `pip install -r requirements.txt` to install python libraries.

Install `pandoc`  

Install `latex` from any of the [distributions](https://www.latex-project.org/get/#tex-distributions)  

## Running the script

`DIR_NAME` is path to directory/folder with Hamilton analysis, e.g. `C:/work/report-gen/reports/230426_AAV9-ELISA_igi_GN004240-033`  
The working directory **must** contain following files in given format:  

- `[DATE]_[GN]_-_worklist-ELISA.xls`
- `[DATE]_[GN]_-_[PROTOCOL]_Parameters.csv`

where `[DATE]` is date format `%y%m%d` (*230801*)  
`[GN]` is analysis identifier (*GN004240-033*)  
`[PROTOCOL]` is protocol name (*AAV9-ELISA*)

Examples:  
`230426_GN004240-033_-_worklist-ELISA.xls`,  
`230426_GN004240-033_-_AAV9-ELISA_Parameters.csv`

### Running with pre-calculated `xls` data

`python report_gen.py ./DIR_NAME --calc`  

### Running with exported `txt` data

`python report_gen.py ./DIR_NAME`
