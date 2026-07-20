import json
import os
import sys
import concurrent.futures
from pathlib import Path
try:
    from deep_translator import GoogleTranslator
except ImportError:
    print('Installing deep-translator...')
    import subprocess
    subprocess.check_call(['uv', 'pip', 'install', 'deep-translator'])
    from deep_translator import GoogleTranslator
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LANGUAGES = {'zh_CN': {'name': 'Simplified Chinese', 'code': 'zh-CN'}, 'de_DE': {'name': 'German', 'code': 'de'}, 'es_ES': {'name': 'Spanish', 'code': 'es'}, 'fr_FR': {'name': 'French', 'code': 'fr'}, 'ru_RU': {'name': 'Russian', 'code': 'ru'}, 'ja_JP': {'name': 'Japanese', 'code': 'ja'}, 'ko_KR': {'name': 'Korean', 'code': 'ko'}, 'pt_BR': {'name': 'Portuguese (Brazil)', 'code': 'pt'}}
NEW_TRANSLATIONS = {
    'character_transfer.unsaved_warning': 'You have unsaved transfers. Save before exiting?',
    'pal_editor.multi_selected': '{n} pals selected',
    'pal_editor.bulk_max_btn': 'Max',
    'pal_editor.bulk_heal_btn': 'Heal',
    'pal_editor.bulk_rename_btn': 'Rename',
    'pal_editor.bulk_delete_btn': 'Delete',
    'pal_editor.bulk_deselect_btn': 'Deselect',
    'pal_editor.bulk_rename_title': 'Rename Pals',
    'pal_editor.bulk_rename_label': 'Enter a nickname for all selected pals:',
    'pal_editor.bulk_rename_placeholder': 'Nickname...',
    'pal_editor.bulk_rename_cancel': 'Cancel',
    'pal_editor.bulk_rename_apply': 'Apply',
    'pal_editor.bulk_rename_no_name': 'Please enter a nickname.',
    'pal_editor.bulk_rename_done': 'Renamed {n} pals to {name}',
    'pal_editor.bulk_delete_title': 'Delete',
    'pal_editor.bulk_delete_confirm': 'Delete {n} selected pals?',
    'pal_editor.bulk_delete_success': 'Deleted {n} pals',
    'pal_editor.bulk_max_success': 'Maxed {n} pals',
    'pal_editor.bulk_heal_done': 'Healed {n} pals',
}
OLD_KEYS = []
def _clean_uv_locks():
    for p in [Path.cwd() / 'uv.lock', PROJECT_ROOT / 'uv.lock']:
        if p.exists():
            p.unlink()
def remove_old_keys_from_all():
    for lang_code in list(LANGUAGES.keys()) + ['en_US']:
        lang_file = PROJECT_ROOT / 'resources' / 'i18n' / f'{lang_code}.json'
        if not lang_file.exists():
            continue
        with open(lang_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        removed = [key for key in OLD_KEYS if data.pop(key, None) is not None]
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if removed:
            print(f'  {lang_code}: removed {len(removed)} keys')
def add_english_keys():
    lang_file = PROJECT_ROOT / 'resources' / 'i18n' / 'en_US.json'
    with open(lang_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for key, english_text in NEW_TRANSLATIONS.items():
        data[key] = english_text
    with open(lang_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def translate_text(text: str, target_lang: str) -> str:
    import re
    placeholders = re.findall(r'\{[^}]+\}', text)
    protected = text
    tokens = {}
    for i, ph in enumerate(placeholders):
        tok = f'__PH{i}__'
        tokens[tok] = ph
        protected = protected.replace(ph, tok, 1)
    translator = GoogleTranslator(source='en', target=target_lang)
    translated = translator.translate(protected)
    for tok, ph in tokens.items():
        translated = translated.replace(tok, ph)
    return translated
def add_keys_to_language(lang_code: str, lang_info: dict) -> bool:
    try:
        lang_file = PROJECT_ROOT / 'resources' / 'i18n' / f'{lang_code}.json'
        with open(lang_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        had_failure = False
        for key, english_text in NEW_TRANSLATIONS.items():
            try:
                translated = translate_text(english_text, lang_info['code'])
                data[key] = translated
            except Exception as e:
                print(f'  [WARN] {key}: translate failed ({e}), using English fallback')
                data[key] = english_text
                had_failure = True
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return not had_failure
    except Exception as e:
        print(f'  [ERROR] File-level failure: {e}')
        return False
def main():
    _clean_uv_locks()
    print('\n' + '=' * 60)
    print('  UPDATING TRANSLATION KEYS')
    print('=' * 60)
    print('\nRemoving old keys...')
    remove_old_keys_from_all()
    print('\nEnglish (en_US)...')
    add_english_keys()
    print('  [OK] Success')
    print('\nTranslating to other languages (parallel processing)...')
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(LANGUAGES)) as executor:
        future_to_lang = {executor.submit(add_keys_to_language, lang_code, lang_info): lang_code for lang_code, lang_info in LANGUAGES.items()}
        for future in concurrent.futures.as_completed(future_to_lang):
            lang_code = future_to_lang[future]
            lang_info = LANGUAGES[lang_code]
            try:
                success = future.result()
                print(f"  {lang_info['name']} ({lang_code}): {('[OK] Success' if success else '[ERROR] Failed')}")
            except Exception as e:
                print(f"  {lang_info['name']} ({lang_code}): [ERROR] {e}")
    _clean_uv_locks()
    print('\n' + '=' * 60)
    print('  DONE')
    print('=' * 60)
if __name__ == '__main__':
    main()
