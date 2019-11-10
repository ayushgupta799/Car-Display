
from tkcolorpicker.functions import tk, round2, rgb_to_hexa, hue2col


class GradientBar(tk.Canvas):
    """HSV gradient colorbar with selection cursor."""

    def __init__(self, parent, hue=0, height=11, width=256, variable=None,
                 **kwargs):
        """
        Create a GradientBar.
        Keyword arguments:
            * parent: parent window
            * hue: initially selected hue value
            * variable: IntVar linked to the alpha value
            * height, width, and any keyword argument accepted by a tkinter Canvas
        """
        tk.Canvas.__init__(self, parent, width=width, height=height, **kwargs)

        self._variable = variable
        if variable is not None:
            try:
                hue = int(variable.get())
            except Exception:
                pass
        else:
            self._variable = tk.IntVar(self)
        if hue > 360:
            hue = 360
        elif hue < 0:
            hue = 0
        self._variable.set(hue)
        try:
            self._variable.trace_add("write", self._update_hue)
        except Exception:
            self._variable.trace("w", self._update_hue)

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        self.bind('<Configure>', lambda e: self._draw_gradient(hue))
        self.bind('<ButtonPress-1>', self._on_click)
        self.bind('<B1-Motion>', self._on_move)

    def _draw_gradient(self, hue):
        """Draw the gradient and put the cursor on hue."""
        self.delete("gradient")
        self.delete("cursor")
        del self.gradient
        width = self.winfo_width()
        height = self.winfo_height()

        self.gradient = tk.PhotoImage(master=self, width=width, height=height)

        line = []
        for i in range(width):
            line.append(rgb_to_hexa(*hue2col(float(i) / width * 360)))
        line = "{" + " ".join(line) + "}"
        self.gradient.put(" ".join([line for j in range(height)]))
        self.create_image(0, 0, anchor="nw", tags="gradient",
                          image=self.gradient)
        self.lower("gradient")

        x = hue / 360. * width
        self.create_line(x, 0, x, height, width=2, tags='cursor')

    def _on_click(self, event):
        """Move selection cursor on click."""
        x = event.x
        self.coords('cursor', x, 0, x, self.winfo_height())
        self._variable.set(round2((360. * x) / self.winfo_width()))

    def _on_move(self, event):
        """Make selection cursor follow the cursor."""
        w = self.winfo_width()
        x = min(max(event.x, 0), w)
        self.coords('cursor', x, 0, x, self.winfo_height())
        self._variable.set(round2((360. * x) / w))

    def _update_hue(self, *args):
        hue = int(self._variable.get())
        if hue > 360:
            hue = 360
        elif hue < 0:
            hue = 0
        self.set(hue)
        self.event_generate("<<HueChanged>>")

    def get(self):
        """Return hue of color under cursor."""
        coords = self.coords('cursor')
        return round2(360 * coords[0] / self.winfo_width())

    def set(self, hue):
        """Set cursor position on the color corresponding to the hue value."""
        x = hue / 360. * self.winfo_width()
        self.coords('cursor', x, 0, x, self.winfo_height())
        self._variable.set(hue)