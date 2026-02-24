"""
colors.py — Fluorescent protein color mappings for Opentrons Bio-Art visualization
===================================================================================
Maps fluorescent protein names to matplotlib-compatible colors for Petri dish rendering.
"""

# ═══════════════════════════════════════════════════════════════════════
# Petri dish constants
# ═══════════════════════════════════════════════════════════════════════

PETRI_INNER_DIAMETER: float = 84  # mm — inner diameter of "90mm" and "100mm" plates
MAX_DRAW_RADIUS: float = PETRI_INNER_DIAMETER / 2 - 2  # 2mm margin for tip size, drops, calibration

# ═══════════════════════════════════════════════════════════════════════
# Protein → visual color mapping
# ═══════════════════════════════════════════════════════════════════════

PROTEIN_VISUAL_COLORS: dict[str, str] = {
    # Reds / Pinks
    'mrfp1':            'red',
    'mcherry':          'firebrick',
    'dsred':            'darkred',
    'mruby2':           'crimson',
    'mscarlet_i':       'tomato',
    'mkate2':           'deeppink',
    'mkate2_tf':        'mediumvioletred',
    'tagrfp':           'coral',
    'tdtomato':         'orangered',
    'eqfp578':          'salmon',
    'mlychee_tf':       'hotpink',
    'mwatermelon':      'lightcoral',
    # Oranges / Yellows
    'mko2':             'orange',
    'mpapaya':          'lightsalmon',
    'venus':            'yellow',
    'mcitrine':         'gold',
    'mvenus':           'goldenrod',
    'mbanana':          'khaki',
    'mstaygold2':       'gold',
    'mchartreuse_tf':   'chartreuse',
    # Greens
    'sfgfp':            'lime',
    'egfp':             'lime',
    'megfp':            'limegreen',
    'avgfp':            'palegreen',
    'mneongreen':       'greenyellow',
    'mazamigreen':      'forestgreen',
    'mclover3':         'green',
    'mwasabi':          'lightgreen',
    'mjuniper':         'darkgreen',
    'zsgreen1':         'springgreen',
    'pa_gfp':           'mediumseagreen',
    'mhoneydew':        'yellowgreen',
    # Blues / Cyans
    'azurite':          'royalblue',
    'tagbfp':           'blue',
    'mtagbfp2':         'mediumblue',
    'ultramarine':      'navy',
    'mturquoise2':      'turquoise',
    'mcerulean3':       'cyan',
    'mtfp1':            'darkcyan',
    'mmicy':            'aquamarine',
    'electra2':         'deepskyblue',
    # Others
    'mplum':            'purple',
}


def resolve_visual_color(protein_or_color_name: str) -> str:
    """Resolve a fluorescent protein name or color name to a matplotlib color.

    Lookup order:
      1. Check PROTEIN_VISUAL_COLORS (case-insensitive)
      2. Map 'green' → 'lime' for better visibility on dark backgrounds
      3. Pass through as-is (assumed to be a valid matplotlib color)

    Args:
        protein_or_color_name: Protein name (e.g. 'sfGFP') or color (e.g. 'red').

    Returns:
        A matplotlib-compatible color string.
    """
    key = protein_or_color_name.lower().strip()
    if key in PROTEIN_VISUAL_COLORS:
        return PROTEIN_VISUAL_COLORS[key]
    if key == 'green':
        return 'lime'
    return protein_or_color_name
