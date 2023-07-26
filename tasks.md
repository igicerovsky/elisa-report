# Photometer Report Generation Tasks - Python

## TODO

- formatting docx, pdf
- Further review process ???
- Unit tests
  - modules
- Documentation
  - modules
- Parameters
  - `Reference value`
  - `Dilutions`

## Done

### KW31-01.08.2023

- convert to pdf `pandoc` using `pdflatex` engine  

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
