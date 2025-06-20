import matplotlib.pyplot as plt
import numpy as np
import smplr
from matplotlib import colors
from matplotlib.image import NonUniformImage

from smpl import doc, util
from smpl import plot as splot

default = {
    "title": [None, "Plot title"],
    "xlabel": [None, "."],
    "ylabel": [None, "."],
    "zlabel": [None, "."],
    "logz": [True, "Colorbar in logarithmic scale."],
    "style": [
        "pcolormesh",
        "Plot via an image ('image') or scatter ('scatter') or mesh ('pcolormesh').",
    ],
    "interpolation": [
        "nearest",
        "Only 'nearest' or 'bilinear' for nonuniformimage. Check https://matplotlib.org/stable/gallery/images_contours_and_fields/interpolation_methods.html#interpolations-for-imshow",
    ],
    "cmap": [
        "viridis",
        "Good default color map for missing datapoints since it does not include white.",
    ],
    # 'zscale' : [None,"Rescale z values."],
}

# @doc.insert_str("\tDefault kwargs\n\n\t")


@doc.append_str(doc.array_table(default, init=False))
@doc.append_str(
    doc.array_table({"plot2d_kwargs": ["default", "description"]}, bottom=False)
)
def plot2d_kwargs(kwargs):
    """Set default plot2d_kwargs if not set."""
    for k, v in default.items():
        if k not in kwargs:
            kwargs[k] = v[0]
    return kwargs


def plot2d(datax, datay, dataz, **kwargs):
    """
    Creates a 2D-Plot.

    Parameters
    ----------
    **kwargs : optional
        see :func:`plot2d_kwargs`.
    """
    kwargs = plot2d_kwargs(kwargs)
    if "xaxis" in kwargs and ("xlabel" not in kwargs or not kwargs["xlabel"]):
        # warnings.warn("xaxis is deprecated. Use xlabel instead.", DeprecationWarning, 2)
        kwargs["xlabel"] = kwargs["xaxis"]
    if "yaxis" in kwargs and ("ylabel" not in kwargs or not kwargs["ylabel"]):
        # warnings.warn("yaxis is deprecated. Use ylabel instead.", DeprecationWarning, 2)
        kwargs["ylabel"] = kwargs["yaxis"]
    if "zaxis" in kwargs and ("zlabel" not in kwargs or not kwargs["zlabel"]):
        # warnings.warn("zaxis is deprecated. Use zlabel instead.", DeprecationWarning, 2)
        kwargs["zlabel"] = kwargs["zaxis"]

    if util.has("axes", kwargs) and kwargs["axes"] is not None:
        plt.sca(kwargs["axes"])
    if kwargs["style"] == "pcolormesh":
        pcolormesh_vplot(datax, datay, dataz, **kwargs)
    elif kwargs["style"] == "image":
        map_vplot(datax, datay, dataz, **kwargs)
    elif kwargs["style"] == "scatter":
        scatter_vplot(datax, datay, dataz, **kwargs)


def sort_xyz(x, y, z):
    p1 = x.argsort(kind="stable")
    x = np.copy(x[p1])
    y = np.copy(y[p1])
    z = np.copy(z[p1])
    p2 = y.argsort(kind="stable")
    x = x[p2]
    y = y[p2]
    z = z[p2]
    return x, y, z


def pcolormesh_vplot(
    tvx,
    tvy,
    tvz,
    xlabel=None,
    ylabel=None,
    zlabel=None,
    logz=True,
    zscale=1.0,
    **kwargs,
):
    """
    Advantage over matplotlibs pcolor(mesh) is that does not require a meshgrid. Instead it uses the data points directly in three lists.
    """
    vx = np.copy(tvx)
    vy = np.copy(tvy)
    vz = np.copy(tvz)
    assert vx.shape == vy.shape == vz.shape

    if len(vz.shape) < 2:
        mesh = np.meshgrid(np.unique(vx), np.unique(vy))
        X, Y = mesh
        # set Z to values of vz on the meshgrid
        Z = np.empty(mesh[0].shape)
        Z[:] = np.nan
        for i, _ in enumerate(vx):
            Z[(mesh[0] == vx[i]) & (mesh[1] == vy[i])] = splot.unv(vz[i])
        Z[:] *= zscale
    else:
        X = vx
        Y = vy
        Z = vz * zscale

    plt.pcolormesh(
        X, Y, Z, norm=colors.LogNorm() if logz else None, cmap=kwargs["cmap"]
    )

    # ax.set_xlim(xl, xm)
    # ax.set_ylim(yl, ym)

    cb = plt.colorbar()
    cb.set_label(zlabel)
    smplr.style_plot2d(xlabel=xlabel, ylabel=ylabel, **kwargs)


def map_vplot(
    tvx,
    tvy,
    tvz,
    xlabel=None,
    ylabel=None,
    zlabel=None,
    logz=True,
    sort=True,
    fill_missing=True,
    zscale=1.0,
    **kwargs,
):
    """ """
    vx = np.copy(tvx)
    vy = np.copy(tvy)
    vz = np.copy(tvz)
    if fill_missing:
        # TODO speed up
        for x in vx:
            for y in vy:
                ex = np.any(np.logical_and((vx == x), (vy == y)))
                if not ex:
                    vx = np.append(vx, x)
                    vy = np.append(vy, y)
                    vz = np.append(vz, 0)
    if sort:
        vx, vy, vz = sort_xyz(vx, vy, vz)

    s = 1
    while vy[s] == vy[s - 1]:
        s = s + 1
    if s == 1:
        # print("flipped x y ")
        while vx[s] == vx[s - 1]:
            s = s + 1
        if s == 1:
            print("error too small map")
            return
        # x, y = y, x
        xlabel, ylabel = ylabel, xlabel
        vx, vy = vy, vx

    grid = splot.unv(vz).reshape((int(np.rint(np.size(vx) / s)), s)) * zscale

    _, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
    im = None
    xl = vx.min() + (vx.min() / 2) - vx[vx != vx.min()].min() / 2
    xm = vx.max() + (vx.max() / 2) - vx[vx != vx.max()].max() / 2
    yl = vy.min() + (vy.min() / 2) - vy[vy != vy.min()].min() / 2
    ym = vy.max() + (vy.max() / 2) - vy[vy != vy.max()].max() / 2
    im = NonUniformImage(
        ax,
        origin="lower",
        cmap=kwargs["cmap"],
        interpolation=kwargs["interpolation"],
        extent=(xl, xm, yl, ym),
        norm=colors.LogNorm() if logz else None,
    )

    im.set_data(np.unique(vx), np.unique(vy), grid)
    ax.add_image(im)
    # ax.images.append(im)
    ax.set_xlim(xl, xm)
    ax.set_ylim(yl, ym)

    cb = plt.colorbar(im)
    cb.set_label(zlabel)
    smplr.style_plot2d(xlabel=xlabel, ylabel=ylabel, **kwargs)


def scatter_vplot(
    vx,
    vy,
    vz,
    xlabel=None,
    ylabel=None,
    zlabel=None,
    logz=True,
    sort=True,
    **kwargs,
):
    if sort:
        vx, vy, vz = sort_xyz(vx, vy, vz)

    _, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
    xl = vx.min() + (vx.min() / 2) - vx[vx != vx.min()].min() / 2
    xm = vx.max() + (vx.max() / 2) - vx[vx != vx.max()].max() / 2
    yl = vy.min() + (vy.min() / 2) - vy[vy != vy.min()].min() / 2
    ym = vy.max() + (vy.max() / 2) - vy[vy != vy.max()].max() / 2

    s = plt.scatter(
        np.concatenate((vx, vx, vx)),
        np.concatenate((vy, vy, vy)),
        c=np.concatenate(
            (
                splot.unv(vz) + splot.usd(vz),
                splot.unv(vz) - splot.usd(vz),
                splot.unv(vz),
            )
        ),
        s=np.concatenate(
            (
                [(3 * plt.rcParams["lines.markersize"]) ** 2 for i in range(len(vx))],
                [(2 * plt.rcParams["lines.markersize"]) ** 2 for i in range(len(vx))],
                [(plt.rcParams["lines.markersize"]) ** 2 for i in range(len(vx))],
            )
        ),
        norm=colors.LogNorm() if logz else None,
        cmap=kwargs["cmap"],
    )

    ax.set_xlim(xl, xm)
    ax.set_ylim(yl, ym)

    cb = plt.colorbar(s)
    cb.set_label(zlabel)
    smplr.style_plot2d(xlabel=xlabel, ylabel=ylabel, **kwargs)
