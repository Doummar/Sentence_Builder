# -*- coding: utf-8 -*-
"""
Sentence Builder - Automatic Note Type Generator
Creates or updates the 'Sentence Builder' Note Type with exactly the 9 required fields and templates.
"""

from typing import Tuple, List
from aqt import mw

NOTE_TYPE_NAME: str = "Sentence Builder"

NOTE_TYPE_FIELDS: List[str] = [
    "Front",
    "Back",
    "Front Audio",
    "Back Audio",
    "Explanation",
    "Visible Front Image",
    "Front Image",
    "Visible Back Image",
    "Back Image",
]

FRONT_TEMPLATE_CONTENT: str = """<div class="sb-card" id="front-card">
  <div class="ctrl">
    {{Front Audio}}
    {{#Front Image}}
    <button class="ibtn" onclick="toggle('fimg', this)" title="Image">image</button>
    {{/Front Image}}
  </div>

  <div class="main">
    {{#Visible Front Image}}
    <div class="img-area">
      {{Visible Front Image}}
    </div>
    {{/Visible Front Image}}

    <div class="sb-prompt">{{Front}}</div>
    
    <div id="sb-interactive-block">
      <div id="sb-sandbox" class="sb-empty" ondragover="sbAllowDrop(event)" ondrop="sbDrop(event, 'sandbox')"></div>
      <div id="sb-word-bank" ondragover="sbAllowDrop(event)" ondrop="sbDrop(event, 'bank')"></div>
      
      <div class="sb-actions">
        <button type="button" class="sb-btn sb-btn-reset" onclick="sbResetTiles()" title="Reset Tiles">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          <span>Reset</span>
        </button>
        <button type="button" class="sb-btn sb-btn-check" onclick="sbCheckSentence()" title="Check Answer">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          <span>Check</span>
        </button>
      </div>
    </div>

    <!-- Hidden Raw Answer Data for script initialization -->
    <div id="sb-target-data" style="display:none;" data-sentence="{{text:Back}}"></div>

    <div id="extra-area" class="extra-area"></div>
  </div>

  {{#Front Image}}
  <div id="fimg" class="ms" style="display: none !important; visibility: hidden !important;">{{Front Image}}</div>
  {{/Front Image}}
</div>

<script>
function toggle(id, btn) {
  var source = document.getElementById(id);
  var area = document.getElementById('extra-area');
  if (!source || !area) return;

  var isActive = area.dataset.active === id;

  document.querySelectorAll('.ibtn').forEach(function(b) {
    b.classList.remove('active');
  });

  if (isActive) {
    area.innerHTML = '';
    area.dataset.active = '';
    area.classList.remove('show');
  } else {
    area.innerHTML = source.innerHTML;
    area.dataset.active = id;
    area.classList.add('show');
    btn.classList.add('active');
  }
}

// Sentence Builder interactive engine
(function() {
  var targetElem = document.getElementById("sb-target-data");
  if (!targetElem) return;

  var rawSentence = (targetElem.getAttribute("data-sentence") || "").trim();
  if (!rawSentence) return;

  var tokens = rawSentence.split(/\s+/).filter(function(t) { return t.length > 0; });
  if (tokens.length === 0) return;

  var originalOrder = tokens.slice();
  var shuffled = tokens.map(function(val, idx) { return { text: val, origIdx: idx }; });
  
  // Fisher-Yates shuffle
  for (var i = shuffled.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var temp = shuffled[i];
    shuffled[i] = shuffled[j];
    shuffled[j] = temp;
  }

  var sandbox = document.getElementById("sb-sandbox");
  var wordBank = document.getElementById("sb-word-bank");
  var draggedTile = null;

  function updateEmptyState() {
    if (sandbox.children.length === 0) {
      sandbox.classList.add("sb-empty");
    } else {
      sandbox.classList.remove("sb-empty");
    }
  }

  function clearDropIndicators() {
    sandbox.classList.remove("sb-drag-over");
    var tiles = Array.prototype.slice.call(sandbox.querySelectorAll(".sb-tile"));
    tiles.forEach(function(t) {
      t.classList.remove("sb-drop-target-left", "sb-drop-target-right");
    });
  }

  function getInsertionTarget(container, clientX, clientY) {
    var tiles = Array.prototype.slice.call(container.querySelectorAll(".sb-tile:not(.dragging)"));
    for (var i = 0; i < tiles.length; i++) {
      var rect = tiles[i].getBoundingClientRect();
      if (clientY < rect.top + 6) {
        return { element: tiles[i], side: "left" };
      }
      if (clientY <= rect.bottom + 6 && clientX < rect.left + rect.width / 2) {
        return { element: tiles[i], side: "left" };
      }
    }
    if (tiles.length > 0) {
      return { element: tiles[tiles.length - 1], side: "right" };
    }
    return null;
  }

  function createTile(item, id) {
    var tile = document.createElement("div");
    tile.className = "sb-tile";
    tile.id = "sb-tile-" + id;
    tile.textContent = item.text;
    tile.setAttribute("draggable", "true");
    tile.setAttribute("data-orig-idx", item.origIdx);
    tile.setAttribute("data-text", item.text);

    tile.addEventListener("click", function(e) {
      e.stopPropagation();
      clearDropIndicators();
      if (tile.parentElement === wordBank) {
        sandbox.appendChild(tile);
      } else {
        wordBank.appendChild(tile);
      }
      tile.classList.add("sb-tile-settle");
      setTimeout(function() { tile.classList.remove("sb-tile-settle"); }, 200);
      updateEmptyState();
      clearFeedback();
      saveUserAttempt();
      checkAutoValidate();
    });

    tile.addEventListener("dragstart", function(e) {
      draggedTile = tile;
      tile.classList.add("dragging");
      e.dataTransfer.setData("text/plain", tile.id);
      e.dataTransfer.effectAllowed = "move";
    });

    tile.addEventListener("dragend", function() {
      tile.classList.remove("dragging");
      draggedTile = null;
      clearDropIndicators();
    });

    return tile;
  }

  function saveUserAttempt() {
    try {
      var assembled = Array.prototype.slice.call(sandbox.children);
      var attempt = assembled.map(function(t, idx) {
        var expected = originalOrder[idx];
        var actual = t.getAttribute("data-text");
        return {
          text: actual,
          isCorrect: (expected === actual)
        };
      });
      sessionStorage.setItem("sb_user_attempt", JSON.stringify(attempt));
    } catch(e) {}
  }

  wordBank.innerHTML = "";
  sandbox.innerHTML = "";
  shuffled.forEach(function(item, idx) {
    var tile = createTile(item, idx);
    wordBank.appendChild(tile);
  });
  updateEmptyState();
  saveUserAttempt();

  function clearFeedback() {
    var tiles = document.querySelectorAll(".sb-tile");
    tiles.forEach(function(t) {
      t.classList.remove("sb-tile-correct", "sb-tile-wrong");
    });
  }

  window.sbAllowDrop = function(e) {
    e.preventDefault();
    if (e.dataTransfer) {
      e.dataTransfer.dropEffect = "move";
    }

    if (sandbox.contains(e.target) || e.target === sandbox) {
      sandbox.classList.add("sb-drag-over");
      var targetInfo = getInsertionTarget(sandbox, e.clientX, e.clientY);
      var tiles = Array.prototype.slice.call(sandbox.querySelectorAll(".sb-tile:not(.dragging)"));
      tiles.forEach(function(t) {
        t.classList.remove("sb-drop-target-left", "sb-drop-target-right");
      });
      if (targetInfo && targetInfo.element) {
        if (targetInfo.side === "left") {
          targetInfo.element.classList.add("sb-drop-target-left");
        } else {
          targetInfo.element.classList.add("sb-drop-target-right");
        }
      }
    }
  };

  window.sbDrop = function(e, targetZone) {
    e.preventDefault();
    var tileId = e.dataTransfer.getData("text/plain");
    var tile = document.getElementById(tileId) || draggedTile;
    clearDropIndicators();
    if (!tile) return;

    if (targetZone === "sandbox") {
      var targetInfo = getInsertionTarget(sandbox, e.clientX, e.clientY);
      if (targetInfo && targetInfo.element) {
        if (targetInfo.side === "left") {
          if (targetInfo.element !== tile) {
            sandbox.insertBefore(tile, targetInfo.element);
          }
        } else {
          if (targetInfo.element.nextSibling !== tile) {
            sandbox.insertBefore(tile, targetInfo.element.nextSibling);
          }
        }
      } else {
        sandbox.appendChild(tile);
      }
    } else {
      wordBank.appendChild(tile);
    }

    tile.classList.add("sb-tile-settle");
    setTimeout(function() { tile.classList.remove("sb-tile-settle"); }, 200);

    updateEmptyState();
    clearFeedback();
    saveUserAttempt();
    checkAutoValidate();
  };

  window.sbResetTiles = function() {
    var allTiles = Array.prototype.slice.call(document.querySelectorAll(".sb-tile"));
    allTiles.forEach(function(tile) {
      tile.classList.remove("sb-tile-correct", "sb-tile-wrong");
      wordBank.appendChild(tile);
    });
    updateEmptyState();
    saveUserAttempt();
  };

  window.sbCheckSentence = function() {
    var assembled = Array.prototype.slice.call(sandbox.children);
    if (assembled.length === 0) return false;

    var isAllCorrect = true;
    if (assembled.length !== originalOrder.length) {
      isAllCorrect = false;
    }

    assembled.forEach(function(tile, idx) {
      var expected = originalOrder[idx];
      var actual = tile.getAttribute("data-text");
      if (expected === actual) {
        tile.classList.add("sb-tile-correct");
        tile.classList.remove("sb-tile-wrong");
      } else {
        tile.classList.add("sb-tile-wrong");
        tile.classList.remove("sb-tile-correct");
        isAllCorrect = false;
      }
    });

    saveUserAttempt();

    if (isAllCorrect && assembled.length === originalOrder.length) {
      if (typeof pycmd !== "undefined") {
        setTimeout(function() {
          try { pycmd("ans"); } catch(e) {}
        }, 400);
      }
    }
    return isAllCorrect;
  };

  function checkAutoValidate() {
    if (wordBank.children.length === 0 && sandbox.children.length === originalOrder.length) {
      sbCheckSentence();
    }
  }
})();
</script>"""

BACK_TEMPLATE_CONTENT: str = """<div class="sb-card" id="back-card">
  <div class="ctrl">
    {{Back Audio}}
    {{#Back Image}}
    <button class="ibtn" onclick="toggle('bimg', this)" title="Image">image</button>
    {{/Back Image}}
  </div>

  <div class="main">
    {{#Visible Back Image}}
    <div class="img-area">
      {{Visible Back Image}}
    </div>
    {{/Visible Back Image}}

    <!-- Unified Back Card Content Group -->
    <div id="sb-content-group">
      <!-- 1. The prompt (Front) -->
      <div class="sb-prompt">{{Front}}</div>

      <!-- 2. Structured Back Block matching front interactive block height -->
      <div id="sb-back-block" class="sb-back-block">
        <!-- User's assembled attempt (tiles) -->
        <div id="sb-user-attempt" class="sb-user-attempt"></div>

        <!-- Clean divider between attempt and full correct sentence -->
        <hr class="sb-divider" />

        <!-- Correct sentence directly under user's attempt in normal text -->
        <div class="sb-solution">
          {{Back}}
        </div>

        <!-- Optional Explanation -->
        {{#Explanation}}
        <div class="sb-explanation">
          <hr class="sb-divider" />
          {{Explanation}}
        </div>
        {{/Explanation}}
      </div>
    </div>

    <div id="extra-area" class="extra-area"></div>
  </div>

  {{#Back Image}}
  <div id="bimg" class="ms" style="display: none !important; visibility: hidden !important;">{{Back Image}}</div>
  {{/Back Image}}
</div>

<script>
function toggle(id, btn) {
  var source = document.getElementById(id);
  var area = document.getElementById('extra-area');
  if (!source || !area) return;

  var isActive = area.dataset.active === id;

  document.querySelectorAll('.ibtn').forEach(function(b) {
    b.classList.remove('active');
  });

  if (isActive) {
    area.innerHTML = '';
    area.dataset.active = '';
    area.classList.remove('show');
  } else {
    area.innerHTML = source.innerHTML;
    area.dataset.active = id;
    area.classList.add('show');
    btn.classList.add('active');
  }
}

// Display user's attempt on back card & format solution
(function() {
  var container = document.getElementById("sb-user-attempt");
  var solElem = document.querySelector(".sb-solution");
  var tilesWrapper = document.createElement("div");
  tilesWrapper.className = "sb-attempt-tiles";
  var attempt = [];
  var targetTokens = [];
  var isBracketed = false;

  try {
    var raw = sessionStorage.getItem("sb_user_attempt");
    if (raw) {
      var parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        attempt = parsed;
      } else if (parsed && parsed.assembled) {
        attempt = parsed.assembled;
        targetTokens = parsed.targetTokens || [];
        isBracketed = !!parsed.isBracketed;
      }
    }
  } catch(e) {}

  if (container) {
    if (attempt.length > 0) {
      attempt.forEach(function(item) {
        var tile = document.createElement("div");
        tile.className = "sb-tile " + (item.isCorrect ? "sb-tile-correct" : "sb-tile-wrong");
        tile.textContent = item.text;
        tilesWrapper.appendChild(tile);
      });
    } else {
      tilesWrapper.innerHTML = '<span style="font-size: 0.88rem; opacity: 0.45; font-style: italic;">(No words assembled)</span>';
    }
    container.appendChild(tilesWrapper);
  }

  // Format solution sentence:
  // Words that the user got correct -> stay normal weight
  // Words that the user got wrong (wrong position or wrong word) -> make them bold
  if (solElem) {
    var rawText = (solElem.textContent || solElem.innerText || "").trim();
    if (rawText && attempt.length > 0) {
      var words = rawText.split(/\s+/).filter(function(w) { return w.length > 0; });
      var formatted = [];
      var targetIdx = 0;

      words.forEach(function(word) {
        var isChallengeWord = false;
        var isWordCorrect = false;

        if (isBracketed && targetTokens.length > 0) {
          if (targetIdx < targetTokens.length) {
            var cleanWord = word.replace(/^[^\w\s\u00C0-\u024F]+|[^\w\s\u00C0-\u024F]+$/g, "").toLowerCase();
            var cleanTarget = targetTokens[targetIdx].replace(/^[^\w\s\u00C0-\u024F]+|[^\w\s\u00C0-\u024F]+$/g, "").toLowerCase();
            if (word.toLowerCase() === targetTokens[targetIdx].toLowerCase() || cleanWord === cleanTarget) {
              isChallengeWord = true;
              if (attempt[targetIdx] && attempt[targetIdx].isCorrect) {
                isWordCorrect = true;
              }
              targetIdx++;
            }
          }
        } else {
          isChallengeWord = true;
          if (attempt[targetIdx] && attempt[targetIdx].isCorrect) {
            isWordCorrect = true;
          }
          targetIdx++;
        }

        if (isChallengeWord && !isWordCorrect) {
          formatted.push('<b class="sb-word-wrong">' + word + '</b>');
        } else {
          formatted.push('<span class="sb-word-normal">' + word + '</span>');
        }
      });

      solElem.innerHTML = formatted.join(" ");
    }
  }
})();
</script>"""

CSS_STYLING_CONTENT: str = """/* ==========================================================================
   Sentence Builder (SB) - Card Template Styling
   Compatible with .ctrl, .ibtn, .ms, .img-area, .main
   ========================================================================== */

/* BASE SB-CARD RESET - Strictly Scoped to Sentence Builder */
.sb-card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  font-size: 18px;
  color: #1a1a1a;
  margin: 0 !important;
  padding: 0 !important;
  text-align: center;
  overflow-x: hidden;
  overflow-y: auto;
  direction: ltr !important;
  min-height: 100vh;
  width: 100%;
  box-sizing: border-box !important;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}

/* IMAGE SLOT */
.sb-card .img-area {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  max-width: var(--sb-img-max-width, 680px) !important;
  margin: 0 auto 16px auto !important;
  position: relative !important;
}

.sb-card .img-area img {
  max-width: min(100%, var(--sb-img-max-width, 680px)) !important;
  max-height: var(--sb-img-max-height, 340px) !important;
  width: auto !important;
  height: auto !important;
  border-radius: 8px !important;
  object-fit: contain !important;
}

/* EXTRA AREA (FOR TOGGLEABLE CONTENT) */
.sb-card .extra-area {
  max-width: min(96vw, max(900px, var(--sb-img-max-width, 680px)));
  width: 100%;
  margin: 20px auto 0;
  padding: 0 16px;
  font-size: 1.05rem;
  line-height: 1.55;
  color: #555;
  text-align: center;
  opacity: 0;
  max-height: 0;
  overflow: hidden;
  transition: opacity 0.2s ease, max-height 0.25s ease;
  box-sizing: border-box;
}

.sb-card .extra-area.show {
  opacity: 1;
  max-height: 1200px;
}

.sb-card .extra-area img {
  max-width: min(100%, var(--sb-img-max-width, 680px)) !important;
  max-height: var(--sb-img-max-height, 340px) !important;
  width: auto !important;
  height: auto !important;
  border-radius: 6px;
  object-fit: contain;
  margin: 0 auto;
  display: block;
}

/* MAIN CONTENT */
.sb-card .main {
  font-size: 1.8rem;
  line-height: 1.45;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: inherit !important;
  justify-content: flex-start !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  box-sizing: border-box !important;
  position: relative !important;
}

.sb-card .main div, .sb-card .main p, .sb-card .main span {
  text-align: inherit;
}

/* CONTROLS (AUDIO & IMAGE TOGGLES) - strictly scoped to .sb-card */
.sb-card .ctrl {
  position: fixed;
  top: var(--sb-ctrl-top, 14px);
  bottom: var(--sb-ctrl-bottom, auto);
  left: var(--sb-ctrl-left, auto);
  right: var(--sb-ctrl-right, 14px);
  display: flex;
  flex-direction: column;
  align-items: var(--sb-ctrl-align, flex-end);
  gap: 4px;
  z-index: 100;
}

/* BUTTONS - strictly scoped to .sb-card */
.sb-card .ibtn {
  min-width: auto;
  height: 22px;
  padding: 0 6px;
  border-radius: 5px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 500;
  color: #aaa;
  white-space: nowrap;
  line-height: 1;
  opacity: 0.65;
  transition: all 0.15s ease;
}

.sb-card .ibtn:hover {
  opacity: 1;
  color: #666;
  background: rgba(0, 0, 0, 0.04);
}

.sb-card .ibtn.active {
  opacity: 1;
  color: #222;
  font-weight: 600;
  background: rgba(0, 0, 0, 0.06);
}

/* HIDDEN (.ms) - Ensures toggleable sources are NEVER visible on the card */
.sb-card .ms,
.sb-card #fimg,
.sb-card #bimg,
.sb-card [id="fimg"],
.sb-card [id="bimg"] {
  display: none !important;
  visibility: hidden !important;
  position: absolute !important;
  width: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

/* NIGHT MODE - strictly scoped to .sb-card */
.nightMode .sb-card,
.night_mode .sb-card,
.sb-card.nightMode {
  color: #e8e8e8;
}
.nightMode .sb-card .main,
.night_mode .sb-card .main,
.sb-card.nightMode .main,
.nightMode .sb-card .main div,
.night_mode .sb-card .main div { color: #f0f0f0; }

.nightMode .sb-card .extra-area,
.night_mode .sb-card .extra-area,
.sb-card.nightMode .extra-area {
  color: #aaa;
}

.nightMode .sb-card .ibtn,
.night_mode .sb-card .ibtn,
.sb-card.nightMode .ibtn {
  color: #777;
  opacity: 0.55;
  background: transparent;
}

.nightMode .sb-card .ibtn:hover,
.night_mode .sb-card .ibtn:hover,
.sb-card.nightMode .ibtn:hover {
  opacity: 0.9;
  color: #ccc;
  background: rgba(255, 255, 255, 0.06);
}

.nightMode .sb-card .ibtn.active,
.night_mode .sb-card .ibtn.active,
.sb-card.nightMode .ibtn.active {
  opacity: 1;
  color: #eee;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.1);
}

/* ==========================================================================
   Sentence Builder Interactive Elements
   ========================================================================== */
:root {
  --sb-font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  --sb-font-size: 18px;
  --sb-correct-color: #22c55e;
  --sb-wrong-color: #ef4444;
  --sb-anki-success: var(--color-success, var(--success, var(--ans-good, #28a745)));
  --sb-anki-error: var(--color-danger, var(--color-error, var(--danger, var(--error, var(--ans-again, #dc2626)))));
  --sb-tile-bg: #ffffff;
  --sb-tile-border: #e5e7eb;
  --sb-tile-text: #1f2937;
  --sb-tile-hover: #f9fafb;
  --sb-box-bg: #f9fafb;
  --sb-box-border: #d1d5db;
  --sb-accent: #3b82f6;
  --sb-text: #1f2937;
}

.nightMode,
.night_mode,
.sb-card.nightMode,
.nightMode .sb-card,
.night_mode .sb-card,
body.nightMode,
body.night_mode,
[data-theme="dark"],
.dark {
  --sb-anki-success: var(--color-success, var(--success, var(--ans-good, #2ecc71)));
  --sb-anki-error: var(--color-danger, var(--color-error, var(--danger, var(--error, var(--ans-again, #ff6b6b)))));
  --sb-tile-bg: #27272a;
  --sb-tile-border: #3f3f46;
  --sb-tile-text: #f4f4f5;
  --sb-tile-hover: #323236;
  --sb-box-bg: rgba(255, 255, 255, 0.02);
  --sb-box-border: #3f3f46;
  --sb-accent: #38bdf8;
  --sb-text: #f4f4f5;
}

/* 4. Prompt Title */
.sb-prompt {
  font-size: 1.25rem !important;
  font-weight: normal !important;
  margin: 0 0 12px 0 !important;
  padding: 0 !important;
  color: inherit;
  line-height: 1.45 !important;
  text-align: inherit !important;
  width: var(--sb-line-width, 520px) !important;
  max-width: var(--sb-line-width, 520px) !important;
  min-width: var(--sb-line-width, 520px) !important;
  word-break: normal !important;
  overflow-wrap: break-word !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  box-sizing: border-box !important;
}

/* 5. Fixed Structure Containers (No Jumping, Zero Visible Scrollbars) */
#sb-interactive-block {
  width: var(--sb-line-width, 520px) !important;
  max-width: var(--sb-line-width, 520px) !important;
  min-width: var(--sb-line-width, 520px) !important;
  height: 280px !important;
  min-height: 280px !important;
  max-height: 280px !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: inherit !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  box-sizing: border-box !important;
}

.sb-back-block {
  width: var(--sb-line-width, 520px) !important;
  max-width: var(--sb-line-width, 520px) !important;
  min-width: var(--sb-line-width, 520px) !important;
  height: auto !important;
  min-height: 280px !important;
  max-height: none !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: inherit !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  box-sizing: border-box !important;
}

#sb-sandbox {
  width: var(--sb-line-width, 520px) !important;
  min-width: var(--sb-line-width, 520px) !important;
  max-width: var(--sb-line-width, 520px) !important;
  height: 140px !important;
  min-height: 140px !important;
  max-height: 140px !important;
  margin: 0 !important;
  box-sizing: border-box !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  overflow: hidden !important;
  background: var(--sb-box-bg);
  border: 1.5px dashed var(--sb-box-border);
  border-radius: 10px;
  padding: 10px 14px !important;
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  align-content: center !important;
  justify-content: center !important;
  gap: 6px !important;
  transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease;
}

#sb-sandbox::-webkit-scrollbar,
#sb-word-bank::-webkit-scrollbar,
.sb-attempt-tiles::-webkit-scrollbar,
.sb-user-attempt::-webkit-scrollbar {
  display: none !important;
  width: 0 !important;
  height: 0 !important;
}

#sb-sandbox.sb-drag-over {
  border-color: var(--sb-accent) !important;
  border-style: solid !important;
  background-color: rgba(59, 130, 246, 0.06) !important;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15) !important;
}

.nightMode #sb-sandbox.sb-drag-over {
  background-color: rgba(56, 189, 248, 0.08) !important;
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
}

#sb-sandbox.sb-empty::after {
  content: "Tap or drag words here to build the sentence";
  font-size: 0.88rem;
  opacity: 0.45;
  font-style: italic;
  pointer-events: none;
  font-weight: 400;
}

#sb-word-bank {
  width: var(--sb-line-width, 520px) !important;
  min-width: var(--sb-line-width, 520px) !important;
  max-width: var(--sb-line-width, 520px) !important;
  min-height: 84px !important;
  max-height: 84px !important;
  height: 84px !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  padding: 6px 10px !important;
  margin: 12px 0 0 0 !important;
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  align-content: center !important;
  justify-content: center !important;
  gap: 6px !important;
  transition: opacity 0.2s ease;
}

.sb-tile {
  font-family: var(--sb-font-family);
  font-size: var(--sb-font-size);
  color: var(--sb-tile-text);
  background-color: var(--sb-tile-bg);
  border: 1px solid var(--sb-tile-border);
  border-radius: 6px;
  padding: 6px 12px;
  font-weight: 500;
  cursor: grab;
  user-select: none;
  touch-action: manipulation;
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease, background-color 0.15s ease, opacity 0.15s ease, margin 0.15s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  position: relative;
  line-height: 1.3;
}

.sb-tile:hover {
  background-color: var(--sb-tile-hover);
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}

.sb-tile:active {
  cursor: grabbing;
}

.sb-tile.dragging {
  opacity: 0.4 !important;
  transform: scale(1.04) translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
  cursor: grabbing !important;
  z-index: 10;
}

.sb-tile.sb-drop-target-left {
  margin-left: 12px !important;
}

.sb-tile.sb-drop-target-left::before {
  content: "";
  position: absolute;
  left: -8px;
  top: 15%;
  height: 70%;
  width: 2px;
  background-color: var(--sb-accent);
  border-radius: 1px;
  pointer-events: none;
}

.sb-tile.sb-drop-target-right {
  margin-right: 12px !important;
}

.sb-tile.sb-drop-target-right::after {
  content: "";
  position: absolute;
  right: -8px;
  top: 15%;
  height: 70%;
  width: 2px;
  background-color: var(--sb-accent);
  border-radius: 1px;
  pointer-events: none;
}

.sb-tile.sb-tile-settle {
  animation: sb-settle 0.15s cubic-bezier(0.2, 0.9, 0.3, 1.2);
}

@keyframes sb-settle {
  0% { transform: scale(0.95); }
  100% { transform: scale(1); }
}

.sb-tile.sb-tile-correct {
  border: 2px solid var(--sb-anki-success) !important;
  border-color: var(--sb-anki-success) !important;
  background-color: var(--sb-tile-bg) !important;
  color: var(--sb-tile-text) !important;
}

.sb-tile.sb-tile-wrong {
  border: 2px solid var(--sb-anki-error) !important;
  border-color: var(--sb-anki-error) !important;
  background-color: var(--sb-tile-bg) !important;
  color: var(--sb-tile-text) !important;
  animation: sb-shake 0.3s ease;
}

@keyframes sb-shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-3px); }
  75% { transform: translateX(3px); }
}

.sb-actions {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  margin-top: 12px !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
}

.sb-btn {
  background: transparent;
  border: 1px solid var(--sb-tile-border);
  color: var(--sb-tile-text);
  opacity: 0.75;
  padding: 4px 10px;
  border-radius: 5px;
  font-size: 11.5px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  line-height: 1;
  transition: all 0.15s ease;
}

.sb-btn:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.04);
  border-color: var(--sb-box-border);
}

.nightMode .sb-btn:hover {
  background: rgba(255, 255, 255, 0.06);
}

.sb-btn.sb-btn-check {
  background: var(--sb-accent);
  color: #ffffff;
  border: none;
  opacity: 1;
  padding: 4px 12px;
}

.sb-btn.sb-btn-check:hover {
  opacity: 0.9;
  background: var(--sb-accent);
}

.sb-user-attempt {
  width: var(--sb-line-width, 520px) !important;
  max-width: var(--sb-line-width, 520px) !important;
  min-width: var(--sb-line-width, 520px) !important;
  margin: 0 !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  box-sizing: border-box !important;
}

.sb-attempt-tiles {
  width: var(--sb-line-width, 520px) !important;
  min-width: var(--sb-line-width, 520px) !important;
  max-width: var(--sb-line-width, 520px) !important;
  min-height: 40px !important;
  height: auto !important;
  max-height: none !important;
  margin: 0 !important;
  box-sizing: border-box !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  background: transparent !important;
  border: none !important;
  padding: 4px 0 !important;
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  align-content: center !important;
  justify-content: center !important;
  gap: 8px !important;
}

.sb-solution {
  font-size: 1.25rem !important;
  font-weight: 400 !important;
  color: var(--sb-text) !important;
  margin: 12px 0 0 0 !important;
  padding: 0 !important;
  width: var(--sb-line-width, 520px) !important;
  max-width: var(--sb-line-width, 520px) !important;
  min-width: var(--sb-line-width, 520px) !important;
  min-height: auto !important;
  height: auto !important;
  max-height: none !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  box-sizing: border-box !important;
  text-align: inherit !important;
  line-height: 1.45 !important;
  background: transparent !important;
  border: none !important;
}

.sb-solution b,
.sb-solution strong,
.sb-solution .sb-word-wrong {
  font-weight: 700 !important;
}

.sb-solution .sb-word-normal {
  font-weight: 400 !important;
}

.nightMode .sb-solution {
  color: var(--sb-text) !important;
}

.sb-explanation {
  margin: 14px 0 0 0 !important;
  font-size: 0.95rem !important;
  line-height: 1.55 !important;
  text-align: inherit !important;
  opacity: 0.82 !important;
  width: var(--sb-line-width, 520px) !important;
  max-width: var(--sb-line-width, 520px) !important;
  min-width: var(--sb-line-width, 520px) !important;
  flex-shrink: 0 !important;
  box-sizing: border-box !important;
}

.sb-divider {
  border: 0;
  border-top: 1px solid rgba(128, 128, 128, 0.2);
  margin: 12px 0;
  width: 100%;
}"""


def ensure_sentence_builder_note_type(overwrite_templates: bool = False) -> Tuple[bool, str]:
    """
    Checks if 'Sentence Builder' exists. If not, creates it automatically.
    Ensures ONLY the 9 required fields exist, deleting every other field permanently.
    Returns (success_boolean, status_message).
    """
    if not mw or not mw.col:
        return False, "Anki collection is not loaded."

    try:
        models = mw.col.models
        model = models.by_name(NOTE_TYPE_NAME)
        created = False

        if not model:
            model = models.new(NOTE_TYPE_NAME)
            created = True

        # 1. Permanently delete all fields that are not in NOTE_TYPE_FIELDS
        allowed_fields = set(NOTE_TYPE_FIELDS)
        for fld in list(model.get("flds", [])):
            fname = fld.get("name", "")
            if fname not in allowed_fields:
                try:
                    models.remove_field(model, fld)
                except Exception:
                    pass

        # 2. Ensure all 9 required fields exist
        existing_fields = [f["name"] for f in model.get("flds", [])]
        for field_name in NOTE_TYPE_FIELDS:
            if field_name not in existing_fields:
                try:
                    new_fld = models.new_field(field_name)
                    models.add_field(model, new_fld)
                except Exception:
                    pass

        # 3. Always synchronize templates and styling
        if len(model.get("tmpls", [])) == 0:
            t = models.new_template("Card 1")
            t["qfmt"] = FRONT_TEMPLATE_CONTENT
            t["afmt"] = BACK_TEMPLATE_CONTENT
            models.add_template(model, t)
        else:
            tmpl = model["tmpls"][0]
            tmpl["qfmt"] = FRONT_TEMPLATE_CONTENT
            tmpl["afmt"] = BACK_TEMPLATE_CONTENT

        model["css"] = CSS_STYLING_CONTENT

        if created:
            models.add(model)
            msg = f"Created '{NOTE_TYPE_NAME}' note type with exactly 9 fields and templates."
        else:
            models.save(model)
            msg = f"Cleaned legacy fields and updated '{NOTE_TYPE_NAME}' note type with 9 fields."

        return True, msg
    except Exception as exc:
        return False, f"Failed to setup note type: {str(exc)}"
