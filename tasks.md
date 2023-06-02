# Photometer Report Generation Tasks - Python

## Data Processing

- Read excel data
  - Dataframe rearangement
  - Indexing according to `220726_SOP_Capsid-AAV9-ELISA_V4`
- Layouts
  - Plate layout indexing (multi index columns <1, 12>, rows <A, H>)
  - Read/reodrer functions for list input
  - Save/Read routines for reodered list input

### Fit

- Reference
  - Fitting algorithm [scipy.curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html#scipy-optimize-curve-fit)
  - Fitting plot
  - Error tabular output
  - Masking: automatic removal of outlayer
- Measurement
  - Apply reference fit
- Automatic fit point removal if outside error interval *eps*

## Final Tabular Output

- Use fit functionality to process all data
  - Display plate format
  - Custom plate formats

## Report Generation ([Markdownn](https://www.markdownguide.org/basic-syntax/))

- Tables
- Images
- ...

## Report Print to PDF

- weasyprint
- GTK
- md2pdf
  - ??? error programmatically add images

## Done

- backfit - recovery rate
- rm reference from final results
- mask samples + reason (<[>] as reference)
- sample procesing output as dictionary
- CV masking  <= 20%
- notes for masking reason
- notes in final result sheet
- reference point removal verbose output to sheet

## TODO

- CV from valid (non-masked) values only
- Backfit table mark masked value (visualy)
- Parameter file loading
  - REF_VAL_MAX
  - DILUTIONS
  - CV masking threshold
  - `fit_reference_auto_rm` verbose output
  - R_squared add to md to fit section
