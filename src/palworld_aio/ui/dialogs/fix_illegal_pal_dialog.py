from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QFrame
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap
from i18n import t
from palworld_aio import constants
from palworld_aio.widgets.toggle_check import ToggleCheckBtn
from palworld_aio.ui.chrome.styles import DIALOG_STYLE as DARK_THEME_STYLE
from palworld_aio.editor.pal_editor.icons import _get_pal_icon_path, _get_cached_pixmap

class PalRowWidget(QFrame):
    def __init__(self, pal_data, parent=None):
        super().__init__(parent)
        self.pal_data = pal_data
        self._setup_ui()
    def _setup_ui(self):
        self.setStyleSheet('PalRowWidget { background: rgba(255,255,255,0.03); border-radius: 4px; margin: 1px 0; } PalRowWidget:hover { background: rgba(125,211,252,0.06); }')
        row = QHBoxLayout(self)
        row.setContentsMargins(6, 3, 6, 3)
        row.setSpacing(6)
        self.checkbox = ToggleCheckBtn('')
        self.checkbox.setChecked(True)
        self.checkbox.setFixedWidth(20)
        row.addWidget(self.checkbox)
        icon_path = _get_pal_icon_path(self.pal_data.get('cid', ''))
        icon_lbl = QLabel()
        icon_lbl.setFixedSize(22, 22)
        if icon_path:
            pix = _get_cached_pixmap(icon_path, 22)
            if pix and not pix.isNull():
                icon_lbl.setPixmap(pix)
        row.addWidget(icon_lbl)
        name_text = self.pal_data.get('name', 'Unknown')
        nick = self.pal_data.get('nickname', '')
        if nick:
            name_text += f' "{nick}"'
        lvl = self.pal_data.get('level', 1)
        rank = self.pal_data.get('rank', 1)
        stars = rank - 1 if rank > 1 else 0
        info_parts = [f'Lv.{lvl}']
        if stars:
            info_parts.append(f'{stars}★')
        info_text = ' '.join(info_parts)
        ivs = f"IVs {self.pal_data.get('talent_hp', 0)}/{self.pal_data.get('talent_shot', 0)}/{self.pal_data.get('talent_defense', 0)}"
        souls = f"Souls {self.pal_data.get('rank_hp', 0)}/{self.pal_data.get('rank_attack', 0)}/{self.pal_data.get('rank_defense', 0)}/{self.pal_data.get('rank_craftspeed', 0)}"
        detail = f'{info_text} | {ivs} | {souls} | {self.pal_data.get("location", "")}'
        text_w = QWidget()
        text_l = QVBoxLayout(text_w)
        text_l.setContentsMargins(0, 0, 0, 0)
        text_l.setSpacing(1)
        name_lbl = QLabel(name_text)
        name_lbl.setStyleSheet('color: #e2e8f0; font-size: 11px; font-weight: 600;')
        text_l.addWidget(name_lbl)
        detail_lbl = QLabel(detail)
        detail_lbl.setStyleSheet('color: #94a3b8; font-size: 9px;')
        text_l.addWidget(detail_lbl)
        row.addWidget(text_w, 1)
        markers = self.pal_data.get('illegal_markers', [])
        if markers:
            marker_text = '  '.join(markers)
            marker_lbl = QLabel(marker_text)
            marker_lbl.setStyleSheet('color: #fb923c; font-size: 10px; font-weight: 600; padding: 1px 6px; background: rgba(251,146,60,0.12); border-radius: 3px;')
            marker_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row.addWidget(marker_lbl)
    def is_checked(self):
        return self.checkbox.isChecked()
    def set_checked(self, checked):
        self.checkbox.setChecked(checked)

class FixIllegalPalDialog(QDialog):
    def __init__(self, scan_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t('fix_illegal_pal.title') if t else 'Fix Illegal Pals')
        self.setMinimumSize(900, 550)
        self.scan_data = scan_data
        self._player_groups = []
        self._pal_rows = []
        self._setup_ui()
        self._populate_players()
    def _setup_ui(self):
        self.setStyleSheet(DARK_THEME_STYLE)
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        self._header = QLabel(t('fix_illegal_pal.description') if t else 'Select illegal pals to fix:')
        self._header.setStyleSheet('color: #e2e8f0; font-size: 13px; font-weight: 600; padding: 4px 0;')
        layout.addWidget(self._header)
        self.summary_label = QLabel('')
        self.summary_label.setStyleSheet('color: #fbbf24; font-size: 12px; padding: 2px 0;')
        layout.addWidget(self.summary_label)
        btn_row = QHBoxLayout()
        self.select_all_btn = QPushButton(t('player_item.select_all') if t else 'Select All')
        self.select_all_btn.clicked.connect(self._select_all)
        btn_row.addWidget(self.select_all_btn)
        self.deselect_all_btn = QPushButton(t('player_item.deselect_all') if t else 'Deselect All')
        self.deselect_all_btn.clicked.connect(self._deselect_all)
        btn_row.addWidget(self.deselect_all_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('QScrollArea { border: none; background: transparent; }')
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(2)
        scroll.setWidget(self.scroll_content)
        layout.addWidget(scroll, 1)
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet('color: rgba(255,255,255,0.1);')
        layout.addWidget(sep)
        action_row = QHBoxLayout()
        self.fix_btn = QPushButton(t('fix_illegal_pal.fix_selected') if t else 'Fix Selected')
        self.fix_btn.setStyleSheet('QPushButton { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); border-radius: 6px; padding: 8px 24px; font-weight: 600; font-size: 13px; } QPushButton:hover { background: rgba(251,191,36,0.25); border-color: rgba(251,191,36,0.5); color: #FFFFFF; } QPushButton:disabled { background: rgba(100,100,100,0.1); color: #666; border-color: rgba(100,100,100,0.2); }')
        self.fix_btn.setCursor(Qt.PointingHandCursor)
        self.fix_btn.clicked.connect(self._on_fix)
        action_row.addWidget(self.fix_btn)
        action_row.addStretch()
        self._close_btn = QPushButton(t('button.close') if t else 'Close')
        self._close_btn.setStyleSheet('QPushButton { background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.2); border-radius: 6px; padding: 8px 24px; } QPushButton:hover { background: rgba(239,68,68,0.2); }')
        self._close_btn.clicked.connect(self.reject)
        action_row.addWidget(self._close_btn)
        layout.addLayout(action_row)
        self.status_label = QLabel('')
        self.status_label.setStyleSheet('color: #4ade80; font-weight: bold; padding: 5px;')
        layout.addWidget(self.status_label)
    def refresh_labels(self):
        self.setWindowTitle(t('fix_illegal_pal.title') if t else 'Fix Illegal Pals')
        self._header.setText(t('fix_illegal_pal.description') if t else 'Select illegal pals to fix:')
        self.select_all_btn.setText(t('player_item.select_all') if t else 'Select All')
        self.deselect_all_btn.setText(t('player_item.deselect_all') if t else 'Deselect All')
        self.fix_btn.setText(t('fix_illegal_pal.fix_selected') if t else 'Fix Selected')
        self._close_btn.setText(t('button.close') if t else 'Close')
        self._update_summary()
    def _update_summary(self):
        total_players = sum(1 for d in self.scan_data.values() if d['pal_count'] > 0)
        total_illegals = sum(d['pal_count'] for d in self.scan_data.values() if d['pal_count'] > 0)
        self.summary_label.setText(t('fix_illegal_pal.summary').format(players=total_players, pals=total_illegals) if t else f'Found {total_players} player(s) with {total_illegals} illegal pal(s)')
    def _make_player_header(self, uid, data):
        header = QFrame()
        header.setStyleSheet('QFrame { background: rgba(59,130,246,0.08); border-radius: 4px; }')
        hl = QHBoxLayout(header)
        hl.setContentsMargins(8, 4, 8, 4)
        name = data.get('player_name', 'Unknown')
        guild = data.get('guild_name', 'Unknown')
        level = data.get('level', 1)
        count = data['pal_count']
        title = QLabel(f'{name} (Lv.{level}) — {guild}  [{count} illegal]')
        title.setStyleSheet('color: #93c5fd; font-size: 12px; font-weight: 700;')
        hl.addWidget(title, 1)
        sel_all = QPushButton(t('player_item.select_all') if t else 'All')
        sel_all.setFixedHeight(22)
        sel_all.setStyleSheet('QPushButton { background: rgba(74,222,128,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.2); border-radius: 4px; padding: 2px 8px; font-weight: 600; font-size: 9px; } QPushButton:hover { background: rgba(74,222,128,0.2); }')
        sel_all.clicked.connect(lambda: self._set_player_pals(uid, True))
        hl.addWidget(sel_all)
        sel_none = QPushButton(t('player_item.deselect_all') if t else 'None')
        sel_none.setFixedHeight(22)
        sel_none.setStyleSheet('QPushButton { background: rgba(251,113,133,0.12); color: #FB7185; border: 1px solid rgba(251,113,133,0.2); border-radius: 4px; padding: 2px 8px; font-weight: 600; font-size: 9px; } QPushButton:hover { background: rgba(251,113,133,0.2); }')
        sel_none.clicked.connect(lambda: self._set_player_pals(uid, False))
        hl.addWidget(sel_none)
        return header
    def _populate_players(self):
        for i in reversed(range(self.scroll_layout.count())):
            w = self.scroll_layout.itemAt(i).widget()
            if w:
                w.deleteLater()
        self._player_groups = []
        self._pal_rows = []
        total_players = 0
        total_illegals = 0
        for uid_clean, data in sorted(self.scan_data.items(), key=lambda x: x[1].get('player_name', '')):
            if data['pal_count'] <= 0:
                continue
            total_players += 1
            total_illegals += data['pal_count']
            header = self._make_player_header(uid_clean, data)
            self.scroll_layout.addWidget(header)
            self._player_groups.append((uid_clean, []))
            for pal in data.get('illegals', []):
                row = PalRowWidget(pal)
                self.scroll_layout.addWidget(row)
                self._pal_rows.append(row)
                self._player_groups[-1][1].append(row)
        self.scroll_layout.addStretch(1)
        self._update_summary()
        if total_players > 0:
            self.select_all_btn.setEnabled(True)
            self.deselect_all_btn.setEnabled(True)
            self.fix_btn.setEnabled(True)
    def _set_player_pals(self, uid, checked):
        for g_uid, rows in self._player_groups:
            if g_uid == uid:
                for r in rows:
                    r.set_checked(checked)
                break
        self._update_fix_btn()
    def _update_fix_btn(self):
        any_checked = any(r.is_checked() for r in self._pal_rows)
        self.fix_btn.setEnabled(any_checked)
    def _select_all(self):
        for r in self._pal_rows:
            r.set_checked(True)
        self.fix_btn.setEnabled(True)
    def _deselect_all(self):
        for r in self._pal_rows:
            r.set_checked(False)
        self.fix_btn.setEnabled(False)
    def _get_selected_uids(self):
        uids = set()
        for g_uid, rows in self._player_groups:
            if any(r.is_checked() for r in rows):
                uids.add(g_uid)
        return list(uids)
    def _on_fix(self):
        uids = self._get_selected_uids()
        if not uids:
            self.status_label.setText(t('fix_illegal_pal.no_selection') if t else 'No players selected.')
            self.status_label.setStyleSheet('color: #ef4444; font-weight: bold; padding: 5px;')
            return
        self.accept()
