:py:mod:`smpl.animation.animation`
==================================

.. py:module:: smpl.animation.animation


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   smpl.animation.animation.FigAnimation



Functions
~~~~~~~~~

.. autoapisummary::

   smpl.animation.animation.dict_product
   smpl.animation.animation.list_product
   smpl.animation.animation.interactive
   smpl.animation.animation.frame
   smpl.animation.animation.clear
   smpl.animation.animation.animate



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.animation.animation.frames


.. py:data:: frames
   :annotation: = []

   

.. py:function:: dict_product(dicts)

   >>> d = {"number": [1,2], "color": ['a','b'] }
   >>> list(dict_product(d))
   [{'number': 1, 'color': 'a'}, {'number': 1, 'color': 'b'}, {'number': 2, 'color': 'a'}, {'number': 2, 'color': 'b'}]


.. py:function:: list_product(lists)

   >>> l = [[1,2],[3,4]]
   >>> list(list_product(l))
   [(1, 3), (1, 4), (2, 3), (2, 4)]


.. py:function:: interactive(func, *args, prerender=True, auto_png=True, rec=0, isls=None, plays=None, **kwargs)


.. py:class:: FigAnimation(figs=None, frames=None, init=None, update=None, *args, **kwargs)

   Bases: :py:obj:`matplotlib.animation.FuncAnimation`

   `TimedAnimation` subclass that makes an animation by repeatedly calling
   a function *func*.

   .. note::

       You must store the created Animation in a variable that lives as long
       as the animation should run. Otherwise, the Animation object will be
       garbage-collected and the animation stops.

   Parameters
   ----------
   fig : `~matplotlib.figure.Figure`
       The figure object used to get needed events, such as draw or resize.

   func : callable
       The function to call at each frame.  The first argument will
       be the next value in *frames*.   Any additional positional
       arguments can be supplied using `functools.partial` or via the *fargs*
       parameter.

       The required signature is::

           def func(frame, *fargs) -> iterable_of_artists

       It is often more convenient to provide the arguments using
       `functools.partial`. In this way it is also possible to pass keyword
       arguments. To pass a function with both positional and keyword
       arguments, set all arguments as keyword arguments, just leaving the
       *frame* argument unset::

           def func(frame, art, *, y=None):
               ...

           ani = FuncAnimation(fig, partial(func, art=ln, y='foo'))

       If ``blit == True``, *func* must return an iterable of all artists
       that were modified or created. This information is used by the blitting
       algorithm to determine which parts of the figure have to be updated.
       The return value is unused if ``blit == False`` and may be omitted in
       that case.

   frames : iterable, int, generator function, or None, optional
       Source of data to pass *func* and each frame of the animation

       - If an iterable, then simply use the values provided.  If the
         iterable has a length, it will override the *save_count* kwarg.

       - If an integer, then equivalent to passing ``range(frames)``

       - If a generator function, then must have the signature::

            def gen_function() -> obj

       - If *None*, then equivalent to passing ``itertools.count``.

       In all of these cases, the values in *frames* is simply passed through
       to the user-supplied *func* and thus can be of any type.

   init_func : callable, optional
       A function used to draw a clear frame. If not given, the results of
       drawing from the first item in the frames sequence will be used. This
       function will be called once before the first frame.

       The required signature is::

           def init_func() -> iterable_of_artists

       If ``blit == True``, *init_func* must return an iterable of artists
       to be re-drawn. This information is used by the blitting algorithm to
       determine which parts of the figure have to be updated.  The return
       value is unused if ``blit == False`` and may be omitted in that case.

   fargs : tuple or None, optional
       Additional arguments to pass to each call to *func*. Note: the use of
       `functools.partial` is preferred over *fargs*. See *func* for details.

   save_count : int, default: 100
       Fallback for the number of values from *frames* to cache. This is
       only used if the number of frames cannot be inferred from *frames*,
       i.e. when it's an iterator without length or a generator.

   interval : int, default: 200
       Delay between frames in milliseconds.

   repeat_delay : int, default: 0
       The delay in milliseconds between consecutive animation runs, if
       *repeat* is True.

   repeat : bool, default: True
       Whether the animation repeats when the sequence of frames is completed.

   blit : bool, default: False
       Whether blitting is used to optimize drawing.  Note: when using
       blitting, any animated artists will be drawn according to their zorder;
       however, they will be drawn on top of any previous artists, regardless
       of their zorder.

   cache_frame_data : bool, default: True
       Whether frame data is cached.  Disabling cache might be helpful when
       frames contain large objects.

   .. py:method:: widget_gif()



.. py:function:: frame()

   Saves current Matplotlib figure.


.. py:function:: clear()

   Empties stored frames.


.. py:function:: animate(**kwargs)

   Make frames to Animation

   Parameters
   ==========

   They are passed directly to ArtistAnimation.

   Returns
   =======
   ArtistAnimation
