from .constants import CV_DIGITS
from .config import config as cfg
from .config import LIMITS_NAME, SOP_NAME, MHF_NAME


def plate_section_ex(df, plate):
    # df is formatted!
    md = f'### Plate {plate}\n\n'

    md += df.to_markdown(floatfmt="#.{}f".format(CV_DIGITS))
    md += '\n\n'
    md += '\* sample will be retested\n\n'

    return md


def assembly(reports, protocol, **kwargs):
    sop = cfg[SOP_NAME]
    md = f'# GT Analytics - Capsid {protocol}\n\n{sop}\n\n'

    md += '## Objective\n\n'
    md += 'Capsid concentration is determined for unknown samples.  \n\n'

    md += '## Method Status\n\n'
    mhf = cfg[MHF_NAME]
    md += f'For detailed method status see either {sop} and/or method history file {mhf}.  \n\n'

    md += '## Results - Current Reference\n\n'

    for r in reports:
        md += plate_section_ex(r['df'], r['plate'])

    md += '## Evaluation criteria\n\n'
    limits = cfg[LIMITS_NAME]
    md += 'Validity of the assay: Intermediary control sample limits (3s) are: {:.3e} - {:.3e} cp/ml  \n\n'.format(
        limits[0], limits[1])

    if kwargs and kwargs['comment']:
        md += '## Comments\n\n'
        md += 'Add comment here...\n'

    return md
