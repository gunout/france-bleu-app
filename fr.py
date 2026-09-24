import sys
import math
import os
import random
import webbrowser
import locale
import mpv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QListWidget,
                              QListWidgetItem, QLabel, QFrame, QSlider,
                              QDialog, QLineEdit)
from PyQt6.QtCore import (Qt, QTimer, QSize, QPropertyAnimation,
                          QEasingCurve, QRectF)
from PyQt6.QtGui import (QFont, QColor, QIcon, QPixmap, QPainter, QPainterPath,
                         QPen, QCursor, QLinearGradient, QBrush)

# --- IMPORTANT : corriger le locale AVANT de créer mpv ---
locale.setlocale(locale.LC_NUMERIC, 'C')


# ============================================================
#  GUNOUT PLAYER — Édition exclusive FRANCE BLEU / ICI
#  Intégration vidéo native (wid) — compatible YouTube
# ============================================================

# --- Les 44 radios France Bleu (flux audio stables) ---
FRANCE_BLEU_AUDIO = [
    {"name": "France Bleu Alsace",              "url": "https://icecast.radiofrance.fr/fbalsace-midfi.mp3"},
    {"name": "France Bleu Armorique",           "url": "https://icecast.radiofrance.fr/fbarmorique-midfi.mp3"},
    {"name": "France Bleu Auxerre",             "url": "https://icecast.radiofrance.fr/fbauxerre-midfi.mp3"},
    {"name": "France Bleu Azur",                "url": "https://icecast.radiofrance.fr/fbazur-midfi.mp3"},
    {"name": "France Bleu Béarn Bigorre",       "url": "https://icecast.radiofrance.fr/fbbearn-midfi.mp3"},
    {"name": "France Bleu Belfort-Montbéliard", "url": "https://icecast.radiofrance.fr/fbbelfort-midfi.mp3"},
    {"name": "France Bleu Berry",               "url": "https://icecast.radiofrance.fr/fbberry-midfi.mp3"},
    {"name": "France Bleu Besançon",            "url": "https://icecast.radiofrance.fr/fbbesancon-midfi.mp3"},
    {"name": "France Bleu Bourgogne",           "url": "https://icecast.radiofrance.fr/fbbourgogne-midfi.mp3"},
    {"name": "France Bleu Breizh Izel",         "url": "https://icecast.radiofrance.fr/fbbreizhizel-midfi.mp3"},
    {"name": "France Bleu Champagne-Ardenne",   "url": "https://icecast.radiofrance.fr/fbchampagne-midfi.mp3"},
    {"name": "France Bleu Corse RCFM",          "url": "https://icecast.radiofrance.fr/fbrcfm-midfi.mp3"},
    {"name": "France Bleu Cotentin",            "url": "https://icecast.radiofrance.fr/fbcotentin-midfi.mp3"},
    {"name": "France Bleu Creuse",              "url": "https://icecast.radiofrance.fr/fbcreuse-midfi.mp3"},
    {"name": "France Bleu Drôme Ardèche",       "url": "https://icecast.radiofrance.fr/fbdromeardeche-midfi.mp3"},
    {"name": "France Bleu Elsass",              "url": "https://icecast.radiofrance.fr/fbelsass-midfi.mp3"},
    {"name": "France Bleu Gard Lozère",         "url": "https://icecast.radiofrance.fr/fbgardlozere-midfi.mp3"},
    {"name": "France Bleu Gascogne",            "url": "https://icecast.radiofrance.fr/fbgascogne-midfi.mp3"},
    {"name": "France Bleu Gironde",             "url": "https://icecast.radiofrance.fr/fbgironde-midfi.mp3"},
    {"name": "France Bleu Hérault",             "url": "https://icecast.radiofrance.fr/fbherault-midfi.mp3"},
    {"name": "France Bleu Isère",               "url": "https://icecast.radiofrance.fr/fbisere-midfi.mp3"},
    {"name": "France Bleu La Rochelle",         "url": "https://icecast.radiofrance.fr/fblarochelle-midfi.mp3"},
    {"name": "France Bleu Limousin",            "url": "https://icecast.radiofrance.fr/fblimousin-midfi.mp3"},
    {"name": "France Bleu Loire Océan",         "url": "https://icecast.radiofrance.fr/fbloireocean-midfi.mp3"},
    {"name": "France Bleu Lorraine Nord",       "url": "https://icecast.radiofrance.fr/fblorrainenord-midfi.mp3"},
    {"name": "France Bleu Maine",               "url": "https://icecast.radiofrance.fr/fbmaine-midfi.mp3"},
    {"name": "France Bleu Mayenne",             "url": "https://icecast.radiofrance.fr/fbmayenne-midfi.mp3"},
    {"name": "France Bleu Nord",                "url": "https://icecast.radiofrance.fr/fbnord-midfi.mp3"},
    {"name": "France Bleu Normandie (Caen)",    "url": "https://icecast.radiofrance.fr/fbnormandiecaen-midfi.mp3"},
    {"name": "France Bleu Normandie (Rouen)",   "url": "https://icecast.radiofrance.fr/fbnormandierouen-midfi.mp3"},
    {"name": "France Bleu Occitanie",           "url": "https://icecast.radiofrance.fr/fboccitanie-midfi.mp3"},
    {"name": "France Bleu Orléans",             "url": "https://icecast.radiofrance.fr/fborleans-midfi.mp3"},
    {"name": "France Bleu Paris",               "url": "https://icecast.radiofrance.fr/fb1071-midfi.mp3"},
    {"name": "France Bleu Pays Basque",         "url": "https://icecast.radiofrance.fr/fbpaysbasque-midfi.mp3"},
    {"name": "France Bleu Pays d'Auvergne",     "url": "https://icecast.radiofrance.fr/fbpaysdauvergne-midfi.mp3"},
    {"name": "France Bleu Pays de Savoie",      "url": "https://icecast.radiofrance.fr/fbpaysdesavoie-midfi.mp3"},
    {"name": "France Bleu Périgord",            "url": "https://icecast.radiofrance.fr/fbperigord-midfi.mp3"},
    {"name": "France Bleu Picardie",            "url": "https://icecast.radiofrance.fr/fbpicardie-midfi.mp3"},
    {"name": "France Bleu Poitou",              "url": "https://icecast.radiofrance.fr/fbpoitou-midfi.mp3"},
    {"name": "France Bleu Provence",            "url": "https://icecast.radiofrance.fr/fbprovence-midfi.mp3"},
    {"name": "France Bleu Roussillon",          "url": "https://icecast.radiofrance.fr/fbroussillon-midfi.mp3"},
    {"name": "France Bleu Saint-Étienne Loire", "url": "https://icecast.radiofrance.fr/fbstetienne-midfi.mp3"},
    {"name": "France Bleu Sud Lorraine",        "url": "https://icecast.radiofrance.fr/fbsudlorraine-midfi.mp3"},
    {"name": "France Bleu Touraine",            "url": "https://icecast.radiofrance.fr/fbtouraine-midfi.mp3"},
    {"name": "France Bleu Vaucluse",            "url": "https://icecast.radiofrance.fr/fbvaucluse-midfi.mp3"},
]

# --- Flux vidéo France 3 régions (ICI Matin) ---
FRANCE_3_VIDEO = [
    {"name": "ICI Matin — France 3 Alsace",           "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/fals.m3u8"},
    {"name": "ICI Matin — France 3 Champagne",        "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/fchg.m3u8"},
    {"name": "ICI Matin — France 3 Lorraine",         "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/flor.m3u8"},
    {"name": "ICI Matin — France 3 Nord PDC",         "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/fpdc.m3u8"},
    {"name": "ICI Matin — France 3 Picardie",         "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/fpcd.m3u8"},
    {"name": "ICI Matin — France 3 B.Normandie",      "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/fbnr.m3u8"},
    {"name": "ICI Matin — France 3 H.Normandie",      "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/fhnr.m3u8"},
    {"name": "ICI Matin — France 3 Aquitaine",        "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/faqt.m3u8"},
    {"name": "ICI Matin — France 3 NOA",              "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/fnoa.m3u8"},
    {"name": "ICI Matin — France 3 Limousin",         "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/flms.m3u8"},
    {"name": "ICI Matin — France 3 Poitou Charentes", "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/fpch.m3u8"},
    {"name": "ICI Matin — France 3 Midi Pyrénées",    "url": "https://raw.githubusercontent.com/ipstreet312/freeiptv/master/ressources/ftv/py/fmpr.m3u8"},
]

# --- France Info TV (YouTube) ---
YOUTUBE_STREAMS = [
    {"name": "France Info — Direct YouTube", "url": "https://www.youtube.com/watch?v=NG7ZX42nZKc"},
]

FRANCE_3_VIDEO = FRANCE_3_VIDEO + YOUTUBE_STREAMS

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")

# ----- Palette (bleu France Bleu) -----
BG          = "rgba(12, 12, 14, 240)"
POPUP_BG    = "rgba(18, 18, 22, 250)"
SURFACE     = "rgba(255, 255, 255, 6)"
SURFACE_HOV = "rgba(255, 255, 255, 14)"

ACCENT      = "#3d7bd9"
ACCENT_SOFT = "rgba(61, 123, 217, 22)"
ACCENT_GLOW = "rgba(61, 123, 217, 40)"

TEXT        = "#f5f5f7"
TEXT_DIM    = "rgba(245, 245, 247, 100)"
SIGNATURE   = "rgba(245, 245, 247, 30)"
CHEVRON     = "rgba(245, 245, 247, 150)"


STYLE = f"""
QMainWindow, QWidget#root {{
    background: {BG};
    border-radius: 14px;
    border: none;
}}
QLabel#logo {{ background: transparent; padding: 2px 4px; }}
QLabel#signature {{ color: {SIGNATURE}; font-size: 9px; letter-spacing: 3px; padding: 0 8px 4px 8px; }}
QListWidget#stations {{
    background: rgba(255, 255, 255, 4);
    color: {TEXT};
    border: none;
    border-radius: 10px;
    padding: 6px;
    font-size: 12px;
    letter-spacing: 1px;
    outline: none;
}}
QListWidget#stations::item {{ padding: 8px 12px; border-radius: 8px; margin: 2px 0; }}
QListWidget#stations::item:hover {{ background: {SURFACE_HOV}; }}
QListWidget#stations::item:selected {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
QLineEdit#search {{
    background: {SURFACE}; color: {TEXT}; border: none; border-radius: 10px;
    padding: 8px 12px; font-size: 11px; letter-spacing: 1px;
}}
QLineEdit#search:focus {{ background: {SURFACE_HOV}; }}
QFrame#stage {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0a0d12, stop:0.5 #06080b, stop:1 #04060a);
    border: none;
    border-radius: 12px;
}}
QFrame#controls {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(0,0,0,0), stop:0.4 rgba(0,0,0,120), stop:1 rgba(0,0,0,180));
    border: none;
    border-bottom-left-radius: 12px;
    border-bottom-right-radius: 12px;
}}
QPushButton#ctrl {{
    background: transparent; border: none; border-radius: 15px;
    padding: 4px; min-width: 30px; min-height: 30px;
}}
QPushButton#ctrl:hover {{ background: {SURFACE_HOV}; }}
QPushButton#site {{
    background: {SURFACE}; color: {TEXT}; border: none; border-radius: 15px;
    padding: 5px 12px; font-size: 10px; font-weight: 700; letter-spacing: 2px;
}}
QPushButton#site:hover {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
QPushButton#site:checked {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
QDialog#popup {{
    background: {POPUP_BG}; border: 1px solid rgba(255, 255, 255, 12); border-radius: 14px;
}}
QLabel#popup_title {{ color: {TEXT}; font-size: 13px; font-weight: 700; letter-spacing: 4px; padding: 4px; }}
QLabel#popup_sub {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 2px; padding: 0 4px 6px 4px; }}
QPushButton#popup_item {{
    background: {SURFACE}; color: {TEXT}; border: none; border-radius: 10px;
    padding: 12px 14px; font-size: 11px; letter-spacing: 1px; text-align: left;
}}
QPushButton#popup_item:hover {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
QPushButton#popup_item:pressed {{ background: {ACCENT_GLOW}; }}
QPushButton#popup_close {{
    background: transparent; color: {TEXT_DIM}; border: none; border-radius: 15px;
    padding: 4px; min-width: 30px; min-height: 30px;
}}
QPushButton#popup_close:hover {{ background: {SURFACE_HOV}; color: {TEXT}; }}
QSlider::groove:horizontal {{ height: 3px; background: rgba(255,255,255,12); border-radius: 2px; }}
QSlider::sub-page:horizontal {{ background: {ACCENT}; border-radius: 2px; }}
QSlider::handle:horizontal {{
    background: #fff; width: 10px; height: 10px; margin: -4px 0; border-radius: 5px; border: none;
}}
QSlider::handle:horizontal:hover {{
    background: {ACCENT}; width: 12px; height: 12px; margin: -5px 0; border-radius: 6px;
}}
QLabel#status {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 2px; padding: 2px 6px; }}
QLabel#time {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 0.5px; min-width: 80px; }}
QLabel#nowplaying {{ color: {TEXT}; font-size: 17px; font-weight: 700; letter-spacing: 3px; }}
QLabel#nowmeta {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 2px; }}
"""


# ================= ICÔNES =================
def _make_icon(kind, size=16, color="#f5f5f7"):
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color))
    pen.setWidthF(1.4)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(QColor(color))
    s = size
    if kind == "play":
        path = QPainterPath()
        path.moveTo(s*0.32, s*0.24); path.lineTo(s*0.76, s*0.50)
        path.lineTo(s*0.32, s*0.76); path.closeSubpath()
        p.drawPath(path)
    elif kind == "pause":
        p.drawRoundedRect(int(s*0.32), int(s*0.24), int(s*0.12), int(s*0.52), 2, 2)
        p.drawRoundedRect(int(s*0.56), int(s*0.24), int(s*0.12), int(s*0.52), 2, 2)
    elif kind == "stop":
        p.drawRoundedRect(int(s*0.32), int(s*0.32), int(s*0.36), int(s*0.36), 3, 3)
    elif kind == "volume":
        path = QPainterPath()
        path.moveTo(s*0.20, s*0.42); path.lineTo(s*0.34, s*0.42)
        path.lineTo(s*0.48, s*0.28); path.lineTo(s*0.48, s*0.72)
        path.lineTo(s*0.34, s*0.58); path.lineTo(s*0.20, s*0.58)
        path.closeSubpath()
        p.drawPath(path)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawArc(int(s*0.44), int(s*0.34), int(s*0.24), int(s*0.32), -50*16, 100*16)
    elif kind == "mute":
        path = QPainterPath()
        path.moveTo(s*0.20, s*0.42); path.lineTo(s*0.34, s*0.42)
        path.lineTo(s*0.48, s*0.28); path.lineTo(s*0.48, s*0.72)
        path.lineTo(s*0.34, s*0.58); path.lineTo(s*0.20, s*0.58)
        path.closeSubpath()
        p.drawPath(path)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.60), int(s*0.38), int(s*0.80), int(s*0.62))
        p.drawLine(int(s*0.80), int(s*0.38), int(s*0.60), int(s*0.62))
    elif kind == "close":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.30), int(s*0.30), int(s*0.70), int(s*0.70))
        p.drawLine(int(s*0.70), int(s*0.30), int(s*0.30), int(s*0.70))
    elif kind == "min":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.28), int(s*0.52), int(s*0.72), int(s*0.52))
    elif kind == "chevron-down":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.30), int(s*0.42), int(s*0.50), int(s*0.62))
        p.drawLine(int(s*0.50), int(s*0.62), int(s*0.70), int(s*0.42))
    elif kind == "chevron-up":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.30), int(s*0.58), int(s*0.50), int(s*0.38))
        p.drawLine(int(s*0.50), int(s*0.38), int(s*0.70), int(s*0.58))
    p.end()
    return QIcon(pm)


# ================= VISUALISEUR (BLEU) =================
class Visualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.bars = 32
        self.values = [0.0] * self.bars
        self.targets = [0.0] * self.bars
        self.phase = 0.0
        self.playing = False
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self._tick)
        self.timer.start()

    def set_playing(self, playing):
        self.playing = playing

    def _tick(self):
        self.phase += 0.15
        for i in range(self.bars):
            if self.playing:
                base = 0.35 + 0.35 * abs(math.sin(self.phase + i * 0.35))
                self.targets[i] = base + random.uniform(-0.15, 0.25)
            else:
                self.targets[i] = 0.02
            self.targets[i] = max(0.02, min(1.0, self.targets[i]))
            self.values[i] += (self.targets[i] - self.values[i]) * 0.25
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return
        bar_w = w / self.bars * 0.55
        gap = w / self.bars
        cy = h / 2
        max_h = h * 0.55
        grad = QLinearGradient(0, cy - max_h/2, 0, cy + max_h/2)
        grad.setColorAt(0.0, QColor(93, 155, 240, 230))
        grad.setColorAt(0.5, QColor(61, 123, 217, 160))
        grad.setColorAt(1.0, QColor(28, 78, 156, 50))
        p.setBrush(QBrush(grad))
        p.setPen(Qt.PenStyle.NoPen)
        for i, v in enumerate(self.values):
            bh = max(2, v * max_h)
            x = i * gap + (gap - bar_w) / 2
            y = cy - bh / 2
            p.drawRoundedRect(QRectF(x, y, bar_w, bh), bar_w/2, bar_w/2)
        p.end()


# ================= POPUP INFO =================
class InfoPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("popup")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setModal(True)
        self.setFixedSize(360, 260)
        if parent:
            geo = parent.geometry()
            self.move(geo.center() - self.rect().center())
        self.setStyleSheet(STYLE)
        root = QWidget(self)
        root.setObjectName("popup")
        root.setGeometry(self.rect())
        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)
        header = QHBoxLayout()
        header.setSpacing(6)
        title = QLabel("FRANCE BLEU / ICI")
        title.setObjectName("popup_title")
        header.addWidget(title)
        header.addStretch()
        btn_close = QPushButton()
        btn_close.setObjectName("popup_close")
        btn_close.setIcon(_make_icon("close", 14, TEXT))
        btn_close.setIconSize(QSize(14, 14))
        btn_close.clicked.connect(self.reject)
        header.addWidget(btn_close)
        layout.addLayout(header)
        sub = QLabel("44 radios · 12 flux ICI Matin · France Info TV")
        sub.setObjectName("popup_sub")
        layout.addWidget(sub)
        layout.addStretch()
        btn_site = QPushButton("OUVRIR FRANCEBLEU.FR")
        btn_site.setObjectName("popup_item")
        btn_site.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_site.clicked.connect(self._open_site)
        layout.addWidget(btn_site)
        btn_ici = QPushButton("OUVRIR ICI.FR")
        btn_ici.setObjectName("popup_item")
        btn_ici.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_ici.clicked.connect(self._open_ici)
        layout.addWidget(btn_ici)
        btn_ftv = QPushButton("OUVRIR FRANCE.TV")
        btn_ftv.setObjectName("popup_item")
        btn_ftv.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_ftv.clicked.connect(self._open_ftv)
        layout.addWidget(btn_ftv)

    def _open_site(self):
        webbrowser.open("https://www.francebleu.fr/")
        self.accept()

    def _open_ici(self):
        webbrowser.open("https://www.ici.fr/")
        self.accept()

    def _open_ftv(self):
        webbrowser.open("https://www.france.tv/")
        self.accept()


# ================= FENÊTRE PRINCIPALE =================
class FranceBleuPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUNOUT PLAYER — FRANCE BLEU / ICI")
        self.resize(560, 640)
        self.setMinimumSize(380, 400)
        self.player = None            # mpv vidéo (wid natif)
        self.audio_player = None      # mpv audio-only
        self._drag_pos = None
        self._resize_edge = None
        self._resize_margin = 6
        self._controls_collapsed = False
        self._controls_full_height = 0
        self._window_folded = False
        self._unfolded_height = 640
        self._current_station = "AUCUNE STATION"
        self._current_type = "audio"
        self._filter_mode = "all"
        self._autostart_done = False
        self.setMouseTracking(True)
        self.setStyleSheet(STYLE)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # --- HUD top ---
        top = QHBoxLayout()
        top.setSpacing(8)
        self.logo = QLabel()
        self.logo.setObjectName("logo")
        pix = QPixmap(LOGO_PATH)
        if not pix.isNull():
            pix = pix.scaledToHeight(28, Qt.TransformationMode.SmoothTransformation)
            self.logo.setPixmap(pix)
        else:
            self.logo.setText("FRANCE BLEU")
            self.logo.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 700; letter-spacing: 4px;")
        self.logo.setFixedHeight(30)
        top.addWidget(self.logo)

        self.btn_filter_audio = QPushButton("RADIOS")
        self.btn_filter_audio.setObjectName("site")
        self.btn_filter_audio.setCheckable(True)
        self.btn_filter_audio.setChecked(True)
        self.btn_filter_audio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_filter_audio.clicked.connect(lambda: self._set_filter("audio"))
        top.addWidget(self.btn_filter_audio)

        self.btn_filter_video = QPushButton("TV")
        self.btn_filter_video.setObjectName("site")
        self.btn_filter_video.setCheckable(True)
        self.btn_filter_video.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_filter_video.clicked.connect(lambda: self._set_filter("video"))
        top.addWidget(self.btn_filter_video)

        self.btn_filter_all = QPushButton("TOUT")
        self.btn_filter_all.setObjectName("site")
        self.btn_filter_all.setCheckable(True)
        self.btn_filter_all.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_filter_all.clicked.connect(lambda: self._set_filter("all"))
        top.addWidget(self.btn_filter_all)

        btn_info = QPushButton("INFO")
        btn_info.setObjectName("site")
        btn_info.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_info.clicked.connect(self.open_info_popup)
        top.addWidget(btn_info)

        top.addStretch()
        btn_min = QPushButton()
        btn_min.setObjectName("ctrl")
        btn_min.setIcon(_make_icon("min", 14, TEXT))
        btn_min.setIconSize(QSize(14, 14))
        btn_min.clicked.connect(self.showMinimized)
        top.addWidget(btn_min)
        btn_close = QPushButton()
        btn_close.setObjectName("ctrl")
        btn_close.setIcon(_make_icon("close", 14, TEXT))
        btn_close.setIconSize(QSize(14, 14))
        btn_close.clicked.connect(self.close)
        top.addWidget(btn_close)
        self.btn_fold = QPushButton()
        self.btn_fold.setObjectName("ctrl")
        self.btn_fold.setIcon(_make_icon("chevron-up", 14, CHEVRON))
        self.btn_fold.setIconSize(QSize(14, 14))
        self.btn_fold.setToolTip("Replier la fenêtre")
        self.btn_fold.clicked.connect(self.toggle_window_fold)
        top.addWidget(self.btn_fold)
        layout.addLayout(top)

        self.signature = QLabel("by gleaphe — Édition France Bleu / ICI")
        self.signature.setObjectName("signature")
        layout.addWidget(self.signature)

        # --- Stage : un seul widget natif, mpv dessine dedans ---
        self.stage = QFrame()
        self.stage.setObjectName("stage")
        v_layout = QVBoxLayout(self.stage)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        # Le widget vidéo natif (mpv dessine dedans pour audio ET vidéo)
        self.video_widget = QWidget()
        self.video_widget.setAttribute(Qt.WidgetAttribute.WA_NativeWindow, True)
        self.video_widget.setAttribute(Qt.WidgetAttribute.WA_DontCreateNativeAncestors, True)
        v_layout.addWidget(self.video_widget, stretch=1)

        # Visualiseur superposé (affiché seulement en mode audio)
        self.viz = Visualizer(self.video_widget)
        self.viz.hide()

        # Overlay texte (audio seulement)
        self.overlay = QWidget(self.video_widget)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        ov = QVBoxLayout(self.overlay)
        ov.setContentsMargins(0, 0, 0, 0)
        ov.addStretch()
        self.lbl_now = QLabel(self._current_station)
        self.lbl_now.setObjectName("nowplaying")
        self.lbl_now.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_now.setStyleSheet("background: transparent;")
        ov.addWidget(self.lbl_now)
        ov.addSpacing(4)
        self.lbl_meta = QLabel("SÉLECTIONNEZ UNE STATION")
        self.lbl_meta.setObjectName("nowmeta")
        self.lbl_meta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_meta.setStyleSheet("background: transparent;")
        ov.addWidget(self.lbl_meta)
        ov.addStretch()

        # --- Contrôles ---
        self.controls = QFrame()
        self.controls.setObjectName("controls")
        c_layout = QVBoxLayout(self.controls)
        c_layout.setContentsMargins(12, 6, 12, 8)
        c_layout.setSpacing(4)
        row = QHBoxLayout()
        row.setSpacing(4)
        self.btn_play = QPushButton()
        self.btn_play.setObjectName("ctrl")
        self.btn_play.setIcon(_make_icon("play", 16, TEXT))
        self.btn_play.setIconSize(QSize(16, 16))
        self.btn_play.clicked.connect(self.toggle_pause)
        row.addWidget(self.btn_play)
        self.btn_stop = QPushButton()
        self.btn_stop.setObjectName("ctrl")
        self.btn_stop.setIcon(_make_icon("stop", 12, TEXT))
        self.btn_stop.setIconSize(QSize(12, 12))
        self.btn_stop.clicked.connect(self.stop)
        row.addWidget(self.btn_stop)
        self.time_lbl = QLabel("EN DIRECT")
        self.time_lbl.setObjectName("time")
        row.addWidget(self.time_lbl)
        row.addStretch()
        self.btn_mute = QPushButton()
        self.btn_mute.setObjectName("ctrl")
        self.btn_mute.setIcon(_make_icon("volume", 14, TEXT))
        self.btn_mute.setIconSize(QSize(14, 14))
        self.btn_mute.clicked.connect(self.toggle_mute)
        row.addWidget(self.btn_mute)
        self.vol = QSlider(Qt.Orientation.Horizontal)
        self.vol.setRange(0, 100)
        self.vol.setValue(80)
        self.vol.setFixedWidth(80)
        self.vol.valueChanged.connect(self.set_volume)
        row.addWidget(self.vol)
        self.btn_toggle = QPushButton()
        self.btn_toggle.setObjectName("ctrl")
        self.btn_toggle.setIcon(_make_icon("chevron-down", 12, CHEVRON))
        self.btn_toggle.setIconSize(QSize(12, 12))
        self.btn_toggle.clicked.connect(self.toggle_controls)
        row.addWidget(self.btn_toggle)
        c_layout.addLayout(row)
        v_layout.addWidget(self.controls)

        self.btn_reopen = QPushButton(self.stage)
        self.btn_reopen.setObjectName("ctrl")
        self.btn_reopen.setIcon(_make_icon("chevron-up", 14, CHEVRON))
        self.btn_reopen.setIconSize(QSize(14, 14))
        self.btn_reopen.setFixedSize(30, 30)
        self.btn_reopen.setStyleSheet("""
            QPushButton { background: rgba(12, 12, 14, 180); border: none; border-radius: 15px; }
            QPushButton:hover { background: rgba(61, 123, 217, 40); }
        """)
        self.btn_reopen.clicked.connect(self.toggle_controls)
        self.btn_reopen.hide()
        layout.addWidget(self.stage, stretch=1)

        # --- Recherche ---
        self.search = QLineEdit()
        self.search.setObjectName("search")
        self.search.setPlaceholderText("RECHERCHER UNE STATION OU UNE MATINALE...")
        self.search.textChanged.connect(self._apply_filters)
        layout.addWidget(self.search)

        # --- Liste ---
        self.header_lbl = QLabel("44 STATIONS FRANCE BLEU / ICI")
        self.header_lbl.setObjectName("status")
        layout.addWidget(self.header_lbl)
        self.stations = QListWidget()
        self.stations.setObjectName("stations")
        self.stations.setMaximumHeight(200)
        self.stations.itemDoubleClicked.connect(self._play_station_item)
        self.stations.itemActivated.connect(self._play_station_item)
        self._populate_stations()
        layout.addWidget(self.stations)
        self.status = QLabel("PRÊT")
        self.status.setObjectName("status")
        layout.addWidget(self.status)

        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.setInterval(3500)
        self.hide_timer.timeout.connect(self._auto_hide_controls)

    # ---------- Liste / filtres ----------
    def _populate_stations(self):
        self.stations.clear()
        for st in FRANCE_BLEU_AUDIO:
            it = QListWidgetItem(f"📻  {st['name']}")
            it.setData(Qt.ItemDataRole.UserRole, {**st, "type": "audio"})
            self.stations.addItem(it)
        for st in FRANCE_3_VIDEO:
            it = QListWidgetItem(f"📺  {st['name']}")
            it.setData(Qt.ItemDataRole.UserRole, {**st, "type": "video"})
            self.stations.addItem(it)

    def _set_filter(self, mode):
        self._filter_mode = mode
        self.btn_filter_audio.setChecked(mode == "audio")
        self.btn_filter_video.setChecked(mode == "video")
        self.btn_filter_all.setChecked(mode == "all")
        self._apply_filters()

    def _apply_filters(self):
        text = self.search.text().lower().strip()
        visible_count = 0
        for i in range(self.stations.count()):
            item = self.stations.item(i)
            data = item.data(Qt.ItemDataRole.UserRole)
            stype = data.get("type", "audio")
            if self._filter_mode != "all" and stype != self._filter_mode:
                item.setHidden(True)
                continue
            if text and text not in item.text().lower():
                item.setHidden(True)
                continue
            item.setHidden(False)
            visible_count += 1
        if self._filter_mode == "audio":
            self.header_lbl.setText(f"{visible_count} RADIOS FRANCE BLEU / ICI")
        elif self._filter_mode == "video":
            self.header_lbl.setText(f"{visible_count} FLUX TV (ICI MATIN + FRANCE INFO)")
        else:
            self.header_lbl.setText(f"{visible_count} STATIONS (RADIOS + TV)")

    def open_info_popup(self):
        popup = InfoPopup(self)
        popup.exec()

    # ---------- Initialisation mpv ----------
    def showEvent(self, event):
        super().showEvent(event)

        # mpv vidéo avec fenêtre native (wid) — capable de lire YouTube
        if self.player is None:
            wid = int(self.video_widget.winId())
            self.player = mpv.MPV(
                wid=wid,
                vo='gpu',
                hwdec='auto-safe',
                osc=False,
                input_default_bindings=False,
                input_vo_keyboard=False,
                ytdl=True,
                ytdl_format='bestvideo+bestaudio/best',
                cache=True,
                cache_secs=3,
                demuxer_max_bytes='10M',
                demuxer_max_back_bytes='5M',
                demuxer_readahead_secs=2,
                network_timeout=15,
                audio_client_name='Gunout Player France Bleu',
                keep_open='yes',
                idle='yes',
            )
            self.player.volume = self.vol.value()

        # mpv audio-only (vo='null') pour les radios
        if self.audio_player is None:
            self.audio_player = mpv.MPV(
                vo='null', ao='pulse', ytdl=False, cache=True, cache_secs=3,
                demuxer_max_bytes='3M', demuxer_max_back_bytes='1M',
                demuxer_readahead_secs=2, network_timeout=15,
                audio_client_name='Gunout Player France Bleu Radio',
                force_window='no', idle='yes',
            )
            self.audio_player.volume = self.vol.value()

        # --- Lancement automatique de France Info TV après 1 seconde ---
        if not self._autostart_done:
            self._autostart_done = True
            QTimer.singleShot(1000, self._autostart_france_info)

    def _autostart_france_info(self):
        """Lance automatiquement France Info TV au démarrage."""
        for st in YOUTUBE_STREAMS:
            if "France Info" in st["name"]:
                self._play(st["url"], st["name"], "video")
                return

    # ---------- Lecture ----------
    def _play_station_item(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        self._play(data["url"], data["name"], data.get("type", "audio"))

    def _play(self, url, name, stream_type):
        self._current_type = stream_type
        self._current_station = name.upper()
        self.lbl_now.setText(self._current_station)

        if stream_type == "video":
            # Stop audio-only
            if self.audio_player:
                try:
                    self.audio_player.command('stop')
                except Exception:
                    pass

            # Stop aussi le mpv vidéo pour purger l'état précédent
            if self.player is not None:
                try:
                    self.player.command('stop')
                except Exception:
                    pass

            # Cacher viz + overlay → mpv dessine dans video_widget
            self.viz.hide()
            self.overlay.hide()
            self.btn_play.setIcon(_make_icon("pause", 16, TEXT))
            self.status.setText(f"TV : {name.upper()}")

            # Petit délai pour laisser mpv se réinitialiser avant play
            def _do_video_play():
                if self.player is not None:
                    try:
                        self.player.play(url)
                    except Exception as ex:
                        self.status.setText(f"ERREUR : {ex}")
            QTimer.singleShot(150, _do_video_play)
            self._reset_auto_hide()
            return

        # Audio
        if self.player is not None:
            try: self.player.command('stop')
            except Exception: pass
        # Afficher viz + overlay
        self.viz.show(); self.viz.raise_()
        self.viz.setGeometry(0, 0, self.video_widget.width(), self.video_widget.height())
        self.viz.set_playing(True)
        self.overlay.show(); self.overlay.raise_()
        self.overlay.setGeometry(0, 0, self.video_widget.width(), self.video_widget.height())

        if self.audio_player is None:
            self.status.setText("LECTEUR NON PRÊT")
            return
        try:
            self.audio_player.command('stop')
            self.audio_player.pause = False
            self.audio_player.mute = False
        except Exception:
            pass
        self.lbl_meta.setText("CONNEXION...")
        self.btn_play.setIcon(_make_icon("pause", 16, TEXT))
        self.status.setText(f"LECTURE : {name.upper()}")
        self._reset_auto_hide()

        def _do_play():
            try:
                self.audio_player.play(url)
                self.lbl_meta.setText("EN DIRECT")
            except Exception as ex:
                self.status.setText(f"ERREUR : {ex}")
                self.viz.set_playing(False)
                self.btn_play.setIcon(_make_icon("play", 16, TEXT))
        QTimer.singleShot(200, _do_play)

    # ---------- Contrôles ----------
    def toggle_pause(self):
        if self._current_type == "video":
            if self.player:
                self.player.pause = not self.player.pause
                self.btn_play.setIcon(_make_icon("play" if self.player.pause else "pause", 16, TEXT))
            return
        if not self.audio_player: return
        self.audio_player.pause = not self.audio_player.pause
        paused = self.audio_player.pause
        self.btn_play.setIcon(_make_icon("play" if paused else "pause", 16, TEXT))
        self.viz.set_playing(not paused)
        self.lbl_meta.setText("PAUSE" if paused else "EN DIRECT")

    def stop(self):
        if self.audio_player:
            try: self.audio_player.command('stop')
            except Exception: pass
        if self.player:
            try: self.player.command('stop')
            except Exception: pass
        self.viz.show(); self.viz.raise_()
        self.viz.set_playing(False)
        self.overlay.show(); self.overlay.raise_()
        self.btn_play.setIcon(_make_icon("play", 16, TEXT))
        self.lbl_now.setText("AUCUNE STATION")
        self.lbl_meta.setText("SÉLECTIONNEZ UNE STATION")
        self.status.setText("ARRÊTÉ")
        self._current_type = "audio"

    def toggle_mute(self):
        if self._current_type == "video":
            if self.player:
                self.player.mute = not self.player.mute
                self.btn_mute.setIcon(_make_icon("mute" if self.player.mute else "volume", 14, TEXT))
            return
        if not self.audio_player: return
        self.audio_player.mute = not self.audio_player.mute
        self.btn_mute.setIcon(_make_icon("mute" if self.audio_player.mute else "volume", 14, TEXT))

    def set_volume(self, v):
        if self.audio_player:
            try: self.audio_player.volume = v
            except Exception: pass
        if self.player:
            try: self.player.volume = v
            except Exception: pass

    # ---------- Replis fenêtre ----------
    def toggle_window_fold(self):
        if self._window_folded:
            self.stage.show(); self.signature.show()
            self.status.show(); self.stations.show()
            self.search.show(); self.header_lbl.show()
            self.btn_filter_audio.show(); self.btn_filter_video.show(); self.btn_filter_all.show()
            target_h = self._unfolded_height
            self.btn_fold.setIcon(_make_icon("chevron-up", 14, CHEVRON))
            self._window_folded = False
            self.setMinimumSize(380, 400)
        else:
            self._unfolded_height = self.height()
            self.stage.hide(); self.signature.hide()
            self.status.hide(); self.stations.hide()
            self.search.hide(); self.header_lbl.hide()
            self.btn_filter_audio.hide(); self.btn_filter_video.hide(); self.btn_filter_all.hide()
            target_h = 70
            self.btn_fold.setIcon(_make_icon("chevron-down", 14, CHEVRON))
            self._window_folded = True
            self.setMinimumSize(280, target_h)
        self.anim_fold = QPropertyAnimation(self, b"size")
        self.anim_fold.setDuration(240)
        self.anim_fold.setStartValue(self.size())
        self.anim_fold.setEndValue(QSize(self.width(), target_h))
        self.anim_fold.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim_fold.start()

    def _reset_auto_hide(self):
        if self._controls_collapsed or self._window_folded: return
        self.hide_timer.start()

    def _auto_hide_controls(self):
        if self._controls_collapsed or self._window_folded: return
        if self.controls.underMouse() or self.btn_reopen.underMouse():
            self.hide_timer.start(); return
        self._controls_collapsed = True
        self._controls_full_height = self.controls.height()
        self.btn_toggle.setIcon(_make_icon("chevron-up", 12, CHEVRON))
        self.btn_reopen.show(); self.btn_reopen.raise_()
        self._place_reopen_button()
        self.anim = QPropertyAnimation(self.controls, b"maximumHeight")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.controls.height())
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim.start()

    def toggle_controls(self):
        if self._controls_collapsed:
            target = self._controls_full_height or 60
            self.btn_toggle.setIcon(_make_icon("chevron-down", 12, CHEVRON))
            self._controls_collapsed = False
            self.btn_reopen.hide()
        else:
            self._controls_full_height = self.controls.height()
            target = 0
            self.btn_toggle.setIcon(_make_icon("chevron-up", 12, CHEVRON))
            self._controls_collapsed = True
            self.btn_reopen.show(); self.btn_reopen.raise_()
            self._place_reopen_button()
        self.anim = QPropertyAnimation(self.controls, b"maximumHeight")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.controls.height())
        self.anim.setEndValue(target)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim.start()
        if not self._controls_collapsed:
            self._reset_auto_hide()

    def _place_reopen_button(self):
        w = self.stage.width(); h = self.stage.height()
        self.btn_reopen.move(w - 44, h - 44)

    # ---------- Resize & drag ----------
    def _edge_at(self, pos):
        if self._window_folded: return None
        m = self._resize_margin
        r = self.rect()
        x, y = pos.x(), pos.y()
        left, right = x <= m, x >= r.width() - m
        top, bottom = y <= m, y >= r.height() - m
        if top and left: return "NW"
        if top and right: return "NE"
        if bottom and left: return "SW"
        if bottom and right: return "SE"
        if left: return "W"
        if right: return "E"
        if top: return "N"
        if bottom: return "S"
        return None

    def _cursor_for_edge(self, edge):
        return {
            "N": Qt.CursorShape.SizeVerCursor, "S": Qt.CursorShape.SizeVerCursor,
            "E": Qt.CursorShape.SizeHorCursor, "W": Qt.CursorShape.SizeHorCursor,
            "NE": Qt.CursorShape.SizeBDiagCursor, "SW": Qt.CursorShape.SizeBDiagCursor,
            "NW": Qt.CursorShape.SizeFDiagCursor, "SE": Qt.CursorShape.SizeFDiagCursor,
        }.get(edge, Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            edge = self._edge_at(e.position().toPoint())
            if edge:
                self._resize_edge = edge
                self._resize_start_geo = self.geometry()
                self._resize_start_pos = e.globalPosition().toPoint()
                return
            self._drag_pos = e.globalPosition().toPoint()

    def mouseMoveEvent(self, e):
        pos = e.position().toPoint()
        if self._resize_edge and (e.buttons() & Qt.MouseButton.LeftButton):
            delta = e.globalPosition().toPoint() - self._resize_start_pos
            g = self._resize_start_geo
            x, y, w, h = g.x(), g.y(), g.width(), g.height()
            edge = self._resize_edge
            min_w, min_h = self.minimumWidth(), self.minimumHeight()
            if "E" in edge: w = max(min_w, g.width() + delta.x())
            if "S" in edge: h = max(min_h, g.height() + delta.y())
            if "W" in edge:
                new_w = max(min_w, g.width() - delta.x())
                x = g.x() + (g.width() - new_w); w = new_w
            if "N" in edge:
                new_h = max(min_h, g.height() - delta.y())
                y = g.y() + (g.height() - new_h); h = new_h
            self.setGeometry(x, y, w, h)
            return
        edge = self._edge_at(pos)
        self.setCursor(QCursor(self._cursor_for_edge(edge)))
        if self._drag_pos is not None:
            delta = e.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = e.globalPosition().toPoint()
        self._reset_auto_hide()

    def mouseReleaseEvent(self, e):
        self._resize_edge = None
        self._drag_pos = None
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Recentrer viz + overlay sur le widget vidéo
        if hasattr(self, 'video_widget'):
            w = self.video_widget.width()
            h = self.video_widget.height()
            self.viz.setGeometry(0, 0, w, h)
            self.overlay.setGeometry(0, 0, w, h)
        if self.btn_reopen.isVisible():
            self._place_reopen_button()

    def closeEvent(self, event):
        if self.audio_player is not None:
            try: self.audio_player.terminate()
            except Exception: pass
        if self.player is not None:
            try: self.player.terminate()
            except Exception: pass
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Inter", 9))
    w = FranceBleuPlayer()
    w.show()
    sys.exit(app.exec())