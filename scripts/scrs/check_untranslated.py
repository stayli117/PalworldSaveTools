#!/usr/bin/env python3
"""
Translation safety scanner for PST UI code.

Two checks, both high-signal (low false-positive):

  [error]   TRANSLATE_INTO_SAVE
      A translation call (t / dn / desc_t / display_name) is assigned
      directly into a save-bound structure (raw, loaded_level_json,
      slot_data, item_name, ...). This would write localized text back
      into the save and corrupt it. Forbidden by the i18n contract.

  [warning] RAW_NAME_IN_DISPLAY
      A display sink (widget ctor / setText / setToolTip / ...) receives a
      value that is *tainted* — i.e. it derives from a raw game-name
      resolver (resolve_name, _NAMEMAP.get, extract_value, ...) and was
      NOT wrapped in t()/dn(). This is the classic "English name leaks
      into the UI" bug. We also flag `t(key, name=TAINTED)`: a raw name
      interpolated into a *translated* template still renders English.
      We deliberately do NOT flag every untranslated string (that drowns
      in false positives from already-localized `t(...) if t else ...`
      idioms and pre-translated parameters).

Taint tracking is intra-function with fixpoint propagation so that
`name = resolve_name(...)` then `QLabel(name)` is caught, while
`name = t(...)` or a pre-translated parameter is not.

Usage:
  python check_untranslated.py                 # scan src/ (UI-focused excludes)
  python check_untranslated.py --root src/palworld_aio
  python check_untranslated.py -v              # show code snippets
  python check_untranslated.py --strict        # fail on warnings too

Exit codes: 0 clean · 1 violations · 2 bad args
"""
from __future__ import annotations

import argparse
import ast
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

# ── Terminal Colors ──────────────────────────────────────────────

_SUPPORTS_COLOR = (
    hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    and os.environ.get('TERM') not in ('dumb', '')
)


def _c(code: str, text: str) -> str:
    return f'{code}{text}\033[0m' if _SUPPORTS_COLOR else text


RED = lambda s: _c('\033[91m', s)
GREEN = lambda s: _c('\033[92m', s)
YELLOW = lambda s: _c('\033[93m', s)
CYAN = lambda s: _c('\033[96m', s)
BOLD = lambda s: _c('\033[1m', s)
DIM = lambda s: _c('\033[2m', s)

# ── Translation / taint vocabulary ───────────────────────────────

TRANSLATE_FUNCS = {
    't', 'dn', 'desc_t', 'display_name',
    'tr', '_', 'gettext', 'translate', 'QT_TRANSLATE_NOOP',
}

# Functions that return a RAW (untranslated) game *name*.
# NOTE: extract_value is intentionally NOT here — it returns all kinds of raw
# values (levels, numbers, player-given nicknames), only some of which are
# names. Including it caused false positives on numeric/昵称 labels.
TAINT_RESOLVER_NAMES = {'resolve_name', 'load_game_data_map'}

# Functions that merely pass a tainted string through unchanged.
TAINT_PASSTHROUGH_NAMES = {'_strip_prefix_label'}

# Known raw-name map attributes (e.g. self._NAMEMAP, cls._SKILLMAP).
TAINT_MAP_NAMES = {
    '_NAMEMAP', '_SKILLMAP', '_PASSMAP', '_PALMAP', '_NPCMAP',
    '_PASSRANK', '_RANK_COLORS', '_PASSFLAGS',
}

# Widget constructors whose first positional arg is a display string.
CTOR_SINKS = {
    'QLabel', 'QPushButton', 'QListWidgetItem', 'QTreeWidgetItem',
    'QTableWidgetItem', 'QAction', 'QCheckBox', 'QRadioButton',
    'QGroupBox', 'QCommandLinkButton', 'QMenu',
}

# Method sinks -> index of the display-text argument.
# -1 means "1 if 2+ args else 0" (QComboBox.addItem(text) / addItem(icon, text)).
METHOD_SINKS = {
    'setText': 0,
    'setToolTip': 0,
    'setWindowTitle': 0,
    'setPlaceholderText': 0,
    'setStatusTip': 0,
    'setWhatsThis': 0,
    'setAccessibleName': 0,
    'addTab': 1,
    'addItem': -1,
    'setItemText': 1,
    'showText': 1,
}

# Tokens marking a save-bound structure (localized text must never land here).
SAVE_TARGET_TOKENS = {
    'raw', 'loaded_level_json', 'slot_data', 'item_name',
    'player_data', 'guild_data', 'save_data', 'inventory_data',
    'container_data', 'pal_data', 'properties',
}

DEFAULT_EXCLUDES = ('src/i18n', 'src/palsav', 'src/palworld_toolsets',
                    'src/palworld_xgp_import', 'tests')

CATEGORY_NAMES = {
    'translate-into-save': 'Translate result written into save structure',
    'raw-name-in-display': 'Raw game name leaks into a display sink',
}
CATEGORY_EMOJI = {'translate-into-save': '💥', 'raw-name-in-display': '⚠️'}
CATEGORY_SEVERITY = {'translate-into-save': 'error', 'raw-name-in-display': 'warning'}


# ══════════════════════════════════════════════════════════════════
#  Data
# ══════════════════════════════════════════════════════════════════

@dataclass
class Violation:
    file_path: Path
    line: int
    col: int
    category: str
    severity: str
    message: str
    snippet: str


@dataclass
class ScanResult:
    violations: List[Violation] = field(default_factory=list)

    @property
    def errors(self) -> List[Violation]:
        return [v for v in self.violations if v.severity == 'error']

    @property
    def warnings(self) -> List[Violation]:
        return [v for v in self.violations if v.severity == 'warning']

    def merge(self, other: 'ScanResult') -> None:
        self.violations.extend(other.violations)


# ══════════════════════════════════════════════════════════════════
#  AST helpers
# ══════════════════════════════════════════════════════════════════

def func_name(node) -> Optional[str]:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def name_key(node) -> Optional[str]:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def is_translate_call(node) -> bool:
    return isinstance(node, ast.Call) and func_name(node.func) in TRANSLATE_FUNCS


def is_taint(node, taint: Set[str]) -> bool:
    """True if the expression is (or derives from) an untranslated raw game name."""
    if node is None:
        return False
    if isinstance(node, ast.Call):
        fn = func_name(node.func)
        if fn in TAINT_RESOLVER_NAMES or fn in TAINT_PASSTHROUGH_NAMES:
            return True
        # map.get(key)  where map is a known raw-name map
        if fn == 'get' and isinstance(node.func, ast.Attribute) \
                and name_key(node.func.value) in TAINT_MAP_NAMES:
            return True
        # don't propagate through general calls (avoids str(x)/format(x) FPs)
        return False
    if isinstance(node, ast.Subscript):
        if name_key(node.value) in TAINT_MAP_NAMES:
            return True
        return is_taint(node.value, taint)
    if isinstance(node, (ast.Name, ast.Attribute)):
        return name_key(node) in taint
    if isinstance(node, ast.BoolOp):
        # Python `or`/`and` — e.g. resolve_name(cid, _NAMEMAP) or cid
        return any(is_taint(v, taint) for v in node.values)
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Or, ast.And)):
        return is_taint(node.left, taint) or is_taint(node.right, taint)
    if isinstance(node, ast.IfExp):
        return is_taint(node.body, taint) or is_taint(node.orelse, taint)
    if isinstance(node, ast.JoinedStr):
        return any(
            is_taint(v.value, taint)
            for v in node.values
            if isinstance(v, ast.FormattedValue)
        )
    return False


def _target_names(tgt) -> List[str]:
    out: List[str] = []
    if isinstance(tgt, ast.Name):
        out.append(tgt.id)
    elif isinstance(tgt, (ast.Tuple, ast.List)):
        for e in tgt.elts:
            out.extend(_target_names(e))
    return out


def collect_taint(func_node) -> Set[str]:
    """Fixpoint: mark vars whose value is a raw-name source / tainted var."""
    assigns = [n for n in ast.walk(func_node)
               if isinstance(n, (ast.Assign, ast.AnnAssign))]
    taint: Set[str] = set()
    changed = True
    while changed:
        changed = False
        for a in assigns:
            val = a.value
            if val is None or not is_taint(val, taint):
                continue
            targets = a.targets if isinstance(a, ast.Assign) else ([a.target] if a.target else [])
            for tgt in targets:
                for nm in _target_names(tgt):
                    if nm not in taint:
                        taint.add(nm)
                        changed = True
    return taint


def target_is_save_bound(tgt) -> bool:
    toks: List[str] = []
    node = tgt
    while isinstance(node, (ast.Attribute, ast.Subscript)):
        if isinstance(node, ast.Attribute):
            toks.append(node.attr)
            node = node.value
        else:
            sl = node.slice
            if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
                toks.append(sl.value)
            node = node.value
    if isinstance(node, ast.Name):
        toks.append(node.id)
    return any(tok in SAVE_TARGET_TOKENS for tok in toks)


# ══════════════════════════════════════════════════════════════════
#  Scanning
# ══════════════════════════════════════════════════════════════════

def scan_function(func, file_path: Path, lines: List[str], result: ScanResult) -> None:
    taint = collect_taint(func)
    for node in ast.walk(func):
        if not isinstance(node, ast.Call):
            continue
        fn = func_name(node.func)

        # --- constructor sinks ---
        if fn in CTOR_SINKS:
            if not node.args:
                continue
            arg = node.args[0]
            if isinstance(arg, ast.Name) and arg.id == 'self':
                continue
            if isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name) and arg.value.id == 'self':
                continue
            if isinstance(arg, ast.Call):  # a widget/parent, not text
                continue
            if is_taint(arg, taint):
                _add(result, file_path, node.lineno, node.col_offset,
                     'raw-name-in-display',
                     f'{fn}() shows a raw (untranslated) game name',
                     _snippet(lines, node.lineno))

        # --- method sinks ---
        elif fn in METHOD_SINKS:
            idx = METHOD_SINKS[fn]
            if idx == -1:
                idx = 1 if len(node.args) >= 2 else 0
            if len(node.args) <= idx:
                continue
            arg = node.args[idx]
            if is_taint(arg, taint):
                _add(result, file_path, node.lineno, node.col_offset,
                     'raw-name-in-display',
                     f'.{fn}() shows a raw (untranslated) game name',
                     _snippet(lines, node.lineno))

        # --- t() interpolation sinks ---
        # t(key, name=TAINTED) injects a raw game name into a *translated*
        # template, so the rendered sentence still shows English. Only keyword
        # args are checked (the 1st positional is the key, the 2nd positional
        # is the intended raw fallback). e.g. t('rename_x', name=pal_name).
        elif fn == 't':
            for kw in node.keywords:
                if kw.arg is None:  # **kwargs splat — cannot reason, skip
                    continue
                if is_taint(kw.value, taint):
                    _add(result, file_path, node.lineno, node.col_offset,
                         'raw-name-in-display',
                         f't() interpolates a raw (untranslated) game name via "{kw.arg}="',
                         _snippet(lines, node.lineno))


def scan_translate_into_save(tree, file_path: Path, lines: List[str], result: ScanResult) -> None:
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and is_translate_call(node.value):
            for tgt in node.targets:
                if target_is_save_bound(tgt):
                    _add(result, file_path, node.lineno, node.col_offset,
                         'translate-into-save',
                         'translation result assigned into a save-bound structure',
                         _snippet(lines, node.lineno))


def _snippet(lines: List[str], lineno: int) -> str:
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1].strip()[:120]
    return ''


def _add(result: ScanResult, fp: Path, line: int, col: int, cat: str, msg: str, snip: str) -> None:
    for v in result.violations:
        if v.file_path == fp and v.line == line and v.category == cat and v.message == msg:
            return
    result.violations.append(Violation(
        file_path=fp, line=line, col=col, category=cat,
        severity=CATEGORY_SEVERITY[cat], message=msg, snippet=snip,
    ))


def scan_file(file_path: Path, root: Path) -> ScanResult:
    result = ScanResult()
    try:
        src = file_path.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return result
    lines = src.splitlines()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return result

    scan_translate_into_save(tree, file_path, lines, result)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            scan_function(node, file_path, lines, result)
    return result


def scan_directory(root: Path, excludes: List[str]) -> ScanResult:
    result = ScanResult()
    for py_file in sorted(root.rglob('*.py')):
        rel = str(py_file.relative_to(root))
        if any(rel == e.rstrip('/') or rel.startswith(e.rstrip('/') + '/') for e in excludes):
            continue
        result.merge(scan_file(py_file, root))
    return result


# ══════════════════════════════════════════════════════════════════
#  Reporting
# ══════════════════════════════════════════════════════════════════

def _plural(n: int, word: str) -> str:
    return f'{n} {word}{"s" if n != 1 else ""}'


def print_report(result: ScanResult, root: Path, *, verbose: bool = False) -> None:
    if not result.violations:
        print()
        print(f'  {GREEN(BOLD("✓ PASS — No translation violations found!"))}')
        print(f'  {DIM("  No raw game names leak into UI, and no translation writes into saves.")}')
        print()
        return

    by_file: Dict[Path, List[Violation]] = defaultdict(list)
    by_cat: Dict[str, int] = defaultdict(int)
    for v in result.violations:
        by_file[v.file_path].append(v)
        by_cat[v.category] += 1

    n_err = len(result.errors)
    n_wrn = len(result.warnings)
    n_tot = len(result.violations)
    n_fls = len(by_file)

    print()
    print(f'  {RED(BOLD(f"✗ FAIL — {_plural(n_tot, "violation")} found across {_plural(n_fls, "file")}"))}')
    sev = ''
    if n_err:
        sev += RED(f'{n_err} error{"s" if n_err != 1 else ""}')
    if n_err and n_wrn:
        sev += ', '
    if n_wrn:
        sev += YELLOW(f'{n_wrn} warning{"s" if n_wrn != 1 else ""}')
    print(f'  {DIM(sev)}')
    print()

    print(f'  {BOLD("Breakdown by type")}')
    for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        emoji = CATEGORY_EMOJI.get(cat, '•')
        name = CATEGORY_NAMES.get(cat, cat)
        color = RED if CATEGORY_SEVERITY.get(cat) == 'error' else YELLOW
        print(f'    {emoji} {color(name):45s} {BOLD(str(count))}')
    print()

    print(f'  {BOLD("Per-file details")}')
    for fpath, violations in sorted(by_file.items()):
        rel = str(fpath.relative_to(root))
        print(f'\n  {CYAN(rel)}')
        for v in sorted(violations, key=lambda x: x.line):
            marker = RED('✗') if v.severity == 'error' else YELLOW('⚠')
            cat_name = CATEGORY_NAMES.get(v.category, v.category)
            loc = DIM(f'L{v.line}')
            print(f'    {marker} {cat_name:45s} {loc}  {v.message}')
            if verbose:
                print(f'         {DIM(v.snippet[:110])}')
    print()


# ══════════════════════════════════════════════════════════════════
#  CLI
# ══════════════════════════════════════════════════════════════════

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description='Find raw game names leaking into UI and translation-into-save bugs.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--root', type=Path, default=Path('src'),
                        help='Directory to scan (default: src/)')
    parser.add_argument('--strict', action='store_true',
                        help='Treat warnings as errors — fail on anything')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show the actual code line for each violation')
    parser.add_argument('--exclude', action='append', default=[],
                        help='Skip files/directories (repeatable)')
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        print(f'Error: {root} is not a directory', file=sys.stderr)
        return 2

    excludes = list(DEFAULT_EXCLUDES) + args.exclude
    result = scan_directory(root, excludes)
    print_report(result, root, verbose=args.verbose)

    if not result.violations:
        return 0
    if args.strict:
        return 1
    return 1 if result.errors else 0


if __name__ == '__main__':
    sys.exit(main())
