# Sentence Builder - Anki Add-on

![Sentence Builder Demonstration](demo.gif)

A lightweight, robust add-on for Anki Desktop that provides customizable styling, card alignment, and interactive word assembly for language learning cards.

## Features

- Interactive sentence construction with word tiles and keyboard shortcuts.
- Customizable vertical positioning (Top, Center, Bottom) and horizontal alignment (Left, Center, Right).
- Native Anki dark mode and light mode support.
- Configurable typography, line width, and image dimensions.
- Optional check button and automatic answer reveal upon sentence completion.
- Cross-platform card templates compatible with Anki Desktop, AnkiMobile (iOS), and AnkiDroid (Android).

## Installation

### Method 1: Install Package File
1. Download Sentence_Builder.ankiaddon.
2. In Anki, open Tools -> Add-ons.
3. Click "Install from file..." in the lower right corner.
4. Select Sentence_Builder.ankiaddon and restart Anki.

### Method 2: Manual Directory Installation
1. Open Anki and navigate to Tools -> Add-ons -> View Files.
2. Copy the Sentence_Builder folder into the opened addons21 directory.
3. Restart Anki.

## Note Type Setup

Create or configure an Anki Note Type named "Sentence Builder" with the following fields:

- Prompt: The source text or prompt to translate.
- Sentence: The target sentence to be reconstructed.
- Subprompt: Optional grammatical hints or supplementary context.
- Audio: Optional audio playback tag, such as [sound:audio.mp3].
- Notes: Optional detailed grammatical explanations or vocabulary notes.

### Template Files

1. Front Template: Copy the contents of templates/front.html into the Front Template editor.
2. Back Template: Copy the contents of templates/back.html into the Back Template editor.
3. Styling: Copy the contents of templates/styling.css into the Styling editor.

## Settings

Access configuration via Tools -> Sentence Builder... or through the Add-ons manager.

- Vertical Position: Aligns cards to the top, center, or bottom of the review window.
- Horizontal Alignment: Aligns content to the left, center, or right.
- Controls Position: Position of card controls (Top Right, Top Left, Bottom Right, Bottom Left).
- Line Width: Sets maximum width in pixels for content blocks (400px to 1200px).
- Font Family: Selects the typeface used for word tiles and sentence text.
- Font Size: Base font size in pixels.
- Image Size: Maximum display size for media images (Small, Medium, Large, Extra Large).
- Check Button: Enables or disables a manual verification button on the front card.
- Answer Reveal: Automatically transitions to the back card when all words are placed.

## Compatibility

The Python add-on runs on Anki Desktop (Windows, macOS, and Linux) to provide configuration and CSS injection. The card templates use standard HTML, CSS, and JavaScript, operating on AnkiMobile (iOS), AnkiDroid (Android), and AnkiWeb without requiring desktop add-on execution.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
