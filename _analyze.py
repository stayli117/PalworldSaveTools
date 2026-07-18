import json, re

with open(r'C:\Users\Administrator\Desktop\PalworldStuff\PalworldSaveTools\resources\game_data\skills.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

passives = data['passives']
total = len(passives)

# L10N
with open(r'C:\Users\Administrator\Desktop\PalworldStuff\PalworldSaveTools\Exports\Pal\Content\L10N\en\Pal\DataTable\Text\DT_SkillNameText_Common.json', 'r', encoding='utf-8') as f:
    l10n = json.load(f)
l10n_rows = l10n[0]['Rows']
l10n_passive_keys = set(k for k in l10n_rows if k.startswith('PASSIVE_'))
l10n_partnerskill_keys = set(k for k in l10n_rows if k.startswith('PARTNERSKILL_'))

has_loc = [p for p in passives if 'localized' in p and p['localized']]
no_loc = [p for p in passives if 'localized' not in p or not p['localized']]

print("=== LOCALIZED passives (488) naming patterns ===")
l_pat = {}
for p in has_loc:
    n = p['name']
    if re.search(r'_\d+$', n):
        l_pat['numeric_suffix'] = l_pat.get('numeric_suffix', 0) + 1
    elif '_PartnerSkill' in n:
        l_pat['contains_PartnerSkill'] = l_pat.get('contains_PartnerSkill', 0) + 1
    else:
        l_pat['base_name'] = l_pat.get('base_name', 0) + 1
for pat,cnt in sorted(l_pat.items(), key=lambda x:-x[1]):
    print(f'  {pat}: {cnt}')

# Check: do localized names map DIRECTLY to L10N PASSIVE_ keys?
# If name is X, does PASSIVE_X exist in L10N?
direct_match = 0
for p in has_loc:
    key = 'PASSIVE_' + p['name']
    if key in l10n_passive_keys:
        direct_match += 1
    else:
        pass  # will check below
print('\n=== Direct L10N match (PASSIVE_<name>) ===')
print(f'  Direct match: {direct_match}')
print(f'  Non-match: {len(has_loc) - direct_match}')

# For non-matching localized ones, print a few
for p in has_loc:
    key = 'PASSIVE_' + p['name']
    if key not in l10n_passive_keys:
        print(f'  LOCALIZED but NOT in L10N: {p["name"]} -> need PASSIVE_{p["name"]}')
        break

# Show a few that DO match
print('\n--- Localized names that DO match L10N ---')
for p in has_loc[:5]:
    key = 'PASSIVE_' + p['name']
    in_l10n = key in l10n_passive_keys
    print(f'  {p["name"]} -> PASSIVE_{p["name"]} in L10N: {in_l10n}')

# For the 1245 numeric-suffix missing ones, check if stripping suffix maps to L10N
print('\n=== Can numeric-suffix missing ones map to L10N by stripping suffix? ===')
numeric_missing = [p for p in no_loc if re.search(r'_\d+$', p['name'])]
strippable = 0
unstrippable = 0
stripped_map = {}
for p in numeric_missing:
    n = p['name']
    base = re.sub(r'_\d+$', '', n)
    l10n_key = 'PASSIVE_' + base
    if l10n_key in l10n_passive_keys:
        strippable += 1
        stripped_map.setdefault(base, []).append(n)
    else:
        unstrippable += 1

print(f'  Numeric-suffix missing: {len(numeric_missing)}')
print(f'  Strippable to PASSIVE_<base> in L10N: {strippable}')
print(f'  NOT strippable: {unstrippable}')

# Show a few examples
print('\n--- Strippable examples ---')
for base, variants in list(stripped_map.items())[:5]:
    print(f'  {base} (L10N: YES) -> variants: {variants[:5]}')

# Show the unstrippable ones
unstrippable_passives = [p for p in numeric_missing if re.sub(r'_\d+$', '', p['name']) + ' not in L10N condition fails, need manual']
print('\n--- Unstrippable examples ---')
shown = 0
for p in numeric_missing:
    n = p['name']
    base = re.sub(r'_\d+$', '', n)
    l10n_key = 'PASSIVE_' + base
    if l10n_key not in l10n_passive_keys:
        print(f'  {n} -> strip to {base} but PASSIVE_{base} NOT in L10N')
        shown += 1
        if shown >= 10:
            break

# Check PARTNERSKILL in L10N for partner skill passives
print('\n=== PartnerSkill passives in L10N ===')
print(f'  PARTNERSKILL_ entries in L10N: {len(l10n_partnerskill_keys)}')
ps_missing = [p for p in no_loc if '_PartnerSkill' in p['name']]
print(f'  Missing passives with _PartnerSkill: {len(ps_missing)}')
for p in ps_missing[:10]:
    # Try stripping the _N suffix too
    n = p['name']

    # Try different L10N key patterns
    key1 = 'PASSIVE_' + n
    key2 = 'PARTNERSKILL_' + n
    found = 'PASSIVE_' + n in l10n_passive_keys or 'PARTNERSKILL_' + n in l10n_partnerskill_keys
    print(f'  {n} -> PASSIVE_{n} in L10N: {key1 in l10n_passive_keys}, PARTNERSKILL_{n} in L10N: {key2 in l10n_partnerskill_keys}')

# Check the "other" missing (not numeric, not partner)
print('\n=== Other missing passives (150) — L10N lookup ===')
other_missing = [p for p in no_loc if not re.search(r'_\d+$', p['name']) and '_PartnerSkill' not in p['name']]
for p in other_missing[:15]:
    n = p['name']
    key = 'PASSIVE_' + n
    print(f'  {n} -> PASSIVE_{n} in L10N: {key in l10n_passive_keys}')

# Check: what L10N PASSIVE_ keys DON'T match any passive name?
print('\n=== L10N PASSIVE_ keys with NO matching passive ===')
l10n_names = {k.replace('PASSIVE_', '') for k in l10n_passive_keys}
passive_names = {p['name'] for p in passives}
unmatched_l10n = l10n_names - passive_names
print(f'  PASSIVE_ keys with no matching passive in skills.json: {len(unmatched_l10n)}')
for k in sorted(unmatched_l10n)[:20]:
    print(f'    PASSIVE_{k}')
