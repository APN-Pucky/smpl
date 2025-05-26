"""Simplified Animations."""
import io
import os
import uuid

import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image

import ipywidgets as widgets
import itertools

from smpl import doc

frames = []

@doc.deprecated("1.0.5","Will be removed from main smpl")
def dict_product(dicts):
    """
    >>> d = {"number": [1,2], "color": ['a','b'] }
    >>> list(dict_product(d))
    [{'number': 1, 'color': 'a'}, {'number': 1, 'color': 'b'}, {'number': 2, 'color': 'a'}, {'number': 2, 'color': 'b'}]
    """
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))


def list_product(lists):
    """
    >>> l = [[1,2],[3,4]]
    >>> list(list_product(l))
    [(1, 3), (1, 4), (2, 3), (2, 4)]
    """
    return itertools.product(*lists)


# TODO mirror ipywidgets.interactive options
def interactive(
    func, *args, prerender=True, auto_png=True, rec=0, isls=None, plays=None, **kwargs
):

    if plays is None:
        plays = []
    if isls is None:
        isls = []
    if rec == 0:
        isls = []
        for arg in [*args, *kwargs.values()]:
            r = np.arange(arg.min, arg.max + arg.step, arg.step)
            if isinstance(arg, widgets.Play):
                isl = widgets.IntSlider()
                widgets.jslink((arg, "value"), (isl, "value"))
                plays += [arg]
            else:
                isl = widgets.SelectionSlider(
                    options=r,
                    value=arg.value,
                    continuous_update=True,
                    description=arg.description,  # TODO copy more
                )
                plays += [None]
            isls += [isl]
    if not prerender:
        widgets.interactive(func, *args, **kwargs)
    else:
        key = None
        arg = None
        if len(kwargs) == 0:
            arg = args[0]
        if len(args) == 0:
            key, arg = list(kwargs.items())[0]
        outs = []
        r = np.arange(arg.min, arg.max + arg.step, arg.step)
        for a in r:
            tout = widgets.Output(layout={"border": "0px solid black"})
            with tout:
                if (len(args) == 1 and len(kwargs) == 0) or (
                    len(args) == 0 and len(kwargs) == 1
                ):
                    if key is None:
                        func(a)
                    else:
                        func(**{key: a})
                    if auto_png:
                        output = io.BytesIO()
                        plt.savefig(output, format="png")
                        plt.close()
                        # plt.clf()

                        tout = widgets.Image(
                            value=output.getvalue(),
                            format="png",
                        )
                else:
                    if len(args) != 0:
                        tout = interactive(
                            lambda *ar, **kw: func(a, *ar, **kw),
                            *args[1:],
                            prerender=prerender,
                            auto_png=auto_png,
                            rec=rec + 1,
                            plays=plays,
                            isls=isls,
                            **kwargs
                        )
                    else:
                        dkw = dict(kwargs).pop(key)
                        tout = interactive(
                            lambda *ar, **kw: func(*ar, **{key: a}, **kw),
                            prerender=prerender,
                            auto_png=auto_png,
                            rec=rec + 1,
                            plays=plays,
                            isls=isls,
                            **dkw
                        )
            outs += [tout]

        tab = widgets.Tab(children=outs)
        if hasattr(isls[rec], "index"):
            widgets.jslink((isls[rec], "index"), (tab, "selected_index"))
        elif hasattr(isls[rec], "value"):
            widgets.jslink((isls[rec], "value"), (tab, "selected_index"))
        else:
            print("no link")

        if rec:
            return tab
        else:
            out = widgets.Output(layout={"border": "0px solid black"})
            for i, isl in enumerate(isls):
                if plays[i] is not None:
                    out.append_display_data(widgets.HBox([plays[i], isl]))
                else:
                    out.append_display_data(isl)
            out.append_display_data(tab)
            plt.close()
            return out


# class WigAnimation(widget.Image):


class FigAnimation(animation.FuncAnimation):
    def widget_gif(self):

        # convert to gif through save as anim.save wants a filename
        uf = str(uuid.uuid4())
        self.save(uf + ".gif")
        with open(uf + ".gif", "rb") as file:
            image = file.read()
        os.remove(uf + ".gif")

        return widgets.Image(
            value=image,
            format="gif",
        )

    def __init__(self, figs=None, frames=None, init=None, update=None, *args, **kwargs):
        # Use the list of figures as the framedata, which will be iterated
        # over by the machinery.
        if update is None:
            f1 = figs[0]
        else:
            update(frames[0])
            f1 = plt.gcf()
            plt.clf()
            plt.close()

        self._figs = figs
        f = plt.figure()
        plt.axis("off")
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)

        canvas = FigureCanvasAgg(f1)
        canvas.draw()
        rgba = np.asarray(canvas.buffer_rgba())
        im = Image.fromarray(rgba)
        self.im = plt.imshow(im)

        def _update(frame):
            ff = None
            if update is not None:
                update(frame)
                ff = plt.gcf()
            else:
                ff = figs[frame]
            canvas = FigureCanvasAgg(ff)
            canvas.draw()
            rgba = np.asarray(canvas.buffer_rgba())
            im = Image.fromarray(rgba)
            self.im.set_array(mpl.image.pil_to_array(im))
            return (self.im,)

        animation.FuncAnimation.__init__(
            self,
            f,
            _update,
            frames=len(figs) if update is None else frames,
            init_func=init,
            *args,
            **kwargs
        )


def frame():
    """
    Saves current Matplotlib figure.
    """
    global frames
    # f = plt.gcf()
    # f.figure = f
    # diold = f.canvas.draw_idle
    # f.set_visible = lambda b: vis(f, b)
    # f.canvas.draw_idle = lambda _=None: io.pr(
    #    diold()) if len(frames) == 0 else None

    frames.append(plt.gcf())
    # plt.savefig("test"+str(len(frames))+".jpg")
    plt.close()


def clear():
    """
    Empties stored frames.
    """
    global frames
    frames = []


def animate(**kwargs):
    """
    Make frames to Animation

    Parameters
    ==========

    They are passed directly to ArtistAnimation.

    Returns
    =======
    ArtistAnimation

    """
    global frames
    ani = FigAnimation(frames, **kwargs)
    # clear()
    return ani
