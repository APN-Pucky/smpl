import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

frames = []


class FigAnimation(animation.FuncAnimation):
    def __init__(self, figs=None, update=None, frames=None, *args, **kwargs):
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
            self, f, _update, frames=len(figs) if update is None else frames, *args, **kwargs)


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
