import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from smpl import io
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

frames = []


class FigAnimation(animation.FuncAnimation):
    def __init__(self, figs, *args, **kwargs):
        # Use the list of figures as the framedata, which will be iterated
        # over by the machinery.
        self._figs = figs
        f = plt.figure()
        plt.axis('off')

        canvas = FigureCanvasAgg(figs[0])
        canvas.draw()
        rgba = np.asarray(canvas.buffer_rgba())
        im = Image.fromarray(rgba)
        self.im = plt.imshow(im)

        def update(frame):
            canvas = FigureCanvasAgg(figs[frame])
            canvas.draw()
            rgba = np.asarray(canvas.buffer_rgba())
            im = Image.fromarray(rgba)
            self.im.set_array(mpl.image.pil_to_array(im))
            return self.im,

        animation.FuncAnimation.__init__(
            self, f, update, frames=len(figs), *args, **kwargs)


class FigureAnimation(animation.TimedAnimation):
    """
    Animation using a fixed set of `Figure` objects.

    Before creating an instance, all plotting should have taken place
    and the relevant figures saved.

    Parameters
    ----------
    fig : `~matplotlib.figure.Figure`
        The figure object used to get needed events, such as draw or resize.
    artists : list
        Each list entry is a collection of artists that are made visible on
        the corresponding frame.  Other artists are made invisible.
    interval : int, default: 200
        Delay between frames in milliseconds.
    repeat_delay : int, default: 0
        The delay in milliseconds between consecutive animation runs, if
        *repeat* is True.
    repeat : bool, default: True
        Whether the animation repeats when the sequence of frames is completed.
    """

    def __init__(self, figs, *args, **kwargs):
        # Use the list of figures as the framedata, which will be iterated
        # over by the machinery.
        self._framedata = figs
        animation.TimedAnimation.__init__(
            self, figs[0], *args, blit=False, **kwargs)

    def _draw_frame(self, fig):
        #self._fig.lines = fig.lines
        self._fig.imshow

        #self._fig._axes = fig._axes
        self._fig_n = fig
        #print("pl " + str(fig.number))
        # plt.figure(fig.number)

    def save(self, filename, writer=None, fps=None, dpi=None, codec=None,
             bitrate=None, extra_args=None, metadata=None, extra_anim=None,
             savefig_kwargs=None, *, progress_callback=None):
        # We use same code as original Animation, but inject the figures into the writer per frame
        if writer is None:
            writer = mpl.rcParams['animation.writer']
        elif (not isinstance(writer, str) and
              any(arg is not None
                  for arg in (fps, codec, bitrate, extra_args, metadata))):
            raise RuntimeError('Passing in values for arguments '
                               'fps, codec, bitrate, extra_args, or metadata '
                               'is not supported when writer is an existing '
                               'MovieWriter instance. These should instead be '
                               'passed as arguments when creating the '
                               'MovieWriter instance.')

        if savefig_kwargs is None:
            savefig_kwargs = {}

        if fps is None and hasattr(self, '_interval'):
            # Convert interval in ms to frames per second
            fps = 1000. / self._interval

        # Re-use the savefig DPI for ours if none is given
        if dpi is None:
            dpi = mpl.rcParams['savefig.dpi']
        if dpi == 'figure':
            dpi = self._fig.dpi

        writer_kwargs = {}
        if codec is not None:
            writer_kwargs['codec'] = codec
        if bitrate is not None:
            writer_kwargs['bitrate'] = bitrate
        if extra_args is not None:
            writer_kwargs['extra_args'] = extra_args
        if metadata is not None:
            writer_kwargs['metadata'] = metadata

        all_anim = [self]
        if extra_anim is not None:
            all_anim.extend(anim
                            for anim
                            in extra_anim if anim._fig is self._fig)

        # If we have the name of a writer, instantiate an instance of the
        # registered class.
        if isinstance(writer, str):
            try:
                writer_cls = animation.writers[writer]
            except RuntimeError:  # Raised if not available.
                writer_cls = PillowWriter  # Always available.
                animation._log.warning("MovieWriter %s unavailable; using Pillow "
                                       "instead.", writer)
            writer = writer_cls(fps, **writer_kwargs)
        animation._log.info('Animation.save using %s', type(writer))

        gfo = writer.grab_frame

        def gf(**kwargs):
            gfo(**kwargs)
            writer.fig = self._fig_n
            #print("fixed fig")
        writer.grab_frame = gf
        animation.TimedAnimation.save(self, filename, writer=writer,  extra_anim=extra_anim,
                                      savefig_kwargs=savefig_kwargs,  progress_callback=progress_callback)


def frame():
    """
    Saves current Matplotlib Graphic.
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
    Empties strored frames.
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
