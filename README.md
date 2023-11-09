# Report Generation

Python project for automatic report generation from Hamilton measurements.

## Prerequisities

To install python libraries use

```bash
pip install -r requirements.txt```
```

Install `pandoc` frpm [pandoc](https://pandoc.org/installing.html) website.  

Install `latex` from any of the [distributions](https://www.latex-project.org/get/#tex-distributions).  

## Buld distribution of `hamrep`

For experts only!  
To build a hemrep library execute following command:

```bash
python -m build --sdist --wheel
```

## Running the script

`DIR_NAME` is path to a folder with finished Hamilton analysis, e.g. `C:/work/report-gen/reports/230426_AAV9-ELISA_igi_GN004240-033`  
The working directory **must** contain following files in given format:  

- `[DATE]_[GN]_-_worklist-ELISA.xls`
- `[DATE]_[GN]_-_[PROTOCOL]_Parameters.csv`

where `[DATE]` is a date in format `%y%m%d` (*230801*)  
`[GN]` is analysis identifier (*GN004240-033*)  
`[PROTOCOL]` is a protocol name (*AAV9-ELISA*)

Examples:  
`230426_GN004240-033_-_worklist-ELISA.xls`  
`230426_GN004240-033_-_AAV9-ELISA_Parameters.csv`

### Config file `config.json`

Command line argument is used to define a folder containing configuration file, and other files necessary to execute `report_gen.py` programm.  

```bash
python report_gen.py DIR_NAME --cfg ./data
```

**Important: if relative path is used for `--cfg` argument, the path is relative to the current execution/working directory!**  
To make sure intended folder path is used, provide absolute path.

```bash
python report_gen.py DIR_NAME --cfg C:/work/report-gen/data
```

Configuration file `config.json` is a json format file containing configurable parameters. It could be located in either default folder `./data` or in local analysis folder. If the file located in the **analysis** folder it has precedence (is meant to be modified by a user). Though, if the parameters file is not found in analysis folder it is read from the default location in the `./data` folder.  
`referenceValue` is identified automatically from the `DIR_NAME` (see above). If the `DIR_NAME` contains a string `AAV8` or `AAV9` reference value for given AAV* is used, otherwise a default value `referenceValue` is used. **If default reference value is used, user is responsible to multiply the result correspondlingly.**  

Validity limits are defined for AAV9, AAV8 or default. Test validity is checked according to 3σ limits. Control result shall be within interval <`limits[0]`, `limits[1]`>.  Default limits should not be used, and are defined so that the `report_gen` doesn't thow exception (fail).  

The file shall contain entries listed below.

```json
{
    "pandoc_bin": "c:/work/pandoc/pandoc",
    "pdflatex_bin": "c:/Users/hwn6193/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex",
    "reference_docx": "custom-reference.docx",
    "params_filename": "params.json",
    "plate_layout_id": "plate_layout_ident.csv",
    "plate_layout_num": "plate_layout_num.csv",
    "plate_layout_dil_id": "plate_layout_dil_id.csv",
    "numeric_warning_disable": true,
    "AAV9": {
        "referenceValue": 1.7954e+10,
        "limits": [
            1.888E+12,
            2.703E+12
        ]
    },
    "AAV8": {
        "referenceValue": 2.1167E+10,
        "limits": [
            1.119E+11,
            1.648E+11
        ]
    },
    "default": {
        "referenceValue": 1.0E+10,
        "limits": [
            1.0E+10,
            1.0E+12
        ]
    },
    "dilutions": [
        1.0,
        2.0,
        4.0,
        8.0,
        16.0,
        32.0,
        64.0
    ]
}
```

### Running with exported photometer `txt` data

This is a prefered way to run the preocessing of the results and following report generation.  
`--cfg` argument is a path of config directory, containing `params.json`, layout `*.csv` files, `custom-reference.docx` and `params.json`

```bash
python report_gen.py DIR_NAME --cfg ./data
```

### Running with pre-calculated `xls` data

This approach is deprecated, and will be removed in future versions.

```bash
python report_gen.py DIR_NAME --cfg ./data --calc
```

## HAMILTON

To export data in **TXT** format run the *SoftMax Pro* softare, and open given analysis. From the main menu choose 'Export' and select the `Export to XML XLS TXT` option.  

![softmax_menu](media\softmax_menu.png)

![softmax_export_opt](media\softmax_export_opt.png)

**Export measurements for all plates.**  

**Make sure the exported file name matches the folder name structure.**  
folder name example `230922_AAV9-ELISA_fff_GN004360-086`  
corresponding file name example `230922_AAV9-ELISA_1_20230922_103137.txt`  

Folder with Hamilton related stuff.

[Hamilton](<C:\Users\hwn6193\OneDrive - Takeda\2 Geräte\Hamilton_System>)
