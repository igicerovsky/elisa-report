from .constants import CV_DIGITS


def plate_section_ex(df, plate):
    # df is formatted!
    md = f'### Plate {plate}\n\n'

    md += df.to_markdown(floatfmt="#.{}f".format(CV_DIGITS))
    md += '\n\n'
    md += '\* sample will be retested\n\n'

    return md


def assembly(reports, protocol):
    md =  f'# GT Analytics - Capsid {protocol}\n\nSOP-051200\n\n'

    md += '## Objective\n\n'
    md += '???-capsid concentration is determined in unknown samples.  \n\n'

    md += '## Method Status\n\n'
    md += 'For detailed Method status see either SOP-051200 and/or method History File RPT-000047.  \n\n'

    md += '## Results - Current Reference\n\n'

    for r in reports:
        md += plate_section_ex(r['df'], r['plate'])

    md += '## Evaluation criteria\n\n'
    md += 'Validity of the assay: Intermediary control sample limits (3s) are: 1,888 - 2,703E+12cp/ml  \n\n'

    md += '## Comments\n\n'
    md += 'Add comment here...\n'

    return md