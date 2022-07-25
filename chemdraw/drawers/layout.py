import numpy as np
import plotly.graph_objs as go

from chemdraw import Molecule


class ConfigLayout:
    def __init__(self, parent):
        self.parent = parent

        self.background_color = 'rgba(255,255,255,1)'
        self.margin = dict(l=0, r=0, b=0, t=0, pad=0)
        self.show_axis = False
        self.fix_zoom = True  # remove controls to do zoom (zoom doesn't change line width and text size)
        self.dragmode = "pan"

        self.fixed_domain = True  # assumed to be square
        self.fixed_range = False
        self.width = 600
        self.height = 600
        self.range_offset = 1
        self.range_x = None
        self.range_y = None
        self._clear_x_ranges = False
        self._clear_y_ranges = False

        self.scaling = 1

    def get_scaling(self, molecule: Molecule):
        if self.range_x is None or self.range_y is None:
            min_ = np.min(molecule.atom_coordinates, axis=0)
            max_ = np.max(molecule.atom_coordinates, axis=0)

            threshold = 5 - self.range_offset
            if self.range_x is None:
                self._clear_x_ranges = True
                if max_[0] > threshold or np.abs(min_[0]) > threshold:
                    self.range_x = np.array((min_[0] - self.range_offset, max_[0] + self.range_offset))
                else:
                    self.range_x = np.array([-5, 5], dtype="float64")
            if self.range_y is None:
                self._clear_y_ranges = True
                if max_[1] > threshold or np.abs(min_[1]) > threshold:
                    self.range_y = np.array((min_[1] - self.range_offset, max_[1] + self.range_offset))
                else:
                    self.range_y = np.array([-5, 5], dtype="float64")

            self.scaling = np.max((self.range_x.ptp(), self.range_y.ptp())) / 10

    def apply_layout(self, fig: go.Figure) -> go.Figure:
        kwargs = {
            "showlegend": False,
            "hovermode": False,
            "plot_bgcolor": self.background_color,
            "paper_bgcolor": self.background_color,
            "dragmode": self.dragmode,
            "margin": self.margin,
        }

        xaxes_kwargs = {
            "visible": self.show_axis,
            "fixedrange": self.fix_zoom,
            "layer": "below traces",
        }

        yaxes_kwargs = {
            "visible": self.show_axis,
            "layer": "below traces"
        }

        # zooming
        kwargs["width"] = self.width
        kwargs["height"] = self.height
        xaxes_kwargs["range"] = self.range_x
        yaxes_kwargs["range"] = self.range_y

        fig.update_layout(**kwargs)
        fig.update_xaxes(**xaxes_kwargs)
        fig.update_yaxes(**yaxes_kwargs)

        self._clear_ranges()
        return fig

    def _clear_ranges(self):
        if self._clear_x_ranges:
            self.range_x = None
            self.scaling = 1
        if self._clear_y_ranges:
            self.range_y = None
            self.scaling = 1
