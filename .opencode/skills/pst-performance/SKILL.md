# pst-performance — Performance optimization patterns for PST

Load when touching any code that iterates CharacterSaveParameterMap, ItemContainerSaveData, DynamicItemSaveData, calls `add_item()`, `save()`, or processes per-player operations in loops.

## Core anti-patterns to flag

### 1. save() called per item in a loop

`PlayerInventory.add_item()` calls `self.save()` internally, which scans **ALL ItemContainerSaveData** in `loaded_level_json` + calls `sync_dynamic_items_with_registry`. Each scan is O(N_world_containers).

**WRONG:**
```python
for item_id in missing_items:
    inv.add_item('key', item_id, 1)  # save() per iteration
```

**RIGHT:**
```python
std_container = inv.get_container('key')._standardized_container
for item_id in missing_items:
    std_container.add_item(item_id, 1)  # pure in-memory, no save
inv.save()  # one save after loop
```

`StandardizedContainer.add_item()` at `standardized_container.py:118` is pure in-memory. No save, no disk I/O.

### 2. Linear char_map scan inside per-slot loop

Iterating CharacterSaveParameterMap with `next((c for c in char_map if ...))` inside a loop over slots creates O(slots × char_map) complexity.

**WRONG:**
```python
for slot in slots:
    ch = next((c for c in char_map if c['key']['InstanceId']['value'] == slot_id), None)
```

**RIGHT:**
```python
instance_lookup = {str(e['key']['InstanceId']['value']): e for e in char_map}
for slot in slots:
    ch = instance_lookup.get(slot_id)
```

### 3. Scanning the same data source multiple times

Don't iterate `CharacterSaveParameterMap`, `GroupSaveDataMap`, or `ItemContainerSaveData` twice when one pass suffices.

**WRONG:** Two separate loops for nicknames + detection.
**RIGHT:** Merge conditions into one pass with `if/elif`.

**WRONG:** `_build_level_map()` + `_build_pal_count_map()` as separate functions.
**RIGHT:** Single `_build_maps()` returning `(level_map, pal_count_map)` tuple.

### 4. No caching for repeated JSON reads

If a function reads a JSON file from disk every call and is called often, add `@lru_cache` or a module-level cache dict.

**WRONG:** `load_game_data_map(fname, key)` reads `resources/game_data/{fname}` from disk every call.
**RIGHT:** `@lru_cache(maxsize=32)` on the function.

**WRONG:** `_load_boss_key_map()` reads `boss_mapping.json` every call.
**RIGHT:** Module-level `_BOSS_KEY_CACHE = None` with lazy init.

### 5. Rebuilding lookup dicts per player

If you iterate players and rebuild a dict from the same static data each iteration, lift the build outside.

**WRONG:**
```python
for uid in player_uids:
    container_lookup = {c['key']['ID']['value']: c for c in item_containers}
    ...
```

**RIGHT:**
```python
container_lookup = {c['key']['ID']['value']: c for c in item_containers}
for uid in player_uids:
    ...
```

### 6. Triple-nested container scans

Scanning all containers → all map objects → all modules per container. Build a reverse lookup dict first.

**WRONG:**
```python
for cont in item_containers:
    for obj in map_objects:
        for module in obj['ConcreteModel']['ModuleMap']['value']:
            ...
```

**RIGHT:**
```python
container_id_to_obj = {str(module.target_container_id): obj for obj in map_objects for module in ...}
for cont in item_containers:
    obj = container_id_to_obj.get(container_id)
```

### 7. Parallelizing independent per-player disk writes

Player .sav writes (Oodle compression) are CPU-heavy and file-independent. Use ThreadPoolExecutor with `max_workers=min(os.cpu_count() or 4, 8)`.

### 8. Non `PlayerInventory.load()` won't decode Level.sav

`PlayerInventory.load()` at `inventory_manager.py:405` only decodes the **per-player** .sav file. Level.sav data comes from `constants.loaded_level_json` (already in memory). Don't worry about Level.sav re-decodes — they don't happen in inventory operations.

## Key file locations

| File | Key functions |
|------|--------------|
| `inventory_manager.py:641` | `PlayerInventory.add_item()` — triggers `save()` |
| `inventory_manager.py:703` | `PlayerInventory.save()` — scans all world containers |
| `standardized_container.py:118` | `StandardizedContainer.add_item()` — safe for loops (no save) |
| `loading_manager.py` | `run_with_loading()` — used for async UI tasks |
| `character_transfer.py:612` | `migrate_inventory_via_player_inventory` — has the loop-save pattern |
| `character_transfer.py:1040` | `gather_and_update_dynamic_containers` — build reverse lookup dicts |

## DPS file performance — known bottleneck

DPS files (`*_dps.sav`) use the same GVAS SaveParameterArray as the main save, but lack the CharacterSaveParameterMap skip optimization. For a 294KB compressed / 77MB decompressed file with 9600 entries:

| Phase | Time | % of total |
|-------|------|-----------|
| Decompress (Oodle) | 21ms | 0.5% |
| GvasFile.read (SKP) | 2812ms | 60% |
| Iterate CIDs | 9ms | 0.2% |
| GvasFile.write (SKP) | 1744ms | 37% |
| Compress (Oodle) | 96ms | 2% |
| **Total** | **4683ms** | |

The ~2.8s read + ~1.7s write is from 9600× `properties_until_end()` calls inside `archive.py:array_property()` → `struct_value()` → `properties_until_end()`. Each entry has ~30 properties; each property requires 2 fstring reads (name + type) + 1 u64 read (size) + type-specific decode.

**The shared struct header** (array_property at archive.py:337-353) means elements share one `prop_name`/`prop_type`/`type_name`/`guid` for ALL entries, then a `struct_value()` call per entry. Individual element boundaries are delimited by `'None'` terminators, not by precomputed sizes, making per-element raw byte extraction without full parsing impossible at the archive layer.

**What already works:** SKP_PALWORLD_CUSTOM_PROPERTIES skips `SaveParameter.SaveParameter.RawData` for each entry (opaque bytes instead of sub-property tree). This saves ~800ms on read but the outer property headers still parse.

**What would require GVAS parser changes:** Adding struct-level skip support to `archive.py:struct_value()` — checking `custom_properties` before calling `properties_until_end()`. This would require either (a) precomputed element sizes via terminator scanning, or (b) a batch read-ahead that counts 'None' boundaries. Both are invasive changes to the core archive reader.

**Pragmatic workaround for bulk DPS operations:**
- `pal_editor_global_ops.py` loads every DPS file serially in a for loop. Wrap in ThreadPoolExecutor for parallel file processing.
- Limit DPS operations to current player's file when possible (avoid scanning all players' DPS files).

