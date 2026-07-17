#2.1.3
- **Loading screen overhaul** — the loading screen can no longer hang or get stuck. Completely rewrote the animation system — it now runs in its own background process, so even if a save operation takes long, the loading window stays smooth and responsive.
- **Loading screens added to more tools** — Convert Save Files, Restore Map (both Steam and GamePass), and the Player Inventory Max All Stats button now show a loading screen during heavy work instead of freezing up.
- **Nested loading conflict fixed** — using menu functions like Max All Pals while the Pal Editor is open no longer spawns multiple overlapping loading screens that break the UI.
- **Lazy tab crash fix** — menu operations no longer crash when you haven't visited certain tabs yet. The app skips cache updates on tabs that haven't been opened, and those tabs load fresh data when you first visit them.
- **Pal editor toggle tooltips** — all toggle buttons in the info panel (Gender, Predator, Boss, Lucky, and more) now show helpful tooltips on hover, translated into all supported languages.
- **Backup now includes more save files** — automatic backups also save WorldOption.sav and LocalData.sav, not just Level.sav and players. Backup folders inside your save are automatically skipped.
- **Game version tooltip** — hovering over the game version label in the header shows the current Palworld version, in all languages.
- **Stream support in palsav json_tools** — save files can now be read and written directly from memory streams, not just file paths. By msansen.
- **Load from Backup** — new File menu option that lists all your auto-backups with timestamp, world name, and player count, so you can easily restore any previous save state.
- **Cheat mode condensed stars capped** — the condenser rank (stars) is now limited to 5 even in cheat mode, since higher values cause glitches in-game. Cheat mode still unlocks other caps like IVs, souls, and level.
- Bumped version to 2.1.3

#2.1.2
- **DPS loading speedup** — `RawData` field inside `SaveParameterArray.SaveParameter` now uses skip-decode in GUI path. Saves ~19ms + ~27MB memory for 9600-pal DPS files. Pal editor still accesses all 30+ other fields normally (CharacterID, Level, PassiveSkillList, talents, etc.). Bottleneck identified: remaining ~400-700ms is `properties_until_end` called 9600× per file — a custom batch decoder would be needed for sub-200ms load times.
- **Restore Map fix** — tool now reads the real Steam/macOS save path (`%LOCALAPPDATA%/Pal/Saved/SaveGames`) instead of the config `last_save_path`, so it finds your actual save folders again. Also handles flat save directories (LocalData.sav in root) in addition to the nested Steam structure
- **Convert Save files fix** — no longer hangs or silently fails; work runs directly instead of through a daemon thread that never starts inside `QEventLoop.exec()`
- **Tab switching performance** — navigating to a lazy-loaded tab no longer refreshes every single tab; only the target tab repopulates. Removed a redundant double-refresh of the base inventory tab on save load
- **macOS trackpad phantom scroll fix** — right-clicking (two-finger tap) on empty grid space in pal editor or base inventory no longer kicks you back pages. Zero-delta scroll events from macOS gesture synthesis now pass through instead of triggering page navigation
- **Linux save path support** — `get_steam_save_path()` now resolves Proton save location (`~/.local/share/Steam/.../SaveGames`). Restore Map works on all 3 platforms
- **Loading overlay on player select** — selecting a player in Player Inventory or Pal Editor now shows the animated loading overlay for the entire operation: both tabs' data (inventory + pals) load simultaneously in the background, then both UIs update at once when the overlay dismisses. Cross-tab player selection sync is instant and works on first use (Player Inventory and Pal Editor tabs are no longer lazily deferred).
- **DPS button visibility** — the DPS mode button in Pal Editor now only shows when the selected player actually has a DPS save file. No more clicking a useless button
- **Loading overlay on base import/export/clone** — importing, exporting, and cloning bases now shows the animated loading overlay instead of a frozen wait cursor. Single-base export, bulk guild export, and multi-file import all wrapped with background progress.
- **Clone base in map viewer** — right-click any base marker and pick "Clone Base" to duplicate it in the same guild with the loading overlay. The clone spawns near the original.
- **Loading overlay on XGP save load** — the entire GamePass save extraction and decoding now runs under the animated overlay instead of freezing the UI during container blob reads.
- **GamePass save error dialogs** — the save picker and Steam↔GamePass converter now show clear error dialogs when no saves are found or saves can't be parsed, with suggestions to log into the world on Xbox Game Pass and update to the latest Palworld version.
- **Bulk Clone/Delete pals** — new "Bulk Clone" and "Bulk Delete" buttons in the Pal Editor header. Opens a species-picker dialog with Party/Palbox/DPS source toggles, search, and per-species quantity (clone) or select-all (delete). Clone mode shows available free slots and caps copies accordingly. Both operations run under the loading overlay.
- Bumped version to 2.1.2

#2.1.1
- **Character Transfer: dynamic data loss fix** — restored 3 orphaned fixes from `feat/av-hardened-nuitka-build` that were never merged to main. Container slots now scan both `ItemContainerSaveData` and `CharacterContainerSaveData` for in-use dynamic IDs before merging. Session-level dedup prevents duplicate entries on repeated transfers. ID remapping accumulates across multi-player sessions so slot references stay consistent. When a source dynamic ID collides with an in-use target ID, a new unique ID is generated and all container slot references are rewritten to match
- **Repair All Items** — menu function that regenerates all weapons, armor, and eggs across every container (player inventories, base chests, guild storage, etc.) with fresh IDs and max durability. Fixes corrupted durability data, missing dynamic entries, or any item that needs a full refresh
- **NPC/pal discrimination fix** — monster-row-based pal detection; NPCs no longer leak into pal pickers, breeding lists, or pal search/delete dialogs. Pal pickers source from `_PALMAP` instead of `_NAMEMAP` so generic Human/NPC templates are excluded
- **Breeding picker cleanup** — candidates sourced directly from `breedingdata.json` pal_info instead of merged npc list. Manual prefix/otomo/zukan-index dedup heuristics removed (superseded by game data)
- **Convert SteamID dialog** — starts empty instead of auto-fetching; no stale data shown before user action
- **Flamethrower gear fix** — items with empty descriptions now show correctly in pickers (no longer hidden)
- **DPS delete fix** — deleting a pal from DPS storage no longer causes infinite loading in-game. Slot data is fully cleared so the game correctly treats it as empty
- Bumped version to 2.1.1

#2.1.0
- **Faster startup** — app now loads ~2–4s faster by deferring heavy modules until needed. Language files load on demand, unused engine modules skip import, and non-visible tabs are created only when you navigate to them
- **Sidebar collapse/expand** — collapse shows icons only, expand reveals labels. Toggle button at top (>>/<<). State persists across sessions
- **Stats editor revamped** — hero stats (Health, Stamina, Attack, Work Speed, Weight) now show correct in-game computed values, capped at 50 points, with a "Max All Stats" button. Relic abilities integrated into the same tab. Defense stat now editable
- **Weight formula fix** — carry weight now calculates correctly using the game's real formula
- **Base move on map** — right-click a base marker, pick "Change Coordinates", then click any spot on the map to teleport the base. Warning dialog explains collision/terrain/AI risks
- **Base nudge** — nudge a base by exact X/Y/Z offsets to fix ground clipping or floating without needing to re-place it
- **Export/Import Pals** — right-click any pal to export as `.pstpal` (compressed) or `.json`. Import into empty slots in party, palbox, DPS, or base worker slots. Works across saves and players
- **Player context menu cleanup** — removed Edit Player Stats and Edit Tech Points (now handled in the Stats tab)
- **New translations** — player stat labels added to all 8 languages
- Bumped version to 2.1.0

#2.0.9
- Updated game data to palworld v1.0.1
- **Breeding formula fixes** — case-insensitive name/tribe mapping prevents missed pal parents; pals produced by unique breeding combos are excluded from the generic formula's candidate pool; `closest_pal()` tiebreaker picks higher combi-rank instead of rarity
- **macOS save path support** — new `get_steam_save_path()` resolves Steam saves on Windows (`%LOCALAPPDATA%\Pal\Saved\SaveGames`) and macOS (`~/Library/Containers/com.pocketpair.palworld.mac/.../SaveGames`); `get_preferred_save_path()` persists last-used directory across sessions in user config; `restore_map.py` no longer crashes on non-Windows
- Bumped version to 2.0.9

#2.0.8
- **Fixed `LocalData.sav` parsing** — `PalLocalWorldSaveGame` saves now load correctly (fixes parser under-consumption that skipped subsequent properties)
- **Bulk Sync (All Pals)** — sync stats/IVs/skills from any pal to all others across Party/Palbox/DPS. Work suitabilities are no longer copied cross-pal — each target keeps its natural suitabilities maxed to 10
- **Guild data fix** — `_u8_flag` → `role` migration prevents silent data loss on save
- **Fix Illegal Pals dialog** — per-player illegal pal counts, player selection, loading overlay, Select All/Deselect All
- **Restore Map** — also clears sky island cloud overlay so revealed map is fully visible
- **Fixed system32 crash** — all relative paths replaced with proper app data resolution; settings no longer lost in Nuitka onefile builds on restart
- **Open Data Folder** — menu item under AIO Tools opens app data directory in file manager
- **Removed auto-update** — kept version check + GitHub chip pulse; click still opens releases page
- **Work suitability icons** — fixed stale icon bug that let users inject illegal work suitabilities into any pal
- Bumped version to 2.0.8

#2.0.7
- **Per-item quantity cap** — non-stackable items (max_stack=1) stay limited to 1; all stackables uncapped to 999,999,999. Uses `max_stack` from generated game data
- **track user.cfg** — removed from `.gitignore`, now version-controlled
- **Abilities panel in Stats tab** — right side of Stats tab now shows relic abilities with toggles, icons, current values, and spinners. Supports edit and apply per player. Retranslates on language change
- **Translations: abilities keys** — added `inventory.abilities`, `inventory.abilities_apply`, `inventory.abilities_loaded`, `inventory.abilities_no_player_selected` in all 8 languages
- **NPC database expanded** — `update_npc_data()` now loads regular NPCs from `DT_PalCharacterIconDataTable.json` (not just boss NPCs). NPC count 33 → 369. Ammo Merchant and all trader/civilian variants now in DB
- **Sort no longer merges** — `_consolidate_container_slots` now just reorders by category/name. No stacking, no 9999 cap, gold and all items left untouched
- **Predator toggle** — paw icon button in pal editor info panel. Toggles `PREDATOR_` prefix. Filter toggle in Add New Pal and Bulk Pal Management dialogs. Red paw badge on thumbnail cards
- **Cheat mode** — bug icon toggle expands all caps to 255: level, IVs, souls, condenser rank, active skills (3→255), passive skills (4→255). Duplicate skills allowed, learnset bypassed. Skill pagination with mouse wheel scroll (3/page active, 4/page passive)
- **Max All Pals** — all 3 locations (pal editor, base inventory, menu→Functions) respect cheat mode caps. Double confirm dialog for menu version
- **Skill name fixes** — case-insensitive l10n lookup fixes "Thunder Rail" (was `Railbolt`). Partner skill names resolved from pal data
- **Add New Pal filter** — all filters removed: shows every entry in `_NAMEMAP`. Standard/Predator/Boss toggles all default to on
- Bumped version to 2.0.7
- **Bumped version to 2.0.7**

#2.0.6
- **Effigies now display in key items grid** — read from player `.sav` `RelicPossessNumMap` (bounty-token pattern)
- Edit/delete effigy count writes directly to `RelicPossessNumMap` (spendable at Statue of Power in-game)
- Add All Key Items prompts for effigy quantity per relic type
- Always show quantity badge on item/equip slots (count visible even at 1)
- XGP save picker (`pick_xgp_world`, `_load_xgp_save`) filters invalid saves via Level+LevelMeta+LocalData directory check
- Fixed `validate_xgp_save` `idx_path` resolution in `_load_xgp_save`
- `find_valid_saves` extracted as module-level function in `game_pass_save_fix.py`, reused in `restore_map.py`
- Theme/style consistency fixes for input dialogs
- Bumped version to `2.0.6`

#2.0.5
- `palsav` — fix `SetProperty` parsing + add missing type hint for `ValidatedStartPointIds`
- Pal editor — apply passive stat modifiers (MaxHP) to display and save writes
- Pal editor — scale current HP by passive multiplier for display consistency
- Breeding formula — align with palcalc: ceiling average for odd sums (`floor((A+B+1)/2)`)
- Update checker — use GitHub releases API instead of hardcoded `APP_VERSION`

#2.0.4
- Linux builds now produce a portable AppImage instead of a raw onefile binary
- Discord notifications upgraded to rich embeds with GitHub and Nexus Mods links
- Build caching per platform/version — same version skips rebuild entirely
- New save diagnostic script (`save_diagnostic.py`) detects orphaned players and save anomalies
- Nexus Mods upload now triggers automatically when a release is published (not during build)
- Changelog tracking system introduced (this file!)
- CI/CD: 5 workflows optimized with reusable composite actions, dist caching, hardened error handling
- Guild data format fixes for pre-2026 and 2026-07 compatibility
- Container type alignment with upstream GamePass format
- Added `encoded_raw_data` and `without_custom_type` archive helpers
- Restore Map: uses `run_with_loading` overlay for Steam and XGP clear-fog

#2.0.3
- Added `append_only` option to Build All & Release workflow (append files without editing release notes)
- Unified macOS builds on `macos_build.py`
- Cleaned up old workflow files (removed dependabot, release-build, test-build-macos)
- Merged macOS signing options into test-build workflow

#2.0.2
- 🎮 **GamePass save support**: load, edit, and save Xbox Game Pass save files with binary recompression
- Added draft test release option to Build All & Test workflow
- Release notes template with version and game version info
- Simplified release tags to just `v<version>` (always draft, publish manually)
- Preserve existing dynamics in `DynamicItemSaveData` during sync
- Fixed player file validation with translatable error messages
- Combined `fix_host_save` GUID swap + XGP save-back into single loading overlay
- Replaced hover frame with inline passive loadout preview

#2.0.1
- 🎵 **Discord notifications**: new workflow sends release announcements to Discord
- Map viewer: added base reassign to guild
- Unified macOS build script (`macos_build.py`)
- Build workflows consolidated and reorganized — cleaner CI/CD
- Fixed: NickName property when renaming a nameless player
- Fixed: base_guild_lookup key format mismatch after reassign
- Fixed: worker pal group_id and guild handles now update on base reassign

#2.0.0
- 🧬 **Breeding combos tab** with pal selector dialog and result filter search
- Refactored all right-click context menus to `ScrollableContextMenu`
- Performance optimization: replaced O(n*m) scans with pre-built maps in `character_transfer` and `fix_host_save`
- Slot injector: skip orphan containers with no matching player, restrict to guild-only players
- Numeric sorting for Level, Pals, Last Seen, Guild Level across all panels
- Map tab: fixed base child coordinate sorting
- Pal editor: show total pal count in Box/DPS headers
- Added `WaitCursor` to all heavy GUI operations
- Breeding formula documentation and rarity tiebreaker fixes
- Fixed parent lookup and `IgnoreCombi` pals children lookup

#1.0.0 — 1.1.88
These are the initial releases of Palworld Save Tools. Changelog tracking started from version 2.0.0 onward. For details on earlier releases, refer to the GitHub release history or Nexus Mods page.
