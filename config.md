# Sentence Builder (SB) Configuration Guide

Sentence Builder is a lightweight, high-performance Anki add-on designed to enhance language learning through interactive sentence reconstruction.

### Configuration Options

* **`enabled`** (`true` / `false`): Globally enables or disables Sentence Builder style injections and behaviors on desktop.
* **`card_position`** (`"top"`, `"center"`, `"bottom"`): Controls the vertical alignment of the card (`.sb-card`).
* **`horizontal_alignment`** (`"center"`, `"left"`, `"right"`): Controls horizontal alignment of the card contents.
* **`controls_position`** (`"top_right"`, `"top_left"`, `"bottom_right"`, `"bottom_left"`): Controls the corner placement of the Audio & Image toggle button bar (`.ctrl`). Default: `"top_right"`.
* **`line_width`** (integer, px: 400 - 700): Sets the fixed line width of the prompt, sandbox, and word bank. Default: 520.
* **`font_family`** (string): Sets the base font family applied via CSS custom properties (`--sb-font-family`).
* **`font_size`** (integer, px): Sets the base font size for sentence tiles and prompts (`--sb-font-size`).
* **`image_size`** (`"small"`, `"medium"`, `"large"`, `"extra_large"`): Controls max dimensions for visible & toggleable images (`"medium"` default: 680×340px, `"small"`: 480×240px, `"large"`: 880×440px, `"extra_large"`: 1160×580px).
* **`correct_color`** (hex string): Color applied to correctly assembled tiles and success borders (`--sb-correct-color`). Default: `#22c55e`.
* **`wrong_color`** (hex string): Color applied to incorrect tiles and error borders (`--sb-wrong-color`). Default: `#ef4444`.
* **`custom_colors_enabled`** (`true` / `false`): Whether custom hex colors override template defaults.
* **`auto_reveal_back`** (`true` / `false`): Automatically reveals the back/explanation when the sentence is assembled correctly.
* **`show_check_button`** (`true` / `false`): Controls visibility of the ✓ Check button. Default: `false` (hidden).

### Mobile Notice
Sentence Builder templates are pure HTML/CSS/JavaScript and run out-of-the-box on **AnkiMobile (iOS)** and **AnkiDroid (Android)** without needing add-ons installed.