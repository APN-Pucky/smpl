import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import ipywidgets
import ipywidgets as widgets
import uuid
import os
import io

frames = []

import itertools

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


#TODO mirror ipywidgets.interactive options
def interactive(func, *args, prerender=True,auto_png=True,rec=0,isls=None,**kwargs):
    # first deiter all of them
    if not rec:
        isls=[]
        for arg in args:
            isl = widgets.SelectionSlider(
                    options=r,
                    value=arg.value,
                    continuous_update=True,
                    description=arg.description,# TODO copy more
                    )
            isls+=[isl]
    if not prerender:
        ipywidgets.interactive(func, *args, **kwargs)
    else:
        arg = args[0]
        outs=[]
        isls=[]
        r = np.arange(arg.min,arg.max,arg.step)
        for a in r:
            tout = widgets.Output(layout={'border': '1px solid black'})
            with tout:
                if len(args)==1:
                    func(a)
                    if auto_png:
                        output = io.BytesIO()
                        plt.savefig(output, format='png')
                        plt.clf()

                        tout = ipywidgets.Image(
                            value=output.getvalue(),
                            format='png',
                        )
                else:
                    tout = interactive(lambda *a,**kw :func(a,*a,**kw),*args[1:],prerender=prerender,auto_png=auto_png,rec=rec+1,isls=isls,**kwargs)
            outs += [tout]


        tab = widgets.Tab(children=outs)
        widgets.jslink((isls[rec],'index'),(tab,'selected_index'))

        if rec:
            return tab
        else:
            out = widgets.Output(layout={'border': '1px solid black'})
            for isl in isls:
                out.append_display_data(isl)
            out.append_display_data(tab)
            return out


#class WigAnimation(widget.Image):


class FigAnimation(animation.FuncAnimation):
    def widget_play(self,):
        # TODO add pre rendereed list of images linked via jslink of values
        play = widgets.Play(
        #     interval=10,
            value=50,
            min=0,
            max=100,
            step=1,
            description="Press play",
            disabled=False
        )
    def widget_gif(self):
        # convert to gif through save as anim.save wants a filename
        uf = str(uuid.uuid4())
        self.save(uf + ".gif")
        with open(uf + ".gif", "rb") as file:
            image = file.read()
        os.remove(uf + ".gif")

        return ipywidgets.Image(
            value=image,
            format='gif',
        )

    def __init__(self, figs=None, frames=None, init=None, update=None,  *args, **kwargs):
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
        plt.axis('off')
        plt.subplots_adjust(top=1, bottom=0, right=1,
                            left=0, hspace=0, wspace=0)
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
            return self.im,

        animation.FuncAnimation.__init__(
            self, f, _update, frames=len(figs) if update is None else frames, init_func=init, *args, **kwargs)


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


