
import matplotlib.cm as cm
from smpl import doc
from smpl import plot as splot
from matplotlib import colors
import numpy as np
from matplotlib.image import NonUniformImage
import matplotlib.pyplot as plt

default = {
           'xaxis' : [None,"."],
           'yaxis' : [None,"."],
           'zaxis' : [None,"."],
           'logz' : [True,"Colorbar in logarithmic scale."],
           'image' : [True,"Plot via an image."],
           'scatter' : [False,"Plot via scatter."],
           #'zscale' : [None,"Rescale z values."],
           }

# @doc.insert_str("\tDefault kwargs\n\n\t")


@doc.append_str(doc.table(default, init=False))
@doc.append_str(doc.table({"plot2d_kwargs": ["default", "description"]}, bottom=False))
def plot2d_kwargs(kwargs):
    """Set default plot2d_kwargs if not set.

    """
    for k, v in default.items():
        if not k in kwargs:
            kwargs[k] = v[0]
    return kwargs


def plot2d(datax,datay,dataz,image=True,scatter=False):
    """
    Creates a 2D-Plot.
    
    Parameters
    ----------
    **kwargs : optional
        see :func:`plot2d_kwargs`.
    """
    kwargs = plot2d_kwargs(kwargs)
    if(kwargs["image"]):
        map_vplot(datax,datay,dataz,**kwargs)
    elif (kwargs["scatter"]):
        scatter_vplot(datax,datay,dataz,**kwargs)


def map_vplot(tvx,
              tvy,
              tvz,
              xaxis=None,
              yaxis=None,
              zaxis=None,
              logz=True,
              sort=True,
              fill_missing=True,
              zscale=1.):
    vx = np.copy(tvx)
    vy = np.copy(tvy)
    vz = np.copy(tvz)
    if fill_missing:
        for x in vx:
            for y in vy:
                ex = False
                for i in range(len(vx)):
                    if vx[i] == x and vy[i] == y:
                        ex = True
                if not ex:
                    vx = np.append(vx, x)
                    vy = np.append(vy, y)
                    vz = np.append(vz, 0)
    if sort:
        p1 = vx.argsort(kind='stable')
        vx = np.copy(vx[p1])
        vy = np.copy(vy[p1])
        vz = np.copy(vz[p1])
        p2 = vy.argsort(kind='stable')
        vx = vx[p2]
        vy = vy[p2]
        vz = vz[p2]
    s = 1
    while vy[s] == vy[s - 1]:
        s = s + 1
    if s == 1:
        #print("flipped x y ")
        while vx[s] == vx[s - 1]:
            s = s + 1
        if s == 1:
            print("error too small map")
            return
        #x, y = y, x
        xaxis, yaxis = yaxis, xaxis
        vx, vy = vy, vx

    grid = splot.unv(vz).reshape((int(np.rint(np.size(vx) / s)), s)) * zscale

    fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
    im = None
    xl = vx.min() + (vx.min() / 2) - vx[vx != vx.min()].min() / 2
    xm = vx.max() + (vx.max() / 2) - vx[vx != vx.max()].max() / 2
    yl = vy.min() + (vy.min() / 2) - vy[vy != vy.min()].min() / 2
    ym = vy.max() + (vy.max() / 2) - vy[vy != vy.max()].max() / 2
    im = NonUniformImage(
        ax,
        origin="lower",
        cmap='viridis',
        interpolation='nearest',
        extent=(xl, xm, yl, ym),
        norm=colors.LogNorm() if logz else None,
    )

    im.set_data(np.unique(vx), np.unique(vy), grid)
    ax.images.append(im)
    ax.set_xlim(xl, xm)
    ax.set_ylim(yl, ym)

    cb = plt.colorbar(im)
    cb.set_label(zaxis)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)

def scatter_vplot(vx,
                  vy,
                  vz,
                  xaxis=None,
                  yaxis=None,
                  zaxis=None,
                  logz=True,
                  sort=True,
                  fill_missing=True,
                  zscale=1.):
    if sort:
        p1 = vx.argsort(kind='stable')
        vx = np.copy(vx[p1])
        vy = np.copy(vy[p1])
        vz = np.copy(vz[p1])
        p2 = vy.argsort(kind='stable')
        vx = vx[p2]
        vy = vy[p2]
        vz = vz[p2]

    fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
    im = None
    xl = vx.min() + (vx.min() / 2) - vx[vx != vx.min()].min() / 2
    xm = vx.max() + (vx.max() / 2) - vx[vx != vx.max()].max() / 2
    yl = vy.min() + (vy.min() / 2) - vy[vy != vy.min()].min() / 2
    ym = vy.max() + (vy.max() / 2) - vy[vy != vy.max()].max() / 2

    s = plt.scatter(np.concatenate((vx, vx, vx)),
                    np.concatenate((vy, vy, vy)),
                    c=np.concatenate(
                        (splot.unv(vz) + splot.usd(vz),
                         splot.unv(vz) - splot.usd(vz), splot.unv(vz))),
                    s=np.concatenate(
                        ([(3 * plt.rcParams['lines.markersize'])**2
                          for i in range(len(vx))], [
                              (2 * plt.rcParams['lines.markersize'])**2
                              for i in range(len(vx))
                          ], [(plt.rcParams['lines.markersize'])**2
                              for i in range(len(vx))])),
                    norm=colors.LogNorm() if logz else None)

    ax.set_xlim(xl, xm)
    ax.set_ylim(yl, ym)

    cb = plt.colorbar(s)
    cb.set_label(zaxis)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)