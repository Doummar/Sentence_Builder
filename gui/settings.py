# -*- coding: utf-8 -*-
"""
Sentence Builder - Settings & Guide Dialog (Qt6 / PyQt6 for Anki 23.10+ / 24.x / 25.x / 26+)
Matches Anki's native theme (Light / Dark) with standard system QFontComboBox.
"""

from typing import Optional, Dict, Any
from aqt import mw
from aqt.qt import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFormLayout,
    QDialogButtonBox,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QFontComboBox,
    QFont,
    QSpinBox,
    QLineEdit,
    QColorDialog,
    QTabWidget,
    QWidget,
    QFrame,
    QGroupBox,
    Qt,
    QCursor,
    QColor,
    QDesktopServices,
    QUrl,
)
from aqt.utils import tooltip

# Default configuration fallback
DEFAULT_CONFIG: Dict[str, Any] = {
    "enabled": True,
    "card_position": "top",
    "horizontal_alignment": "center",
    "controls_position": "top_right",
    "line_width": 520,
    "font_family": "Arial",
    "font_size": 18,
    "image_size": "medium",
    "correct_color": "#22c55e",
    "wrong_color": "#ef4444",
    "custom_colors_enabled": True,
    "auto_reveal_back": True,
    "show_check_button": False,
    "version": "1.0.0",
}


def is_night_mode() -> bool:
    """Detects whether Anki is currently in Dark/Night mode across all Anki versions (2.1.20 - 25.x+)."""
    # Method 1: aqt.theme.theme_manager (Anki 2.1.50+ / 23.x / 24.x / 25.x)
    try:
        from aqt.theme import theme_manager
        if hasattr(theme_manager, "night_mode"):
            nm = theme_manager.night_mode
            return bool(nm() if callable(nm) else nm)
        if hasattr(theme_manager, "get_night_mode"):
            return bool(theme_manager.get_night_mode())
    except Exception:
        pass

    # Method 2: ProfileManager on main window mw.pm.night_mode()
    try:
        from aqt import mw
        if mw and hasattr(mw, "pm") and mw.pm and hasattr(mw.pm, "night_mode"):
            nm = mw.pm.night_mode
            return bool(nm() if callable(nm) else nm)
    except Exception:
        pass

    # Method 3: aqt.theme.is_dark helper
    try:
        import aqt.theme
        if hasattr(aqt.theme, "is_dark") and callable(aqt.theme.is_dark):
            return bool(aqt.theme.is_dark())
    except Exception:
        pass

    # Method 4: Inspect active Qt application window palette luminance
    try:
        from aqt.qt import QApplication, QPalette
        app = QApplication.instance()
        if app:
            bg = app.palette().color(QPalette.ColorRole.Window)
            luminance = (bg.red() * 0.299 + bg.green() * 0.587 + bg.blue() * 0.114)
            return luminance < 128
    except Exception:
        pass

    return False


def get_dialog_stylesheet(dark_mode: bool) -> str:
    """Returns empty string so dialog uses Anki's native Qt palette and theme directly."""
    return ""


class SentenceBuilderSettingsDialog(QDialog):
    """Native Qt6 Settings dialog for Sentence Builder add-on matching Anki's theme."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Sentence Builder Settings")
        self.setMinimumSize(500, 420)
        self.resize(520, 440)
        # Use native Qt styling so it automatically matches Anki's light and dark mode.
        # Do not force custom dark colors or custom backgrounds.

        # Load existing config or defaults
        self.config: Dict[str, Any] = self._load_config()

        # Silently trigger note type validation and legacy field cleanup
        if mw and mw.col:
            try:
                from ..model_manager import ensure_sentence_builder_note_type
                ensure_sentence_builder_note_type(overwrite_templates=True)
            except Exception:
                pass

        # Build UI components
        self._init_ui()
        self._populate_fields()

    def _load_config(self) -> Dict[str, Any]:
        """Loads configuration safely from Anki Addon Manager or defaults."""
        config = DEFAULT_CONFIG.copy()
        if mw and hasattr(mw, "addonManager"):
            saved = mw.addonManager.getConfig(__name__.split(".")[0])
            if saved and isinstance(saved, dict):
                config.update(saved)
        return config

    def _save_config(self, new_config: Dict[str, Any]) -> None:
        """Writes configuration to Anki Addon Manager."""
        if mw and hasattr(mw, "addonManager"):
            addon_pkg = __name__.split(".")[0]
            mw.addonManager.writeConfig(addon_pkg, new_config)
            tooltip("Sentence Builder: Settings saved successfully!", period=2000)

            # Trigger webview refresh on active reviewer if present
            if mw.reviewer and hasattr(mw.reviewer, "card") and mw.reviewer.card:
                try:
                    mw.reviewer.card.load()
                except Exception:
                    mw.reset()

    def _init_ui(self) -> None:
        """Constructs native layout, tabs, and symmetrically aligned bottom action buttons."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(12)

        # Tab Widget
        self.tabs = QTabWidget(self)

        # 1. General Tab
        self.tab_general = QWidget()
        self._build_general_tab()
        self.tabs.addTab(self.tab_general, "General")

        # 2. Behavior Tab
        self.tab_behavior = QWidget()
        self._build_behavior_tab()
        self.tabs.addTab(self.tab_behavior, "Behavior")

        main_layout.addWidget(self.tabs)

        # Native Anki QDialogButtonBox: Help and Restore Defaults on the left, Save and Cancel on the right
        self.button_box = QDialogButtonBox(self)
        self.btn_help = self.button_box.addButton(QDialogButtonBox.StandardButton.Help)
        self.btn_restore = self.button_box.addButton("Restore Defaults", QDialogButtonBox.ButtonRole.ResetRole)
        self.btn_cancel = self.button_box.addButton(QDialogButtonBox.StandardButton.Cancel)
        self.btn_save = self.button_box.addButton(QDialogButtonBox.StandardButton.Save)
        self.btn_save.setDefault(True)

        self.btn_restore.clicked.connect(self._on_reset_defaults)
        self.button_box.helpRequested.connect(self._on_open_user_guide)
        self.button_box.rejected.connect(self.reject)
        self.button_box.accepted.connect(self._on_save)

        main_layout.addWidget(self.button_box)

    # -------------------------------------------------------------
    # Tab 1: General (Display & Typography)
    # -------------------------------------------------------------
    def _build_general_tab(self) -> None:
        form = QFormLayout(self.tab_general)
        form.setContentsMargins(36, 22, 36, 22)
        form.setVerticalSpacing(16)
        form.setHorizontalSpacing(18)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        if hasattr(QFormLayout, "FieldGrowthPolicy") and hasattr(QFormLayout.FieldGrowthPolicy, "FieldsStayAtSizeHint"):
            form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)

        label_width = 170
        control_width = 240

        def add_row(label_text: str, widget: QWidget) -> None:
            lbl = QLabel(label_text, self.tab_general)
            lbl.setFixedWidth(label_width)
            lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            widget.setFixedWidth(control_width)
            form.addRow(lbl, widget)

        # 1. Vertical Position (Top / Center / Bottom)
        self.combo_position = QComboBox(self.tab_general)
        self.combo_position.addItems(["Top (Default)", "Center", "Bottom"])
        add_row("Vertical Position:", self.combo_position)

        # 2. Horizontal Alignment (Left / Center / Right)
        self.combo_h_align = QComboBox(self.tab_general)
        self.combo_h_align.addItems(["Center (Default)", "Left", "Right"])
        add_row("Horizontal Alignment:", self.combo_h_align)

        # 3. Controls Position (Top Right / Top Left / Bottom Right / Bottom Left)
        self.combo_ctrl_pos = QComboBox(self.tab_general)
        self.combo_ctrl_pos.addItems([
            "Top Right (Default)",
            "Top Left",
            "Bottom Right",
            "Bottom Left",
        ])
        add_row("Controls Position:", self.combo_ctrl_pos)

        # 4. Line Width (px)
        self.spin_line_width = QSpinBox(self.tab_general)
        self.spin_line_width.setRange(400, 1200)
        self.spin_line_width.setSingleStep(10)
        self.spin_line_width.setValue(520)
        self.spin_line_width.setSuffix(" px")
        add_row("Line Width (px):", self.spin_line_width)

        # 5. Font Family (QFontComboBox with system fonts)
        self.font_combo = QFontComboBox(self.tab_general)
        add_row("Font family:", self.font_combo)

        # 6. Font Size (px)
        self.spin_font_size = QSpinBox(self.tab_general)
        self.spin_font_size.setRange(12, 48)
        self.spin_font_size.setValue(18)
        self.spin_font_size.setSuffix(" px")
        add_row("Font size (px):", self.spin_font_size)

        # 7. Image Size
        self.combo_img_size = QComboBox(self.tab_general)
        self.combo_img_size.addItems([
            "Medium (Default - 680px)",
            "Small (480px)",
            "Large (880px)",
            "Extra Large (1160px)",
        ])
        add_row("Image Size:", self.combo_img_size)

    # -------------------------------------------------------------
    # Tab 2: Behavior (Interaction & Automation)
    # -------------------------------------------------------------
    def _build_behavior_tab(self) -> None:
        form = QFormLayout(self.tab_behavior)
        form.setContentsMargins(36, 22, 36, 22)
        form.setVerticalSpacing(18)
        form.setHorizontalSpacing(18)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        if hasattr(QFormLayout, "FieldGrowthPolicy") and hasattr(QFormLayout.FieldGrowthPolicy, "FieldsStayAtSizeHint"):
            form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)

        label_width = 170

        # 8. Show Check Button
        lbl_check = QLabel("Check Button:", self.tab_behavior)
        lbl_check.setFixedWidth(label_width)
        lbl_check.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.chk_show_check = QCheckBox("Show manual Check button on front card", self.tab_behavior)
        self.chk_show_check.setToolTip("Displays a Check button to manually test placed words before flipping.")
        form.addRow(lbl_check, self.chk_show_check)

        # 9. Auto-reveal Back Card on completion
        lbl_reveal = QLabel("Answer Reveal:", self.tab_behavior)
        lbl_reveal.setFixedWidth(label_width)
        lbl_reveal.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.chk_autoreveal = QCheckBox("Automatically flip to back when all words are placed", self.tab_behavior)
        self.chk_autoreveal.setToolTip("Automatically shows the answer and feedback once all word tiles are placed.")
        form.addRow(lbl_reveal, self.chk_autoreveal)

    # -------------------------------------------------------------
    # Tab 3: Support & Quick Guide
    # -------------------------------------------------------------
    def _build_support_tab(self) -> None:
        layout = QVBoxLayout(self.tab_support)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # Clean quick guide box
        help_box = QLabel(
            "<b>Sentence Builder Quick Help</b><br><br>"
            "• <b>What it does:</b> Turns sentences into interactive word puzzles. Drag or tap words to assemble the sentence. Flip to see right (green) and wrong (red) words.<br>"
            "• <b>How to use:</b> Drag or tap words into the answer box. Tap words in the box to return them. Flip to check.<br>"
            "• <b>Settings:</b> Change vertical position, alignment, line width, font, check button, and auto-reveal in the General & Behavior tabs.<br>"
            "• <b>Images:</b> Tap the 📷 button to toggle hint pictures without spoiling the answer.",
            self.tab_support,
        )
        help_box.setWordWrap(True)
        help_box.setStyleSheet("font-size: 12px; line-height: 1.4;")
        layout.addWidget(help_box)

        layout.addSpacing(6)

        # Button 1: Open Full User Guide...
        btn_guide = QPushButton("Open Full User Guide...", self.tab_support)
        btn_guide.setProperty("class", "actionButton")
        btn_guide.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_guide.clicked.connect(self._on_open_user_guide)
        layout.addWidget(btn_guide)

        # Button 2: Report an Issue (GitHub)...
        btn_issue = QPushButton("Report an Issue (GitHub)...", self.tab_support)
        btn_issue.setProperty("class", "actionButton")
        btn_issue.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_issue.clicked.connect(self._on_report_issue)
        layout.addWidget(btn_issue)

        # Button 3: Restore Defaults
        btn_restore = QPushButton("Restore Defaults", self.tab_support)
        btn_restore.setProperty("class", "actionButton")
        btn_restore.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_restore.clicked.connect(self._on_reset_defaults)
        layout.addWidget(btn_restore)

        layout.addStretch()

    def _on_open_user_guide(self) -> None:
        """Opens the standalone User Guide dialog."""
        open_guide_dialog(parent_dialog=self)

    # -------------------------------------------------------------
    # Logic & Event Handlers
    # -------------------------------------------------------------
    def _populate_fields(self) -> None:
        """Populates UI widgets from current config."""
        pos = self.config.get("card_position", "top").lower()
        if pos == "center":
            self.combo_position.setCurrentIndex(1)
        elif pos == "bottom":
            self.combo_position.setCurrentIndex(2)
        else:
            self.combo_position.setCurrentIndex(0)  # Top (Default)

        h_align = self.config.get("horizontal_alignment", "center").lower()
        if h_align == "left":
            self.combo_h_align.setCurrentIndex(1)
        elif h_align == "right":
            self.combo_h_align.setCurrentIndex(2)
        else:
            self.combo_h_align.setCurrentIndex(0)  # Center (Default)

        ctrl_pos = str(self.config.get("controls_position", "top_right")).lower()
        if ctrl_pos == "top_left":
            self.combo_ctrl_pos.setCurrentIndex(1)
        elif ctrl_pos == "bottom_right":
            self.combo_ctrl_pos.setCurrentIndex(2)
        elif ctrl_pos == "bottom_left":
            self.combo_ctrl_pos.setCurrentIndex(3)
        else:
            self.combo_ctrl_pos.setCurrentIndex(0)  # Top Right (Default)

        self.spin_line_width.setValue(int(self.config.get("line_width", 520)))

        saved_font = str(self.config.get("font_family", DEFAULT_CONFIG["font_family"]))
        self.font_combo.setCurrentFont(QFont(saved_font))

        self.spin_font_size.setValue(int(self.config.get("font_size", 18)))

        img_size = str(self.config.get("image_size", "medium")).lower().strip()
        if img_size == "small":
            self.combo_img_size.setCurrentIndex(1)
        elif img_size == "large":
            self.combo_img_size.setCurrentIndex(2)
        elif img_size in ("extra_large", "extra large", "extralarge"):
            self.combo_img_size.setCurrentIndex(3)
        else:
            self.combo_img_size.setCurrentIndex(0)  # Medium (Default)

        self.chk_autoreveal.setChecked(bool(self.config.get("auto_reveal_back", True)))
        self.chk_show_check.setChecked(bool(self.config.get("show_check_button", False)))

    def _on_save(self) -> None:
        """Collects values and saves configuration."""
        pos_idx = self.combo_position.currentIndex()
        position_map = {0: "top", 1: "center", 2: "bottom"}
        selected_pos = position_map.get(pos_idx, "top")

        h_align_idx = self.combo_h_align.currentIndex()
        h_align_map = {0: "center", 1: "left", 2: "right"}
        selected_h_align = h_align_map.get(h_align_idx, "center")

        ctrl_pos_idx = self.combo_ctrl_pos.currentIndex()
        ctrl_pos_map = {0: "top_right", 1: "top_left", 2: "bottom_right", 3: "bottom_left"}
        selected_ctrl_pos = ctrl_pos_map.get(ctrl_pos_idx, "top_right")

        selected_font = self.font_combo.currentFont().family()

        img_size_idx = self.combo_img_size.currentIndex()
        img_size_map = {0: "medium", 1: "small", 2: "large", 3: "extra_large"}
        selected_img_size = img_size_map.get(img_size_idx, "medium")

        new_config = {
            "enabled": True,
            "card_position": selected_pos,
            "horizontal_alignment": selected_h_align,
            "controls_position": selected_ctrl_pos,
            "line_width": self.spin_line_width.value(),
            "font_family": selected_font or DEFAULT_CONFIG["font_family"],
            "font_size": self.spin_font_size.value(),
            "image_size": selected_img_size,
            "auto_reveal_back": self.chk_autoreveal.isChecked(),
            "show_check_button": self.chk_show_check.isChecked(),
            "custom_colors_enabled": bool(self.config.get("custom_colors_enabled", True)),
            "correct_color": self.config.get("correct_color", "#22c55e"),
            "wrong_color": self.config.get("wrong_color", "#ef4444"),
            "version": self.config.get("version", "1.0.0"),
        }

        self._save_config(new_config)
        self.accept()

    def _on_reset_defaults(self) -> None:
        """Resets inputs to default settings."""
        self.config = DEFAULT_CONFIG.copy()
        self._populate_fields()
        tooltip("Sentence Builder: Reset to default values.", period=1500)

    def _on_report_issue(self) -> None:
        """Opens issue tracker."""
        QDesktopServices.openUrl(QUrl("https://github.com/Doummar/Sentence_Builder/issues"))


class SentenceBuilderGuideDialog(QDialog):
    """Dedicated native Guide Dialog with clean, simple, and friendly help."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Sentence Builder — Help & Guide")
        self.setMinimumSize(480, 440)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(12)

        # Content frame with native background
        content_frame = QFrame(self)
        content_frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame_layout = QVBoxLayout(content_frame)
        frame_layout.setContentsMargins(14, 14, 14, 14)
        frame_layout.setSpacing(12)

        # Section 1: What the add-on does
        lbl_what = QLabel("What the add-on does", content_frame)
        lbl_what.setStyleSheet("font-weight: 600; font-size: 13px;")
        frame_layout.addWidget(lbl_what)

        lbl_what_bullets = QLabel(
            "\n".join([
                "• Turns sentences into interactive word-ordering puzzle cards.",
                "• Words are split into tiles to drag or click into place.",
                "• Flipping reveals instant feedback: correct words turn green, incorrect turn red.",
            ]),
            content_frame,
        )
        lbl_what_bullets.setWordWrap(True)
        lbl_what_bullets.setStyleSheet("font-size: 12px;")
        frame_layout.addWidget(lbl_what_bullets)

        # Section 2: How to use it
        lbl_how = QLabel("How to use it", content_frame)
        lbl_how.setStyleSheet("font-weight: 600; font-size: 13px;")
        frame_layout.addWidget(lbl_how)

        lbl_how_bullets = QLabel(
            "\n".join([
                "• Place words: Drag tiles or click them to move them into the answer box.",
                "• Remove words: Click any word inside the answer box to send it back.",
                "• Rearrange: Drag words within the answer box to swap positions.",
                "• Check answer: Flip the card to check, or use the optional Check button.",
            ]),
            content_frame,
        )
        lbl_how_bullets.setWordWrap(True)
        lbl_how_bullets.setStyleSheet("font-size: 12px;")
        frame_layout.addWidget(lbl_how_bullets)

        # Section 3: Main settings
        lbl_set = QLabel("Main settings", content_frame)
        lbl_set.setStyleSheet("font-weight: 600; font-size: 13px;")
        frame_layout.addWidget(lbl_set)

        lbl_set_bullets = QLabel(
            "\n".join([
                "• Controls Position: Place Audio & Image buttons in any of the four corners.",
                "• Card Layout: Customize vertical position, horizontal alignment, and line width.",
                "• Typography: Select your preferred font family and font size.",
                "• Behavior: Enable the manual Check button or automatic flip when complete.",
            ]),
            content_frame,
        )
        lbl_set_bullets.setWordWrap(True)
        lbl_set_bullets.setStyleSheet("font-size: 12px;")
        frame_layout.addWidget(lbl_set_bullets)

        # Section 4: How images work
        lbl_img = QLabel("How images work", content_frame)
        lbl_img.setStyleSheet("font-weight: 600; font-size: 13px;")
        frame_layout.addWidget(lbl_img)

        lbl_img_bullets = QLabel(
            "\n".join([
                "• Toggle hints: Click the camera icon (📷) to reveal hint pictures without spoilers.",
                "• Front & Back: Show images directly on the card or keep them behind the toggle button.",
            ]),
            content_frame,
        )
        lbl_img_bullets.setWordWrap(True)
        lbl_img_bullets.setStyleSheet("font-size: 12px;")
        frame_layout.addWidget(lbl_img_bullets)

        main_layout.addWidget(content_frame)

        # Bottom Action Buttons
        btn_row = QHBoxLayout()
        btn_open_settings = QPushButton("Open Settings", self)
        btn_open_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_open_settings.clicked.connect(self._open_settings_and_close)
        btn_row.addWidget(btn_open_settings)

        btn_report = QPushButton("Report an Issue", self)
        btn_report.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_report.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/Doummar/Sentence_Builder/issues")))
        btn_row.addWidget(btn_report)

        btn_row.addStretch()

        btn_close = QPushButton("Close", self)
        btn_close.setDefault(True)
        btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_close.clicked.connect(self._on_close)
        btn_row.addWidget(btn_close)

        main_layout.addLayout(btn_row)

    def reject(self) -> None:
        """Handles dialog rejection (Escape key, window close button)."""
        super().reject()
        self._bring_settings_to_front(create_if_missing=False)

    def _on_close(self) -> None:
        """Closes the Guide dialog immediately on first click and returns to caller Settings panel if open."""
        self.accept()
        self._bring_settings_to_front(create_if_missing=False)

    def _open_settings_and_close(self) -> None:
        """Closes guide dialog and switches to or opens settings dialog without duplicating."""
        self.accept()
        self._bring_settings_to_front(target_tab=0, create_if_missing=True)

    def _bring_settings_to_front(self, target_tab: Optional[int] = None, create_if_missing: bool = False) -> None:
        """Ensures the caller or active settings dialog stays open, comes to the front, and is activated."""
        global _settings_dialog_instance
        parent = self.parent()
        target = None
        if parent and isinstance(parent, QWidget) and hasattr(parent, "isVisible") and parent.isVisible():
            target = parent
        elif _settings_dialog_instance is not None and _settings_dialog_instance.isVisible():
            target = _settings_dialog_instance

        if target is not None:
            try:
                if target_tab is not None and hasattr(target, "tabs"):
                    target.tabs.setCurrentIndex(target_tab)
                target.show()
                target.raise_()
                target.activateWindow()
            except Exception:
                pass
        elif create_if_missing:
            open_settings_dialog(target_tab=target_tab or 0)


_settings_dialog_instance: Optional["SentenceBuilderSettingsDialog"] = None
_guide_dialog_instance: Optional["SentenceBuilderGuideDialog"] = None
_last_guide_open_timestamp: float = 0.0


def open_settings_dialog(target_tab: int = 0) -> None:
    """Helper entry-point function to display or bring to front the settings dialog without creating duplicates."""
    global _settings_dialog_instance
    if _settings_dialog_instance is not None and _settings_dialog_instance.isVisible():
        _settings_dialog_instance.tabs.setCurrentIndex(target_tab)
        _settings_dialog_instance.show()
        _settings_dialog_instance.raise_()
        _settings_dialog_instance.activateWindow()
        return

    parent = mw if mw else None
    dialog = SentenceBuilderSettingsDialog(parent)
    _settings_dialog_instance = dialog
    dialog.tabs.setCurrentIndex(target_tab)
    dialog.exec()
    _settings_dialog_instance = None


def open_guide_dialog(parent_dialog: Optional[QWidget] = None) -> None:
    """Helper entry-point function to display the guide dialog without creating duplicates."""
    global _guide_dialog_instance, _settings_dialog_instance, _last_guide_open_timestamp
    import time

    # Debounce guard: prevent duplicate signals or rapid clicks from queueing a second dialog
    now = time.time()
    if now - _last_guide_open_timestamp < 0.6:
        if _guide_dialog_instance is not None and _guide_dialog_instance.isVisible():
            _guide_dialog_instance.raise_()
            _guide_dialog_instance.activateWindow()
        return
    _last_guide_open_timestamp = now

    if _guide_dialog_instance is not None and _guide_dialog_instance.isVisible():
        _guide_dialog_instance.raise_()
        _guide_dialog_instance.activateWindow()
        return

    # Determine parent: prioritize explicit parent_dialog, then active settings instance, then mw
    parent = parent_dialog
    if parent is None and _settings_dialog_instance is not None and _settings_dialog_instance.isVisible():
        parent = _settings_dialog_instance
    if parent is None and mw:
        parent = mw

    dialog = SentenceBuilderGuideDialog(parent)
    _guide_dialog_instance = dialog
    dialog.exec()
    _guide_dialog_instance = None

    # After Guide dialog closes, ensure caller/parent Settings dialog stays open and comes back to front
    target = parent if (parent and isinstance(parent, QWidget)) else _settings_dialog_instance
    if target is not None and hasattr(target, "isVisible") and target.isVisible():
        try:
            target.show()
            target.raise_()
            target.activateWindow()
        except Exception:
            pass
