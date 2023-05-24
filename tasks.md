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


## TODO

