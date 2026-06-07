#!/usr/bin/env python3
"""
Run this against your index.html to fix the broken exercise image display.
Usage: python3 fix_exercise_images.py index.html
"""
import sys, re, shutil, os

if len(sys.argv) < 2:
    print("Usage: python3 fix_exercise_images.py index.html")
    sys.exit(1)

path = sys.argv[1]
shutil.copy(path, path + ".bak")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ── CHANGE 1: Replace broken IIFE with named function call ──────────────────
old_iife = "${(()=>{const u=EXERCISE_IMAGES[ex.name.toLowerCase().trim()];return u?'<img class=\"exercise-img\" src=\"'+u+'\" alt=\"'+ex.name+'\" loading=\"lazy\">':'';})()}"
new_call = "${_exImg(ex.name)}"

if old_iife not in content:
    print("WARNING: Could not find the broken IIFE pattern. File may already be patched or differ.")
else:
    content = content.replace(old_iife, new_call)
    print("CHANGE 1 applied: replaced IIFE with _exImg() call")

# ── CHANGE 2: Inject helper function before closing </script> ────────────────
helper_fn = """
// ── EXERCISE IMAGE HELPER ────────────────────────────────────────────────────
function _exImg(name) {
  var u = EXERCISE_IMAGES[(name || '').toLowerCase().trim()];
  if (!u) return '';
  return '<img class="exercise-img" src="' + u + '" alt="' + (name || '').replace(/"/g, "\\'") + '" loading="lazy" onerror="this.style.display=\\'none\\'">';
}
"""

if "_exImg" not in content:
    # Insert before the closing </script> that contains EXERCISE_IMAGES
    content = content.replace("</script>", helper_fn + "</script>", 1)
    print("CHANGE 2 applied: _exImg() helper function added")
else:
    print("CHANGE 2 skipped: _exImg already present")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone. Original saved as {path}.bak")
print("Upload the updated index.html to GitHub to deploy.")
