import matplotlib as mpl
import matplotlib.pyplot as plt
import os


def use(styles):
    """Extends matplotlib.use to include .mplstyle files included in this package.

    Looks for styles in this package and if they cannot be found, will look for
    standard definitions in the matplotlib directories. Since packaging styles
    is currently a 'wishlist' item for matplotlib devs
    (see https://github.com/matplotlib/matplotlib/issues/4781),
    this must be done with a wrapper function.

    Parameters
    ----------
    styles : {str | list}
        A string or list of styles, either found in this package or in the
        standard matplotlib directories. This works similarly to matplotlib.use
        so that rightward styles overwrite conflicting elements of previous
        styles.
    """
    if not isinstance(styles, list):
        styles = [styles]
    path = os.path.dirname(__file__)  # Path of this file
    for style in styles:
        try:
            fname = os.path.join(path, 'stylelib', style + '.mplstyle')
            rc = mpl.rc_params_from_file(fname, use_default_template=False)
            mpl.rcParams.update(rc)
        except FileNotFoundError:
            mpl.style.use(style)


def set_size(fig=None, w='narrow', aspect=None, h=None, tight=True):
    """Sets the size of a figure to be used in Physical Review publications.

    Figures should be sized as close to how they will be shown in a publication
    to prevent stretching or squishing of plot elements, e.g., text size. This
    function correctly sizes single- and two-column figures and provides an
    additional medium size that is meant to be centered with padding on both
    sides. Measurements taken from the Physical Review Style and Notation Guide
    http://home.fnal.gov/~bellanto/work/MINERvA/Phys%20Review%20Style%20Guide.pdf
    This function should be called after all plot customizations have finished.

    Parameters
    ----------
    fig : {matplotlib figure}, optional
        The figure to be resized, by default takes the current
    w : {str}, optional
        The width for use in publication. Must be 'narrow' (single column),
        'medium' (intermediate sized), or wide (two column)
    aspect : {float}, optional
        The aspect ratio of the display coordinates: height = aspect * width.
        The default is chosen based on the value of w: narrow -> 1, else 1/2.
        Aspect is ignored if h is provided.
    h : {float}, optional
        The height of the figure in inches.
    tight : {True | False | dict | None}, optional
        The argument passed to fig.set_tight_layout. From matplotlib docs:
        "Set whether tight_layout() is used upon drawing. If None, the
        rcParams[‘figure.autolayout’] value will be set. When providing a dict
        containing the keys pad, w_pad, h_pad and rect, the default
        tight_layout() paddings will be overridden."

    Raises
    ------
    ValueError
        If w is not one of 'narrow', 'medium', or 'wide'
    """
    if fig is None:
        fig = plt.gcf()
    if w not in ['narrow', 'medium', 'wide']:
        raise ValueError('w must be "narrow", "medium", or "wide"')

    widths_inches = {'narrow': 3.4, 'medium': 5.5, 'wide': 7.0}
    aspect_dict = {'narrow': 1, 'medium': 1/2, 'wide': 1/2}

    width = widths_inches[w]
    if aspect is None:
        aspect = aspect_dict[w]
    height = aspect * width
    if h is not None:
        height = h

    fig.set_size_inches(width, height)
    fig.set_tight_layout(tight)
