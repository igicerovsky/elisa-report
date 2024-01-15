
# Photometer Report Generation Tasks - Python

## TODO

- 231213_AAV9-ELISA_sey_GN004240-068; plate 3; why is masked second point and not first??? see fitting
- add description of graphs to README.md, symbol meaning (croos, circle, -) [Ewald Fri 12/15/2023 2:04 PM]
- check correctness of the exported `*.txt` filename for given plate
- save final results with `,` decimal delimiter for Andrea
- Further review process ???
- Unit tests
  - modules
- Documentation
  - modules

## Review

- Sample mean multiply (Andrea) in sample overview; add if easy  

## Done

## KW03-15.01.2024

- in progress..

## KW01-08.01.2024

- new version deployed
- invstigating fit

### KW01-02.01.2024-Prot-Quant Meeting

- `<LOQ`, `>ULOQ` except of number in `mask_reason`
- refactoring removing unused code, params
- rm deprecated `--calc` input remnants
- MS Word final report building programmatically
- insert sheet to Word final results; configuring the formatting
- page break in Word (sheet is not split on page end)

### KW52-18.12.2023

- profiling (find bottlenecks): image generating is slow
- exception handling added to main script
- configure initial analysis folder `--ifld` argument
- `Cancel` select folder dialog; close window; bug fix
- page break for plate analysis PDF
- `sample` to `point` in graph legend

### KW51-11.12.2023

- masked values check [Ewald email Fri 12/15/2023 2:34 PM] `mask_reason = concentration_backfit * plate_layout_dil`
- bug fix: `ext` legend not always shown
- additional checks for correctness of input files
- GUI refactoring: only select folder dialog is displayed, ten back to stdout
- data / tests cleaning: moving files outside project folder except units tests data

### KW50-04.12.2023

- GUI with desktop link
- Ewald email 30.11.2023 (OD value vs backfitted concentration)

### KW49-27.11.2023

- `PRE_DILUTION_THRESHOLD = 10` is sample valid if dilution is `>` pre dilution threshold?
- r_squared in fit data fix if exception is thrown

### KW48-20.11.2023

- non valid values `****` in experiment 231122_AAV9-ELISA_sey_GN004240-064 `PRE_DILUTION_THRESHOLD = 10`  
- update unit tests for pre-dilution invalid results

### KW47-13.11.2023

- write markdown with `encoding='utf-8'`
- remove trailing `/\` from input path
- bug fix SOP num in final report at beginning
- bug fix reference docx join path

### KW46-7.11.2023

- use correct SOP, MHF names for `AAV*`
  - add to config
  - Die aktuellen Nummern beim AAV8-Elisa lauten: `SOP-236462`, MHF `DMD-211877`
  - Beim AAV9-Elisa lauten die Nummern: `SOP-234702`, MHF `DMD-211328`
  - update README, test
- raise exception if analysis file is not found in analysis folder (exported `txt` file from Hamilton)
- fix pandas deprecated indexing to  iloc
- update e2e test
  - for 3s limits
  - aav*[8, 9]
- config
  - directory as parameter
  - global variable
  - `init_config()` function
- merge `config.json` with `params.json` into `config.json`
  - update README.md
  - update e2e tests
- deployment to Hamilton
  - manual using `R:/`

### KW44-30.10.2023

- Validity limits
  - apply to control only
  - AAV8 3s limits <1.119E+11, 1.648E+11> [cp/ml] (see GN000168-055)
  - AAV9 3s limits <1.888E+12, 2.703E+12> [cp/ml]
  - if not valid (*value*); comment `test invalid`
  - write to md to section `Evaluation criteria` (according to aav8[9]); final report
  - update unit e2e tests
- `params.json` refactoring AAV8, AAV9 parameters grouping

### KW43-23.10.2023

- update reading reference values AAV8, AAV9, default
  - update `parameters.json`
  - update code
  - update documentation
- Unit tests
  - new e2e test using `txt` input
- Blank sample `b` not in `*_report_plate[n].md`
  - update unit tests
- fix order of images in pdf

### KW42-16.10.2023

- Blank sample `b` not in `*_report_plate[n].md`
  - implementation
- Pre-dilution shall be read from separate file and used in computation of final results (read in `make_final` function?)

### KW36-04.09.2023

- Word formatting, reference document for `pandoc`
- Exception handling for pandoc calls

### KW33-15.08.2023

- package `hamrep` setup and versionning (including module refactoring)
- Hamilton computer integration
  - command line run on data produced by Hamilton
  - intergration into Hamilton software
- decouple pandoc generation code (`./data/config.json` contains paths to pandoc, latex, reference doc)
- README.md update

### KW32-08.08.2023

- Pythom module distribution package
- version handling
- dummy test script for Hamilton integration check
- `__` remove in `txt` file
- Hamilton new version deployment
- Use original photometer output
  - script
  - batch
- Results word document
- formatting docx, pdf
- Documentation `README.md` update

### KW31-01.08.2023

- Bug fix: backfit produces `nan` for `230712_AAV8-ELISA_sey_GN004240-048`
- Parse original output from photometer
  - encoding (UTF_16)
  - file processing
  - merge to computing framework
- convert to pdf `pandoc` using `pdflatex` engine  
- formatting docx, pdf - stage 0
- Review: Rounding style (Andrea) checked - OK
- Masking 1 vs 2 values `results_plate_1\230628_GN004240-046_-_report_plate_1.md` (Andrea) checked - OK
- Parse, format and output datetime to header
- Parsing -> sample info from dir name (Andrea)
- Parameters read from json
  - `Reference value`
  - `Dilutions`

### KW30-25.07.2023

- Batch directory processing  
- Input as directory for processing  
  - ipynb
  - py
- Pandoc `docx` report generation  
  - equation using `\frac`  
  - included in report generation ipynb
- E2E test  

### KW29-17.07.2023

- SOPs
- Unit tests & docs (fit function)
- batch

To check  
[230628_GN004240-046_-_report_plate_1.md.pdf](https://mytakeda.sharepoint.com/:b:/r/sites/PA.GTProtein-Quantification/Shared%20Documents/General/Team-Members/cerovskyi/230628_GN004240-046_-_report_plate_1.md.pdf?csf=1&web=1&e=Nikrw1)  
[230628_GN004240-046_-_report_plate_2](https://mytakeda.sharepoint.com/:b:/r/sites/PA.GTProtein-Quantification/Shared%20Documents/General/Team-Members/cerovskyi/230628_GN004240-046_-_report_plate_2.md.pdf?csf=1&web=1&e=xoPKJs)

### KW28-11.07.2023

Review Sebasitian, Felix  

- mask sample point(s) if `CV>CV_THRESHOLD` and `valid sample_ponits <= MIN_VALID_SAMPLE_POINTS` (Igor)
- `CV[%]` one `{:.1f}` decimal digit (Felix)
- `Result [cp/ml]` three `{:.3e}` (Felix)
- `nan` -> `NA` (Felix)
- control sample image line ending (Sebastian)
- `CV[%]` column format to 1 decimal digits with trailing zeroes (Sebastian/Robert)
- Fit parameter description

### Old

- backfit - recovery rate
- rm reference from final results
- mask samples + reason (<[>] as reference)
- sample procesing output as dictionary
- CV masking  <= 20%
- notes for masking reason
- notes in final result sheet
- reference point removal verbose output to sheet
- CV from valid (non-masked) values only

## Notes

- weasyprint
- GTK
- md2pdf
  - ??? error programmatically add images  

[teams link](https://mytakeda.sharepoint.com/:f:/r/sites/GeneTherapyAnalytics2/Freigegebene%20Dokumente/General/3_Teams/3.1_Protein_Quantification/_report_generation?csf=1&web=1&e=BtRjmZ)
