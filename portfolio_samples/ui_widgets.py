"""Selected non-core UI components from FaceTrack Analytics v1.0.0.

The production identity-resolution implementation, calibrated decision rules,
model configuration, and private diagnostics are intentionally not included.
"""

from PySide6.QtCore import QPointF, QRectF, QTimer, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QScrollArea, QSizePolicy, QToolButton, QWidget

class LineChartWidget(QWidget):
    """Small native Qt chart for runtime values only.

    The count-history variant keeps a stable, data-driven Y range and renders the
    cumulative unique series as a step chart.  No synthetic/smoothed data points
    are created: the painter only changes how real samples are connected.
    """
    def __init__(self, parent=None, dual=False, compact=False,
                 color_a="#1597FF", color_b="#2DD36F",
                 series_b_step=False, chart_kind="performance"):
        super().__init__(parent)
        self.dual = dual
        self.compact = compact
        self.color_a = color_a
        self.color_b = color_b
        self.series_b_step = bool(series_b_step)
        self.chart_kind = chart_kind
        self.a: list[float] = []
        self.b: list[float] = []
        self.duration_seconds = 0.0
        self._display_vmax: float | None = None
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMinimumHeight(0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_data(self, a, b=None):
        self.a = [float(v) for v in a]
        self.b = [float(v) for v in (b or [])]
        if not self.a and not self.b:
            self._display_vmax = None
        self.update()

    def set_duration(self, seconds: float):
        self.duration_seconds = max(0.0, float(seconds or 0.0))
        self.update()

    @staticmethod
    def _nice_count_max(v: float) -> float:
        """Ceiling used by Count History (11→15, 23→30, ~52→60)."""
        import math
        v = max(1.0, float(v))
        padded = v + max(2.0, v * 0.12)
        if padded <= 20:
            step = 5.0
        elif padded <= 100:
            step = 10.0
        elif padded <= 200:
            step = 20.0
        elif padded <= 500:
            step = 50.0
        else:
            magnitude = 10 ** max(1, int(math.floor(math.log10(padded))) - 1)
            step = float(magnitude)
        return max(step, math.ceil(padded / step) * step)

    @staticmethod
    def _nice_perf_max(v: float) -> float:
        import math
        v = max(1.0, float(v))
        if v <= 60:
            return 60.0
        if v <= 100:
            return 100.0
        p = 10 ** int(math.floor(math.log10(v)))
        return float(math.ceil(v / p) * p)

    def _axis_range(self, values: list[float]) -> tuple[float, float]:
        if self.compact and self.chart_kind == "confidence":
            return 0.0, 100.0

        raw_max = max(values, default=0.0)
        if self.chart_kind == "count":
            target = self._nice_count_max(raw_max if raw_max > 0 else 5.0)
            # During a session the axis only expands. This prevents visual jumping
            # while still giving low counts useful vertical space.
            if self._display_vmax is None or target > self._display_vmax:
                self._display_vmax = target
            return 0.0, max(5.0, float(self._display_vmax or target))

        target = self._nice_perf_max(raw_max * 1.08)
        if self._display_vmax is None or target > self._display_vmax:
            self._display_vmax = target
        return 0.0, max(1.0, float(self._display_vmax or target))

    @staticmethod
    def _line_path(points: list[QPointF]) -> QPainterPath:
        path = QPainterPath()
        if not points:
            return path
        path.moveTo(points[0])
        for point in points[1:]:
            path.lineTo(point)
        return path

    @staticmethod
    def _step_path(points: list[QPointF]) -> QPainterPath:
        path = QPainterPath()
        if not points:
            return path
        path.moveTo(points[0])
        previous = points[0]
        for point in points[1:]:
            path.lineTo(QPointF(point.x(), previous.y()))
            path.lineTo(point)
            previous = point
        return path

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        if not self.compact:
            p.fillRect(self.rect(), QColor("#010A16"))

        left = 5 if self.compact else 38
        right = 5 if self.compact else (20 if self.dual else 12)
        top = 4 if self.compact else 11
        bottom = 4 if self.compact else (25 if self.dual else 11)
        r = self.rect().adjusted(left, top, -right, -bottom)
        if r.width() < 4 or r.height() < 4:
            return

        values = self.a + (self.b if self.dual else [])
        vmin, vmax = self._axis_range(values)

        if not self.compact:
            grid = QColor("#11243A")
            grid.setAlpha(125)
            p.setPen(QPen(grid, 1))
            y_steps = 4 if self.dual else 5
            x_steps = 6 if self.dual else 4
            for i in range(y_steps):
                y = r.top() + r.height() * i / max(1, y_steps - 1)
                p.drawLine(r.left(), int(y), r.right(), int(y))
            for i in range(x_steps):
                x = r.left() + r.width() * i / max(1, x_steps - 1)
                p.drawLine(int(x), r.top(), int(x), r.bottom())

            p.setFont(QFont("Segoe UI", 8))
            p.setPen(QColor("#8290A3"))
            for i in range(y_steps):
                val = vmax * (y_steps - 1 - i) / max(1, y_steps - 1)
                y = r.top() + r.height() * i / max(1, y_steps - 1)
                p.drawText(QRectF(0, y - 7, left - 7, 14),
                           Qt.AlignRight | Qt.AlignVCenter, f"{val:.0f}")

            if self.dual and self.duration_seconds > 0:
                # Clamp the first/last text boxes inside the widget so the final
                # timestamp can never be clipped by the panel border.
                for i in range(x_steps):
                    sec = self.duration_seconds * i / max(1, x_steps - 1)
                    m = int(sec // 60)
                    sec_i = int(sec % 60)
                    x = r.left() + r.width() * i / max(1, x_steps - 1)
                    if i == 0:
                        box = QRectF(r.left(), r.bottom() + 4, 52, 15)
                        align = Qt.AlignLeft
                    elif i == x_steps - 1:
                        box = QRectF(r.right() - 52, r.bottom() + 4, 52, 15)
                        align = Qt.AlignRight
                    else:
                        box = QRectF(x - 28, r.bottom() + 4, 56, 15)
                        align = Qt.AlignHCenter
                    p.drawText(box, align | Qt.AlignVCenter, f"{m:02d}:{sec_i:02d}")

        def points(vals):
            if len(vals) < 2:
                return []
            n = len(vals) - 1
            out = []
            span = max(1e-9, vmax - vmin)
            for i, value in enumerate(vals):
                x = r.left() + r.width() * i / n
                normalized = (max(vmin, min(vmax, float(value))) - vmin) / span
                y = r.bottom() - r.height() * normalized
                out.append(QPointF(x, max(r.top() + 1, min(r.bottom() - 1, y))))
            return out

        def draw_series(vals, color, width, *, fill=False, step=False):
            pts = points(vals)
            if len(pts) < 2:
                return
            path = self._step_path(pts) if step else self._line_path(pts)
            p.save()
            p.setClipRect(r.adjusted(-2, -2, 2, 2))
            if fill:
                area = QPainterPath(path)
                area.lineTo(pts[-1].x(), r.bottom())
                area.lineTo(pts[0].x(), r.bottom())
                area.closeSubpath()
                grad = QLinearGradient(0, r.top(), 0, r.bottom())
                c1 = QColor(color); c1.setAlpha(34)
                c2 = QColor(color); c2.setAlpha(1)
                grad.setColorAt(0, c1); grad.setColorAt(1, c2)
                p.fillPath(area, QBrush(grad))
            pen = QPen(QColor(color), width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            p.drawPath(path)
            if not self.compact:
                last = pts[-1]
                glow = QColor(color); glow.setAlpha(45)
                p.setPen(Qt.NoPen); p.setBrush(glow); p.drawEllipse(last, 3.5, 3.5)
                p.setBrush(QColor(color)); p.drawEllipse(last, 1.6, 1.6)
            p.restore()

        if self.a:
            draw_series(self.a, self.color_a, 2.0 if self.compact else 2.1,
                        fill=(not self.dual and not self.compact), step=False)
        if self.dual and self.b:
            draw_series(self.b, self.color_b, 2.1, fill=False,
                        step=self.series_b_step)


class CircularMediaButton(QToolButton):
    """Reusable 40x40 FaceTrack media Play/Pause control."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = "play"
        self.setFixedSize(40, 40)
        self.setMinimumSize(40, 40)
        self.setMaximumSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setStyleSheet("background:transparent; border:0; padding:0; margin:0;")
        # Do NOT apply a QRegion ellipse mask here. QRegion is a hard 1-bit mask
        # and produces visibly stair-stepped/jagged circular edges on Windows.
        # The transparent widget + antialiased QPainter ellipse below gives a
        # genuinely smooth circle while preserving the exact 40×40 footprint.

    def set_state(self, state: str):
        state = "pause" if str(state) == "pause" else "play"
        if state != self._state:
            self._state = state
            self.update()

    def state(self) -> str:
        return self._state

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        if not self.isEnabled():
            # Empty-state player remains visually consistent with the loaded-video
            # state: keep the FaceTrack electric-blue circle, while the disabled
            # interaction itself is still enforced by Qt.
            fill = QColor("#0A5DB8")
            glyph = QColor("#DCEEFF")
        elif self.isDown():
            fill = QColor("#084D99")
            glyph = QColor("#DCEEFF")
        elif self.underMouse():
            fill = QColor("#0D6BC9")
            glyph = QColor("#F5FBFF")
        else:
            # Reference-like medium electric blue.
            fill = QColor("#0A5DB8")
            glyph = QColor("#DCEEFF")

        # No outer border: only the blue circular face.
        # A 1 px transparent inset keeps antialias coverage away from the widget
        # boundary and prevents clipped/rough circumference pixels.
        p.setPen(Qt.NoPen)
        p.setBrush(fill)
        p.drawEllipse(QRectF(1.0, 1.0, 38.0, 38.0))

        pen = QPen(glyph, 2.15, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)

        if self._state == "pause":
            p.drawLine(QPointF(16.0, 13.0), QPointF(16.0, 27.0))
            p.drawLine(QPointF(24.0, 13.0), QPointF(24.0, 27.0))
        else:
            # Slight right optical shift makes the outlined triangle look centered.
            path = QPainterPath()
            path.moveTo(16.3, 12.7)
            path.lineTo(16.3, 27.3)
            path.lineTo(27.3, 20.0)
            path.closeSubpath()
            p.drawPath(path)

        p.end()


class StableWorkspaceScrollArea(QScrollArea):
    """QScrollArea whose content extent is recalculated from the current viewport.

    This prevents a maximized Workspace height from being retained after Restore
    and keeps the dashboard scrollbar independent from focus/log scrolling.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sync_pending = False
        self._syncing = False
        self.setWidgetResizable(False)

    def setWidget(self, widget):
        super().setWidget(widget)
        self.schedule_extent_sync()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.schedule_extent_sync()

    def schedule_extent_sync(self):
        if self._sync_pending:
            return
        self._sync_pending = True
        QTimer.singleShot(0, self.sync_extent)

    def sync_extent(self):
        self._sync_pending = False
        if self._syncing:
            return
        widget = self.widget()
        if widget is None:
            return

        self._syncing = True
        try:
            layout = widget.layout()
            if layout is not None:
                layout.invalidate()
                layout.activate()

            widget.setMinimumSize(0, 0)
            widget.setMaximumSize(16777215, 16777215)
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            minimum_h = widget.minimumSizeHint().height()
            if layout is not None:
                minimum_h = max(minimum_h, layout.minimumSize().height())

            viewport_w = max(1, self.viewport().width())
            viewport_h = max(1, self.viewport().height())
            target_h = max(viewport_h, minimum_h)

            widget.resize(viewport_w, target_h)
            widget.updateGeometry()
        finally:
            self._syncing = False
