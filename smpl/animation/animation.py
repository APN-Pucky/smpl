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

def interactive(func, *args, prerender=True,**kwargs):
    if not prerender:
        ipywidgets.interactive(func, *args, **kwargs)
    else:
        # TODO generalize for many sliders and kwargs
        arg = args[0]
        imgs=[]
        r = np.arange(arg.min,arg.max,arg.step)
        for a in r:
            func(a)
            output = io.BytesIO()
            plt.savefig(output, format='png')
            plt.clf()

            imgs += [ipywidgets.Image(
                value=output.getvalue(),
                format='png',
            )]
        
        out = widgets.Output(layout={'border': '1px solid black'})
        isl = widgets.SelectionSlider(
                options=r,
                value=arg.value,
                continuous_update=True,
                description=arg.description,# TODO copy more
                )
        tab = widgets.Tab(children=imgs)
        widgets.jslink((isl,'index'),(tab,'selected_index'))
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
        #convert to gif through save
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


