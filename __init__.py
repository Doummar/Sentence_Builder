# -*- coding: utf-8 -*-
"""
Sentence Builder (SB) - Anki Desktop Add-on
--------------------------------------------
Minimalist, high-performance Anki desktop add-on (Python + Qt6 / PyQt6).
Injects CSS custom properties and positioning classes ONLY for interactive Sentence Builder note types.
Strictly isolated: NEVER injects CSS into or modifies other note types in the collection.

Author: Anki Add-on Community
License: MIT
Compatibility: Anki 23.10+, 24.x, 25.x, 26+
"""

import sys
from typing import Dict, Any

from aqt import mw, gui_hooks
from aqt.qt import QAction
from aqt.webview import AnkiWebView, WebContent

from .gui.settings import open_settings_dialog, DEFAULT_CONFIG
from .model_manager import ensure_sentence_builder_note_type

# Ensure desktop execution only
IS_DESKTOP: bool = not any(
    mod in sys.modules for mod in ["ankidroid", "anki_mobile"]
)


def get_config() -> Dict[str, Any]:
    """Retrieves addon configuration with safe fallbacks."""
    config = DEFAULT_CONFIG.copy()
    if mw and hasattr(mw, "addonManager"):
        saved = mw.addonManager.getConfig(__name__)
        if saved and isinstance(saved, dict):
            config.update(saved)
    return config


def generate_injected_css(cfg: Dict[str, Any]) -> str:
    """
    Generates CSS rules strictly scoped to Sentence Builder.
    .sb-card is the only element receiving the position and alignment rules.
    """
    enabled = cfg.get("enabled", True)
    if not enabled:
        return ""

    pos = str(cfg.get("card_position", "top")).lower().strip()
    h_align = str(cfg.get("horizontal_alignment", "center")).lower().strip()
    
    raw_line_width = cfg.get("line_width", 520)
    try:
        line_width = int(raw_line_width)
    except (ValueError, TypeError):
        line_width = 520
    line_width = max(400, min(1200, line_width))

    font_family = cfg.get("font_family", DEFAULT_CONFIG["font_family"])
    font_size = int(cfg.get("font_size", 18))
    
    # Image Size presets (Medium default: 680x340px, Small: 480x240px, Large: 880x440px, Extra Large: 1160x580px)
    raw_img_size = str(cfg.get("image_size", "medium")).lower().strip()
    if raw_img_size == "small":
        img_max_width = 480
        img_max_height = 240
    elif raw_img_size == "large":
        img_max_width = 880
        img_max_height = 440
    elif raw_img_size in ("extra_large", "extra large", "extralarge"):
        img_max_width = 1160
        img_max_height = 580
    else:  # "medium" (default)
        img_max_width = 680
        img_max_height = 340

    # Controls Position (Audio & Image button placement)
    raw_ctrl_pos = str(cfg.get("controls_position", "top_right")).lower().strip()
    if raw_ctrl_pos == "top_left":
        ctrl_top = "14px"
        ctrl_bottom = "auto"
        ctrl_left = "14px"
        ctrl_right = "auto"
        ctrl_align = "flex-start"
    elif raw_ctrl_pos == "bottom_right":
        ctrl_top = "auto"
        ctrl_bottom = "14px"
        ctrl_left = "auto"
        ctrl_right = "14px"
        ctrl_align = "flex-end"
    elif raw_ctrl_pos == "bottom_left":
        ctrl_top = "auto"
        ctrl_bottom = "14px"
        ctrl_left = "14px"
        ctrl_right = "auto"
        ctrl_align = "flex-start"
    else:  # "top_right" (default)
        ctrl_top = "14px"
        ctrl_bottom = "auto"
        ctrl_left = "auto"
        ctrl_right = "14px"
        ctrl_align = "flex-end"

    use_custom_colors = cfg.get("custom_colors_enabled", True)
    correct_color = cfg.get("correct_color", "#22c55e") if use_custom_colors else "#22c55e"
    wrong_color = cfg.get("wrong_color", "#ef4444") if use_custom_colors else "#ef4444"
    show_check = cfg.get("show_check_button", False)
    check_btn_display = "inline-flex" if show_check else "none"

    # Vertical position rules - applies cleanly to the entire card content group
    if pos == "top":
        v_rules = "justify-content: flex-start !important; padding-top: 20px !important; padding-bottom: 24px !important;"
    elif pos == "bottom":
        v_rules = "justify-content: flex-end !important; padding-top: 16px !important; padding-bottom: 24px !important;"
    else:  # "center" (default)
        v_rules = "justify-content: center !important; padding-top: 16px !important; padding-bottom: 16px !important;"

    # Horizontal alignment rules
    if h_align == "left":
        h_rules = "align-items: flex-start !important; padding-left: 28px !important;"
        text_align_rule = "text-align: left !important;"
        h_justify_rule = "justify-content: flex-start !important;"
    elif h_align == "right":
        h_rules = "align-items: flex-end !important; padding-right: 28px !important;"
        text_align_rule = "text-align: right !important;"
        h_justify_rule = "justify-content: flex-end !important;"
    else:  # "center" (default)
        h_rules = "align-items: center !important;"
        text_align_rule = "text-align: center !important;"
        h_justify_rule = "justify-content: center !important;"

    return f"""
    /* --- Sentence Builder Scoped Properties --- */
    .sb-card {{
        display: flex !important;
        flex-direction: column !important;
        min-height: 100vh !important;
        width: 100% !important;
        box-sizing: border-box !important;
        {v_rules}
        {h_rules}
        
        --sb-line-width: {line_width}px;
        --sb-font-family: {font_family};
        --sb-font-size: {font_size}px;
        --sb-img-max-width: {img_max_width}px;
        --sb-img-max-height: {img_max_height}px;
        --sb-ctrl-top: {ctrl_top};
        --sb-ctrl-bottom: {ctrl_bottom};
        --sb-ctrl-left: {ctrl_left};
        --sb-ctrl-right: {ctrl_right};
        --sb-ctrl-align: {ctrl_align};
        --sb-correct-color: {correct_color};
        --sb-wrong-color: {wrong_color};
        --sb-check-btn-display: {check_btn_display};
        --sb-anki-success: var(--color-success, var(--success, var(--ans-good, #28a745)));
        --sb-anki-error: var(--color-danger, var(--color-error, var(--danger, var(--error, var(--ans-again, #dc2626)))));
        --sb-text: #1f2937;
    }}

    .nightMode .sb-card,
    .night_mode .sb-card,
    .sb-card.nightMode,
    body.nightMode .sb-card,
    body.night_mode .sb-card {{
        --sb-anki-success: var(--color-success, var(--success, var(--ans-good, #2ecc71)));
        --sb-anki-error: var(--color-danger, var(--color-error, var(--danger, var(--error, var(--ans-again, #ff6b6b)))));
        --sb-text: #f4f4f5;
    }}

    .sb-card .main,
    .sb-card > .main {{
        display: flex !important;
        flex-direction: column !important;
        align-items: inherit !important;
        justify-content: inherit !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
        position: relative !important;
    }}

    .sb-card .sb-prompt,
    .sb-card #sb-interactive-block,
    .sb-card .sb-back-block,
    .sb-card .sb-user-attempt,
    .sb-card #sb-sandbox,
    .sb-card .sb-attempt-tiles,
    .sb-card #sb-word-bank,
    .sb-card .sb-solution,
    .sb-card .sb-explanation {{
        width: var(--sb-line-width, {line_width}px) !important;
        min-width: var(--sb-line-width, {line_width}px) !important;
        max-width: var(--sb-line-width, {line_width}px) !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        box-sizing: border-box !important;
        flex-shrink: 0 !important;
        flex-grow: 0 !important;
    }}

    .sb-card .sb-prompt {{
        font-family: var(--sb-font-family, {font_family}) !important;
        font-size: 1.25rem !important;
        font-weight: normal !important;
        margin: 0 0 12px 0 !important;
        padding: 0 !important;
        line-height: 1.45 !important;
        {text_align_rule}
        word-break: normal !important;
        overflow-wrap: break-word !important;
    }}

    .sb-card #sb-interactive-block,
    .sb-card .sb-back-block {{
        min-height: 280px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: inherit !important;
        margin: 0 !important;
    }}

    .sb-card #sb-sandbox {{
        height: 140px !important;
        min-height: 140px !important;
        max-height: 140px !important;
        margin: 0 !important;
        overflow: hidden !important;
        background: var(--sb-box-bg);
        border: 2px dashed var(--sb-box-border);
        border-radius: 12px;
        padding: 12px 14px !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        align-content: center !important;
        {h_justify_rule}
        gap: 8px !important;
    }}

    .sb-card .sb-attempt-tiles {{
        min-height: 40px !important;
        height: auto !important;
        max-height: none !important;
        margin: 0 !important;
        background: transparent !important;
        border: none !important;
        padding: 4px 0 !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        align-content: center !important;
        {h_justify_rule}
        gap: 8px !important;
    }}

    .sb-card .sb-divider {{
        border: 0 !important;
        border-top: 1px solid rgba(128, 128, 128, 0.2) !important;
        margin: 12px 0 !important;
        width: 100% !important;
    }}

    .sb-card #sb-word-bank {{
        height: 84px !important;
        min-height: 84px !important;
        max-height: 84px !important;
        margin: 12px 0 0 0 !important;
        overflow: hidden !important;
        padding: 8px 12px !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        align-content: center !important;
        {h_justify_rule}
        gap: 8px !important;
    }}

    .sb-card .sb-actions {{
        display: flex !important;
        align-items: center !important;
        {h_justify_rule}
        gap: 10px !important;
        margin: 12px 0 0 0 !important;
        height: 32px !important;
        min-height: 32px !important;
        max-height: 32px !important;
        flex-shrink: 0 !important;
        flex-grow: 0 !important;
    }}

    .sb-card .sb-solution {{
        margin: 12px 0 0 0 !important;
        padding: 0 !important;
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        display: block !important;
        {text_align_rule}
        color: var(--sb-text) !important;
        font-weight: 400 !important;
        font-size: 1.25rem !important;
        line-height: 1.45 !important;
    }}

    .sb-card .sb-solution b,
    .sb-card .sb-solution strong,
    .sb-card .sb-solution .sb-word-wrong {{
        font-weight: 700 !important;
    }}

    .sb-card .sb-solution .sb-word-normal {{
        font-weight: 400 !important;
    }}

    .sb-card .sb-explanation {{
        display: flex !important;
        flex-direction: column !important;
        align-items: inherit !important;
        margin: 14px 0 0 0 !important;
    }}

    /* Fixed Control Bar (.ctrl) - strictly scoped to .sb-card */
    .sb-card .ctrl {{
        position: fixed !important;
        top: var(--sb-ctrl-top, {ctrl_top}) !important;
        bottom: var(--sb-ctrl-bottom, {ctrl_bottom}) !important;
        left: var(--sb-ctrl-left, {ctrl_left}) !important;
        right: var(--sb-ctrl-right, {ctrl_right}) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: var(--sb-ctrl-align, {ctrl_align}) !important;
        gap: 4px !important;
        z-index: 100 !important;
    }}

    /* Button Style (.ibtn) - strictly scoped to .sb-card */
    .sb-card .ibtn {{
        min-width: auto !important;
        height: 22px !important;
        padding: 0 6px !important;
        border-radius: 5px !important;
        border: none !important;
        background: transparent !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-family: inherit !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        color: #aaa !important;
        white-space: nowrap !important;
        line-height: 1 !important;
        opacity: 0.65 !important;
        transition: all 0.15s ease !important;
        user-select: none !important;
        -webkit-user-select: none !important;
    }}

    .sb-card .ibtn:hover {{
        opacity: 1 !important;
        color: #666 !important;
        background: rgba(0, 0, 0, 0.04) !important;
    }}

    .sb-card .ibtn.active {{
        opacity: 1 !important;
        color: #222 !important;
        font-weight: 600 !important;
        background: rgba(0, 0, 0, 0.06) !important;
    }}

    /* Night Mode for .ibtn */
    .sb-card.nightMode .ibtn,
    .nightMode .sb-card .ibtn {{
        color: #777 !important;
        opacity: 0.55 !important;
        background: transparent !important;
    }}

    .sb-card.nightMode .ibtn:hover,
    .nightMode .sb-card .ibtn:hover {{
        opacity: 0.9 !important;
        color: #ccc !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }}

    .sb-card.nightMode .ibtn.active,
    .nightMode .sb-card .ibtn.active {{
        opacity: 1 !important;
        color: #eee !important;
        font-weight: 600 !important;
        background: rgba(255, 255, 255, 0.1) !important;
    }}

    /* Sound / Audio button inside .ctrl */
    .sb-card .ctrl .replay-button,
    .sb-card .ctrl a.soundLink {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        opacity: 0.7 !important;
        transition: opacity 0.15s ease !important;
    }}

    .sb-card .ctrl .replay-button:hover,
    .sb-card .ctrl a.soundLink:hover {{
        opacity: 1 !important;
    }}

    /* Hide Toggleable Images by default via .ms */
    .sb-card .ms,
    .sb-card #fimg,
    .sb-card #bimg,
    .sb-card [id="fimg"],
    .sb-card [id="bimg"] {{
        display: none !important;
        visibility: hidden !important;
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}

    /* Image Area (for Visible images) - clean in-flow container */
    .sb-card .img-area {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        max-width: var(--sb-img-max-width, {img_max_width}px) !important;
        margin: 0 auto 16px auto !important;
        position: relative !important;
    }}

    .sb-card .img-area img {{
        max-width: min(100%, var(--sb-img-max-width, {img_max_width}px)) !important;
        max-height: var(--sb-img-max-height, {img_max_height}px) !important;
        width: auto !important;
        height: auto !important;
        border-radius: 8px !important;
        object-fit: contain !important;
    }}

    /* Extra Area (for toggleable content) */
    .sb-card .extra-area {{
        max-width: min(96vw, max(900px, var(--sb-img-max-width, {img_max_width}px))) !important;
        width: 100% !important;
        margin: 20px auto 0 !important;
        padding: 0 16px !important;
        font-size: 1.05rem !important;
        line-height: 1.55 !important;
        color: #555 !important;
        text-align: center !important;
        opacity: 0 !important;
        max-height: 0 !important;
        overflow: hidden !important;
        transition: opacity 0.2s ease, max-height 0.25s ease !important;
        box-sizing: border-box !important;
    }}

    .sb-card .extra-area.show {{
        opacity: 1 !important;
        max-height: 1200px !important;
    }}

    .sb-card .extra-area img {{
        max-width: min(100%, var(--sb-img-max-width, {img_max_width}px)) !important;
        max-height: var(--sb-img-max-height, {img_max_height}px) !important;
        width: auto !important;
        height: auto !important;
        border-radius: 6px !important;
        object-fit: contain !important;
        margin: 0 auto !important;
        display: block !important;
    }}

    .sb-card.nightMode .extra-area,
    .nightMode .sb-card .extra-area {{
        color: #aaa !important;
    }}

    .sb-card .sb-tile {{
        font-size: var(--sb-font-size, {font_size}px) !important;
        font-family: var(--sb-font-family, {font_family}) !important;
    }}

    .sb-card .sb-tile.sb-tile-correct {{
        border: 2px solid var(--sb-anki-success) !important;
        border-color: var(--sb-anki-success) !important;
        background-color: var(--sb-tile-bg) !important;
        color: var(--sb-tile-text) !important;
    }}

    .sb-card .sb-tile.sb-tile-wrong {{
        border: 2px solid var(--sb-anki-error) !important;
        border-color: var(--sb-anki-error) !important;
        background-color: var(--sb-tile-bg) !important;
        color: var(--sb-tile-text) !important;
    }}

    .sb-card .sb-btn-check {{
        display: {check_btn_display} !important;
    }}
    """


def on_card_will_show(text: str, card: Any, kind: str) -> str:
    """
    Hooks into Anki's card rendering pipeline.
    Condition: ONLY injects CSS if card HTML actually contains Sentence Builder markers.
    Other note types are 100% untouched and receive zero extra CSS.
    """
    if not IS_DESKTOP:
        return text

    # Strict check: Does this card contain Sentence Builder elements?
    if "#sb-sandbox" not in text and "sb-card" not in text and "#front-card" not in text and "#back-card" not in text:
        return text

    cfg = get_config()
    if not cfg.get("enabled", True):
        return text

    injected_css = generate_injected_css(cfg)
    if not injected_css:
        return text

    return f"<style id='sentence-builder-injected'>{injected_css}</style>" + text


def on_webview_will_set_content(web_content: WebContent, context: Any) -> None:
    """
    Secondary safeguard for Anki WebView WebContent pipeline.
    Strictly checks that the body contains Sentence Builder markers before injecting.
    """
    if not IS_DESKTOP or not mw:
        return

    # Check if context is Reviewer, Previewer, or CardLayout
    if not (hasattr(context, "card") or context.__class__.__name__ in ("Reviewer", "Previewer", "CardLayout")):
        return

    body_content = getattr(web_content, "body", "") or ""
    # If not a Sentence Builder card, inject NOTHING
    if "#sb-sandbox" not in body_content and "sb-card" not in body_content:
        return

    cfg = get_config()
    if not cfg.get("enabled", True):
        return

    injected_css = generate_injected_css(cfg)
    if injected_css:
        web_content.head += f"<style id='sentence-builder-injected'>{injected_css}</style>"


def on_profile_did_open() -> None:
    """Automatically ensures the 'Sentence Builder' note type exists on profile load."""
    if mw and mw.col:
        ensure_sentence_builder_note_type(overwrite_templates=True)


def init_addon() -> None:
    """Initializes menu items, hooks, and configuration actions."""
    if not mw:
        return

    # 1. Register Card Render Hook (checks HTML content per card)
    gui_hooks.card_will_show.append(on_card_will_show)

    # 2. Register Webview Hook (with strict content check)
    gui_hooks.webview_will_set_content.append(on_webview_will_set_content)

    # 3. Register Profile Open Hook for automatic Note Type creation
    gui_hooks.profile_did_open.append(on_profile_did_open)

    # 4. If collection is already loaded during add-on reload/startup, ensure note type
    if mw.col:
        ensure_sentence_builder_note_type(overwrite_templates=True)

    # 5. Add single 'Sentence Builder' to Tools Menu
    action_sb = QAction("Sentence Builder", mw)
    action_sb.triggered.connect(lambda: open_settings_dialog(0))
    mw.form.menuTools.addAction(action_sb)

    # 6. Add Config Action for Add-ons list dialog
    mw.addonManager.setConfigAction(__name__, lambda: open_settings_dialog(0))


# Boot add-on
init_addon()
