from __future__ import annotations
import hashlib
import os
import sys
from typing import Dict, Any
from palsav import json_tools

from resource_resolver import get_base_dir, get_resources_dir, get_user_config_dir
base_dir = get_base_dir()
_CFG: str = os.path.join(get_user_config_dir(), 'config.json')
_BUNDLED_CFG: str = os.path.join(base_dir, 'src', 'data', 'configs', 'config.json')
_SUPPORTED_LANGS = ['en_US', 'zh_CN', 'ru_RU', 'fr_FR', 'es_ES', 'de_DE', 'ja_JP', 'ko_KR', 'pt_BR']
_cfg_path = _CFG if os.path.exists(_CFG) else _BUNDLED_CFG
try:
    _LANG: str = json_tools.load(_cfg_path).get('lang', 'en_US') if os.path.exists(_cfg_path) else 'en_US'
except Exception:
    _LANG: str = 'en_US'
_RES: Dict[str, Dict[str, str]] = {}
_loaded_langs: set = set()


_RESOURCES_DIR_CACHE: str | None = None


def _get_resources_dir() -> str:
    """获取 resources 目录。

    优先使用 boot_paths.RESOURCES_DIR（由 __file__ 探测，路径可靠且不依赖
    sys.executable）；若 boot_paths 尚未导入，则回退到 resource_resolver。
    同时保证 resources 目录在 sys.path 中，供翻译键加载。
    """
    global _RESOURCES_DIR_CACHE
    if _RESOURCES_DIR_CACHE is None:
        try:
            from boot_paths import RESOURCES_DIR
            r = str(RESOURCES_DIR)
        except Exception:
            r = get_resources_dir()
        _RESOURCES_DIR_CACHE = r
        if _RESOURCES_DIR_CACHE not in sys.path:
            sys.path.insert(0, _RESOURCES_DIR_CACHE)
    return _RESOURCES_DIR_CACHE


def _load_json(path: str) -> Dict[str, Any]:
    try:
        return json_tools.load(path)
    except Exception:
        return {}


def _get_i18n_path(lang: str) -> str:
    """获取 i18n 翻译文件路径，延迟解析 resources 目录"""
    return os.path.join(_get_resources_dir(), 'i18n', f'{lang}.json')


def _ensure_lang(lang: str) -> None:
    if lang not in _loaded_langs:
        _RES[lang] = _load_json(_get_i18n_path(lang))
        _loaded_langs.add(lang)


def load_resources(lang: str | None=None) -> None:
    global _RES, _LANG, _loaded_langs
    _loaded_langs.clear()
    for l in _SUPPORTED_LANGS:
        _RES[l] = _load_json(_get_i18n_path(l))
        _loaded_langs.add(l)
    if lang:
        _LANG = lang


def get_language() -> str:
    return _LANG


def set_language(lang: str) -> None:
    global _LANG
    if lang not in _SUPPORTED_LANGS:
        return
    _ensure_lang(lang)
    # 确保 en_US 已加载，作为 fallback
    if 'en_US' not in _loaded_langs:
        _ensure_lang('en_US')
    _LANG = lang
    try:
        os.makedirs(os.path.dirname(_CFG), exist_ok=True)
        cfg = _load_json(_CFG) if os.path.exists(_CFG) else {}
        cfg['lang'] = lang
        json_tools.dump(cfg, _CFG)
    except Exception:
        pass


def get_config_value(key: str, default: Any=None) -> Any:
    cfg_path = _CFG if os.path.exists(_CFG) else _BUNDLED_CFG
    if os.path.exists(cfg_path):
        cfg = _load_json(cfg_path)
        return cfg.get(key, default)
    return default


def set_config_value(key: str, value: Any) -> None:
    try:
        os.makedirs(os.path.dirname(_CFG), exist_ok=True)
        cfg = _load_json(_CFG) if os.path.exists(_CFG) else {}
        cfg[key] = value
        json_tools.dump(cfg, _CFG)
    except Exception:
        pass


def init_language(default_lang: str='zh_CN') -> None:
    global _RES, _LANG, _loaded_langs
    lang = default_lang
    cfg_path = _CFG if os.path.exists(_CFG) else _BUNDLED_CFG
    if os.path.exists(cfg_path):
        cfg = _load_json(cfg_path)
        lang = cfg.get('lang', default_lang)
    # 只加载当前语言 + en_US 作为 fallback，其他语言在 set_language() 切换时按需加载
    _ensure_lang(lang)
    if lang != 'en_US':
        _ensure_lang('en_US')
    _LANG = lang


_DEF = object()

def get_native_lang_name(code: str) -> str:
    _ensure_lang('en_US')
    return _RES.get('en_US', {}).get(f'lang.{code}', code)

def t(key: str, default: str | object=_DEF, **fmt) -> str:
    src = _RES.get(_LANG, {})
    fallback = _RES.get('en_US', {})
    text = src.get(key) or fallback.get(key)
    if text is None:
        text = key if default is _DEF else default
    try:
        return text.format(**fmt) if fmt else text
    except Exception:
        return text


def desc_t(category: str, text: str | None, default: str | None = None) -> str:
    """翻译游戏数据的「描述/介绍」长文本（物品、技能、被动、帕鲁、科技、结构等）。

    描述文本是自由文本，无法用固定键枚举，因此以「分类 + 描述文本哈希」为键，
    存入 resources/i18n/zh_CN.json（形如 desc.item.a1b2c3d4e5f6）。
    命中则返回中文，未命中则回退英文原文（default 优先，否则原样返回）。

    被动技能描述含 {CharacterName}/{EffectValueN} 令牌，翻译时已保留，调用方拿到
    中文模板后需自行做令牌替换。
    """
    if not text:
        return default if default is not None else (text or '')
    norm = text.replace('\r', '').strip()
    if not norm:
        return default if default is not None else (text or '')
    h = hashlib.md5(norm.encode('utf-8')).hexdigest()[:12]
    key = f"desc.{category}.{h}"
    fallback = text if default is None else default
    return t(key, fallback)


__all__ = ['init_language', 't', 'set_language', 'get_language', 'load_resources', 'desc_t', 'get_native_lang_name']
