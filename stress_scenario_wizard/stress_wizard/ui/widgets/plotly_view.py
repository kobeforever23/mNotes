from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go

from PySide6.QtWidgets import QTextBrowser, QVBoxLayout, QWidget


try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
except Exception:  # pragma: no cover
    QWebEngineView = None


class PlotlyWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        if QWebEngineView is not None:
            self.view = QWebEngineView(self)
        else:
            self.view = QTextBrowser(self)
            self.view.setText("Qt WebEngine is unavailable. Install PySide6-Essentials with WebEngine support.")
        self.layout.addWidget(self.view)

    def set_figure(self, fig: go.Figure) -> None:
        html = fig.to_html(include_plotlyjs="cdn", full_html=False)
        if QWebEngineView is not None:
            self.view.setHtml(html)
        else:
            self.view.setHtml(html)


def make_heatmap(frame, x: str, y: str, value: str, title: str) -> go.Figure:
    pivot = frame.pivot(index=y, columns=x, values=value)
    fig = px.imshow(
        pivot,
        text_auto=True,
        color_continuous_scale="RdYlGn",
        aspect="auto",
        title=title,
    )
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=50, b=20))
    return fig


def make_waterfall(labels: list[str], values: list[float], title: str) -> go.Figure:
    fig = go.Figure(
        go.Waterfall(
            x=labels,
            y=values,
            measure=["relative"] * len(values),
            connector={"line": {"color": "#95a5a6"}},
            decreasing={"marker": {"color": "#ff5f56"}},
            increasing={"marker": {"color": "#27ae60"}},
            totals={"marker": {"color": "#1f77b4"}},
        )
    )
    fig.update_layout(title=title, template="plotly_dark", margin=dict(l=20, r=20, t=50, b=20))
    return fig


def make_tornado(frame, title: str) -> go.Figure:
    show = frame.head(15).sort_values("max_abs_impact", ascending=True)
    fig = px.bar(
        show,
        x="max_abs_impact",
        y="parameter",
        orientation="h",
        color="max_abs_impact",
        color_continuous_scale="Reds",
        title=title,
    )
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=50, b=20))
    return fig
