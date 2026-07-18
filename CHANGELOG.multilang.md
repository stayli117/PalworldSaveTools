# 🗒️ Changelog

<details open>
<summary>🇺🇸 English</summary>

- **Portuguese (Brazil) translations** — added full Brazilian Portuguese language support. All 2171 UI strings translated. Selectable from the menu under Languages.
- **READMEs updated** — added Cheat Mode, Export/Import `.pstpal`, Base Change Coordinates, Base Nudge, and other missing features to all 9 README translations.
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
- **Map viewer base actions enhanced** — every base operation (delete, export, clone, radius, reassign, move, nudge) now zooms to the base with a glow effect before executing, and plays a pulsing sparkle animation on completion. Clone Base is now also available from the tree list right-click menu.
- Bumped version to 2.1.3

</details>

<details>
<summary>🇨🇳 中文</summary>

- **葡萄牙语（巴西）翻译** — 添加了完整的巴西葡萄牙语支持。所有 2171 个 UI 字符串均已翻译。可从语言下的菜单中选择。
- **更新自述文件** — 在所有 9 个自述文件翻译中添加了作弊模式、导出/导入 `.pstpal`、基础更改坐标、基础微调和其他缺失功能。
- **加载屏幕大修** — 加载屏幕不再挂起或卡住。完全重写了动画系统 - 它现在在自己的后台进程中运行，因此即使保存操作需要很长时间，加载窗口也能保持流畅且响应灵敏。
- **加载屏幕添加到更多工具** - 转换保存文件、恢复地图（Steam 和 GamePass）以及玩家库存最大所有统计数据按钮现在在繁重工作期间显示加载屏幕，而不是冻结。
- **嵌套加载冲突已修复** - 在 Pal 编辑器打开时使用 Max All Pals 等菜单功能不再产生多个重叠的加载屏幕，从而破坏 UI。
- **惰性选项卡崩溃修复** - 当您尚未访问某些选项卡时，菜单操作不再崩溃。该应用程序会跳过尚未打开的选项卡上的缓存更新，并且这些选项卡会在您首次访问时加载新数据。
- **Pal 编辑器切换工具提示** — 信息面板中的所有切换按钮（性别、掠食者、老板、幸运等）现在在悬停时显示有用的工具提示，并翻译成所有支持的语言。
- **备份现在包括更多保存文件** - 自动备份还保存 WorldOption.sav 和 LocalData.sav，而不仅仅是 Level.sav 和玩家。保存中的备份文件夹将被自动跳过。
- **游戏版本工具提示** — 将鼠标悬停在标题中的游戏版本标签上会显示所有语言的当前 Palworld 版本。
- **palsav json_tools 中的流支持** — 现在可以直接从内存流读取和写入保存文件，而不仅仅是文件路径。作者：姆桑森。
- **从备份加载** — 新的文件菜单选项列出了所有自动备份以及时间戳、世界名称和玩家数量，以便您可以轻松恢复任何以前的保存状态。
- **作弊模式压缩星星上限** - 即使在作弊模式下，压缩等级（星星）现在也限制为 5，因为较高的值会导致游戏中出现故障。作弊模式仍然可以解锁其他上限，例如 IV、灵魂和等级。
- **地图查看器基本操作增强** - 每个基本操作（删除、导出、克隆、半径、重新分配、移动、微移）现在在执行前都会缩放到具有发光效果的基础，并在完成时播放脉冲闪烁动画。现在还可以从树列表右键菜单中使用克隆基地。
- 版本升级至 2.1.3

</details>

<details>
<summary>🇩🇪 Deutsch</summary>

- **Portugiesisch (Brasilien)-Übersetzungen** – volle Sprachunterstützung für brasilianisches Portugiesisch hinzugefügt. Alle 2171 UI-Strings übersetzt. Auswählbar im Menü unter Sprachen.
- **READMEs aktualisiert** – Cheat-Modus, Export/Import „.pstpal“, Base Change Coordinates, Base Nudge und andere fehlende Funktionen zu allen 9 README-Übersetzungen hinzugefügt.
- **Überarbeitung des Ladebildschirms** – der Ladebildschirm kann nicht mehr hängen bleiben oder hängen bleiben. Das Animationssystem wurde komplett neu geschrieben – es läuft jetzt in einem eigenen Hintergrundprozess, sodass das Ladefenster auch dann reibungslos und reaktionsschnell bleibt, wenn ein Speichervorgang lange dauert.
- **Ladebildschirme zu weiteren Tools hinzugefügt** – Speicherdateien konvertieren, Karte wiederherstellen (sowohl Steam als auch GamePass) und die Schaltfläche „Spielerinventar max. Alle Statistiken“ zeigen jetzt bei schwerer Arbeit einen Ladebildschirm an, anstatt einzufrieren.
- **Verschachtelter Ladekonflikt behoben** – Die Verwendung von Menüfunktionen wie „Alle Freunde maximieren“, während der Freunde-Editor geöffnet ist, führt nicht mehr dazu, dass mehrere überlappende Ladebildschirme angezeigt werden, die die Benutzeroberfläche beschädigen.
- **Lazy Tab Crash Fix** – Menüvorgänge stürzen nicht mehr ab, wenn Sie bestimmte Tabs noch nicht besucht haben. Die App überspringt Cache-Updates auf Tabs, die nicht geöffnet wurden, und diese Tabs laden neue Daten, wenn Sie sie zum ersten Mal besuchen.
- **Kumpel-Editor-Umschalt-Tooltips** – alle Umschaltschaltflächen im Infofeld (Geschlecht, Predator, Boss, Lucky und mehr) zeigen jetzt beim Hover hilfreiche Tooltips an, übersetzt in alle unterstützten Sprachen.
- **Backup enthält jetzt mehr Sicherungsdateien** – automatische Backups sichern auch WorldOption.sav und LocalData.sav, nicht nur Level.sav und Player. Sicherungsordner in Ihrem Speicher werden automatisch übersprungen.
- **Tooltip zur Spielversion** – Wenn Sie mit der Maus über die Bezeichnung der Spielversion in der Kopfzeile fahren, wird die aktuelle Palworld-Version in allen Sprachen angezeigt.
- **Stream-Unterstützung in palsav json_tools** – Sicherungsdateien können jetzt direkt aus Speicherstreams gelesen und geschrieben werden, nicht nur aus Dateipfaden. Von msansen.
- **Aus Backup laden** – neue Menüoption „Datei“, die alle Ihre automatischen Backups mit Zeitstempel, Weltnamen und Spieleranzahl auflistet, sodass Sie jeden vorherigen Speicherstatus problemlos wiederherstellen können.
- **Kondensierte Sterne im Cheat-Modus begrenzt** – der Kondensator-Rang (Sterne) ist jetzt auch im Cheat-Modus auf 5 begrenzt, da höhere Werte zu Störungen im Spiel führen. Der Cheat-Modus schaltet weiterhin andere Obergrenzen wie IVs, Seelen und Level frei.
- **Basisaktionen des Kartenviewers verbessert** – jeder Basisvorgang (Löschen, Exportieren, Klonen, Radius, Neu zuweisen, verschieben, verschieben) zoomt jetzt vor der Ausführung mit einem Leuchteffekt auf die Basis und spielt nach Abschluss eine pulsierende Glitzeranimation ab. Clone Base ist jetzt auch über das Kontextmenü der Baumliste verfügbar.
- Version auf 2.1.3 erweitert

</details>

<details>
<summary>🇪🇸 Español</summary>

- **Traducciones al portugués (Brasil)**: se agregó soporte completo para el idioma portugués de Brasil. Todas las 2171 cadenas de UI traducidas. Seleccionable desde el menú en Idiomas.
- **README actualizado**: se agregó el modo Cheat, Exportar/Importar `.pstpal`, Coordenadas de cambio de base, Empujar base y otras características faltantes a las 9 traducciones README.
- **Revisión de la pantalla de carga**: la pantalla de carga ya no puede colgarse ni atascarse. Se reescribió completamente el sistema de animación: ahora se ejecuta en su propio proceso en segundo plano, por lo que incluso si una operación de guardado lleva mucho tiempo, la ventana de carga se mantiene fluida y receptiva.
- **Pantallas de carga agregadas a más herramientas**: Convertir archivos guardados, restaurar mapa (tanto Steam como GamePass) y el botón Máximo de todas las estadísticas del inventario del jugador ahora muestran una pantalla de carga durante el trabajo pesado en lugar de congelarse.
- **Se solucionó el conflicto de carga anidada**: el uso de funciones de menú como Max All Pals mientras el Editor Pal está abierto ya no genera múltiples pantallas de carga superpuestas que interrumpen la interfaz de usuario.
- **Solución de bloqueo de pestañas diferidas**: las operaciones del menú ya no fallan cuando aún no has visitado ciertas pestañas. La aplicación omite las actualizaciones de caché en las pestañas que no se han abierto, y esas pestañas cargan datos nuevos cuando las visitas por primera vez.
- **Información sobre herramientas de alternancia del editor Pal**: todos los botones de alternancia en el panel de información (Género, Depredador, Jefe, Afortunado y más) ahora muestran información sobre herramientas útiles al pasar el cursor, traducida a todos los idiomas admitidos.
- **La copia de seguridad ahora incluye más archivos guardados**: las copias de seguridad automáticas también guardan WorldOption.sav y LocalData.sav, no solo Level.sav y los reproductores. Las carpetas de respaldo dentro de tu archivo guardado se omiten automáticamente.
- **Información sobre herramientas de la versión del juego**: al pasar el cursor sobre la etiqueta de la versión del juego en el encabezado, se muestra la versión actual de Palworld, en todos los idiomas.
- **Soporte de transmisión en palsav json_tools**: los archivos guardados ahora se pueden leer y escribir directamente desde las secuencias de memoria, no solo desde las rutas de los archivos. Por msansen.
- **Cargar desde copia de seguridad**: nueva opción del menú Archivo que enumera todas tus copias de seguridad automáticas con marca de tiempo, nombre mundial y recuento de jugadores, para que puedas restaurar fácilmente cualquier estado de guardado anterior.
- **Estrellas condensadas del modo trampa limitadas**: el rango del condensador (estrellas) ahora está limitado a 5 incluso en el modo trampa, ya que los valores más altos causan fallas en el juego. El modo trampa aún desbloquea otros límites como IV, almas y niveles.
- **Acciones base del visor de mapas mejoradas**: cada operación base (eliminar, exportar, clonar, radio, reasignar, mover, empujar) ahora se acerca a la base con un efecto de brillo antes de ejecutarse y reproduce una animación de brillo pulsante al finalizar. Clonar base ahora también está disponible en el menú contextual de la lista de árbol.
- Versión mejorada a 2.1.3

</details>

<details>
<summary>🇫🇷 Français</summary>

- **Traductions en portugais (Brésil)** — ajout d'une prise en charge complète de la langue portugaise brésilienne. Toutes les 2 171 chaînes d’interface utilisateur traduites. Sélectionnable dans le menu sous Langues.
- **README mis à jour** — ajout du mode de triche, de l'exportation/importation `.pstpal`, des coordonnées de changement de base, du déplacement de base et d'autres fonctionnalités manquantes aux 9 traductions README.
- **Révision de l'écran de chargement** — l'écran de chargement ne peut plus se bloquer ou rester bloqué. Le système d'animation a été entièrement réécrit : il s'exécute désormais dans son propre processus en arrière-plan, de sorte que même si une opération de sauvegarde prend du temps, la fenêtre de chargement reste fluide et réactive.
- **Écrans de chargement ajoutés à davantage d'outils** — Convertir les fichiers de sauvegarde, restaurer la carte (à la fois Steam et GamePass) et le bouton Player Inventory Max All Stats affichent désormais un écran de chargement pendant un travail intense au lieu de se bloquer.
- **Conflit de chargement imbriqué résolu** — l'utilisation de fonctions de menu telles que Max All Pals lorsque l'éditeur Pal est ouvert ne génère plus plusieurs écrans de chargement qui se chevauchent et interrompent l'interface utilisateur.
- **Correction d'un crash d'onglet paresseux** — les opérations de menu ne plantent plus lorsque vous n'avez pas encore visité certains onglets. L'application ignore les mises à jour du cache sur les onglets qui n'ont pas été ouverts, et ces onglets chargent de nouvelles données lorsque vous les visitez pour la première fois.
- **Les info-bulles de l'éditeur Pal** — tous les boutons à bascule du panneau d'informations (Sexe, Prédateur, Boss, Lucky, et plus) affichent désormais des info-bulles utiles au survol, traduites dans toutes les langues prises en charge.
- **La sauvegarde inclut désormais davantage de fichiers de sauvegarde** — les sauvegardes automatiques enregistrent également WorldOption.sav et LocalData.sav, et pas seulement Level.sav et les lecteurs. Les dossiers de sauvegarde dans votre sauvegarde sont automatiquement ignorés.
- **Info-bulle de la version du jeu** — le survol de l'étiquette de la version du jeu dans l'en-tête affiche la version actuelle de Palworld, dans toutes les langues.
- **Prise en charge des flux dans palsav json_tools** — les fichiers de sauvegarde peuvent désormais être lus et écrits directement à partir des flux de mémoire, et pas seulement des chemins de fichiers. Par Msansen.
- **Charger à partir de la sauvegarde** — nouvelle option de menu Fichier qui répertorie toutes vos sauvegardes automatiques avec l'horodatage, le nom du monde et le nombre de joueurs, afin que vous puissiez facilement restaurer n'importe quel état de sauvegarde précédent.
- **Étoiles condensées du mode Cheat plafonnées** — le rang du condenseur (étoiles) est désormais limité à 5, même en mode Cheat, car des valeurs plus élevées provoquent des problèmes dans le jeu. Le mode Cheat déverrouille toujours d’autres plafonds comme les IV, les âmes et le niveau.
- **Actions de base de la visionneuse de carte améliorées** — chaque opération de base (supprimer, exporter, cloner, rayon, réaffecter, déplacer, déplacer) effectue désormais un zoom sur la base avec un effet de lueur avant de s'exécuter et joue une animation scintillante pulsée à la fin. Clone Base est désormais également disponible dans le menu contextuel de la liste arborescente.
- Version améliorée à 2.1.3

</details>

<details>
<summary>🇷🇺 Русский</summary>

- **Португальский (Бразилия) перевод** — добавлена ​​полная поддержка бразильского португальского языка. Переведена вся 2171 строка пользовательского интерфейса. Можно выбрать в меню «Языки».
- **Обновлены файлы README** — во все 9 переводов README добавлены чит-режим, экспорт/импорт `.pstpal`, координаты изменения базы, сдвиг базы и другие недостающие функции.
- **Переработка экрана загрузки** — экран загрузки больше не зависает и не застревает. Полностью переписана система анимации — теперь она работает в собственном фоновом процессе, поэтому даже если операция сохранения занимает много времени, окно загрузки остается плавным и отзывчивым.
- **Добавлены экраны загрузки к большему количеству инструментов** — «Преобразование файлов сохранения», «Восстановить карту» (как Steam, так и GamePass), а также кнопка «Максимальная вся статистика» в инвентаре игрока теперь отображают экран загрузки во время интенсивной работы, а не зависают.
- **Исправлен вложенный конфликт загрузки** — использование таких функций меню, как Max All Pals, когда открыт редактор Pal, больше не вызывает несколько перекрывающихся экранов загрузки, которые нарушают пользовательский интерфейс.
- **Исправление сбоя при ленивой вкладке** — операции меню больше не приводят к сбою, если вы еще не посетили определенные вкладки. Приложение пропускает обновления кэша на вкладках, которые не открывались, и эти вкладки загружают свежие данные при первом посещении.
- **Подсказки для переключения редактора Pal** — все кнопки переключения на информационной панели («Пол», «Хищник», «Босс», «Счастливчик» и другие) теперь при наведении показывают полезные всплывающие подсказки, переведенные на все поддерживаемые языки.
- **Резервное копирование теперь включает больше файлов сохранения** — автоматические резервные копии также сохраняют WorldOption.sav и LocalData.sav, а не только Level.sav и игроков. Папки резервных копий внутри вашего сохранения автоматически пропускаются.
- **Подсказка о версии игры** — при наведении курсора на метку версии игры в заголовке отображается текущая версия Palworld на всех языках.
- **Поддержка потоков в palsav json_tools** — файлы сохранения теперь можно читать и записывать непосредственно из потоков памяти, а не только из путей к файлам. Автор: Мсансен.
- **Загрузить из резервной копии** — новый пункт меню «Файл», в котором перечислены все автоматически созданные резервные копии с отметкой времени, мировым именем и количеством игроков, поэтому вы можете легко восстановить любое предыдущее состояние сохранения.
- **Ограничено количество конденсированных звезд в режиме читов** — ранг конденсатора (звезд) теперь ограничен 5 даже в режиме читов, поскольку более высокие значения вызывают сбои в игре. Чит-режим по-прежнему открывает другие ограничения, такие как IV, души и уровень.
- **Улучшены базовые действия средства просмотра карт** — каждая базовая операция (удаление, экспорт, клонирование, радиус, переназначение, перемещение, смещение) теперь перед выполнением приближается к базе с эффектом свечения, а по завершении воспроизводится пульсирующая блестящая анимация. База клонов теперь также доступна из контекстного меню древовидного списка.
- Обновлена ​​версия до 2.1.3.

</details>

<details>
<summary>🇯🇵 日本語</summary>

- **ポルトガル語 (ブラジル) 翻訳** — ブラジルポルトガル語の完全なサポートを追加しました。 2171 個の UI 文字列をすべて翻訳しました。 「言語」の下のメニューから選択できます。
- **README を更新** — チート モード、`.pstpal` のエクスポート/インポート、ベース変更座標、ベース ナッジ、およびその他の不足している機能を 9 つの README 翻訳すべてに追加しました。
- **ロード画面のオーバーホール** — ロード画面がハングしたり固まったりすることがなくなりました。アニメーション システムを完全に書き直しました。アニメーション システムは独自のバックグラウンド プロセスで実行されるため、保存操作に時間がかかっても、読み込みウィンドウはスムーズで応答性が高くなります。
- **より多くのツールにロード画面を追加** — セーブ ファイルの変換、マップの復元 (Steam と GamePass の両方)、およびプレーヤー インベントリ Max All Stats ボタンは、重い作業中にフリーズするのではなくロード画面を表示するようになりました。
- **ネストされた読み込みの競合が修正されました** — Pal エディターが開いているときに Max All Pals などのメニュー機能を使用すると、UI を壊す複数の重複する読み込み画面が生成されなくなりました。
- **遅延タブ クラッシュの修正** — 特定のタブにまだアクセスしていないときにメニュー操作がクラッシュすることはなくなりました。アプリは、開かれていないタブのキャッシュ更新をスキップし、それらのタブには、最初にアクセスしたときに新しいデータが読み込まれます。
- **Pal エディターのトグル ツールチップ** — 情報パネルのすべてのトグル ボタン (性別、プレデター、ボス、ラッキーなど) にホバーすると役立つツールチップが表示され、サポートされているすべての言語に翻訳されます。
- **バックアップにはさらに多くの保存ファイルが含まれるようになりました** — 自動バックアップでは、Level.sav とプレーヤーだけでなく、WorldOption.sav と LocalData.sav も保存されます。セーブデータ内のバックアップ フォルダーは自動的にスキップされます。
- **ゲーム バージョン ツールチップ** — ヘッダーのゲーム バージョン ラベルの上にマウスを置くと、現在の Palworld バージョンがすべての言語で表示されます。
- **palsav json_tools でのストリーム サポート** — 保存ファイルは、ファイル パスだけでなくメモリ ストリームから直接読み書きできるようになりました。 by ムサンセン。
- **バックアップからロード** — すべての自動バックアップをタイムスタンプ、ワールド名、プレイヤー数とともにリストする新しい [ファイル] メニュー オプションにより、以前の保存状態を簡単に復元できます。
- **チート モードの凝縮スターに上限あり** — 値が高くなるとゲーム内で不具合が発生するため、チート モードであっても凝縮スターのランク (スター) は 5 に制限されます。チートモードでは、IV、ソウル、レベルなどの他のキャップのロックが解除されます。
- **マップ ビューアのベース アクションの強化** — すべてのベース操作 (削除、エクスポート、クローン、半径、再割り当て、移動、ナッジ) は、実行前にグロー効果でベースにズームし、完了時にパルスの輝きアニメーションを再生するようになりました。クローン ベースは、ツリー リストの右クリック メニューからも使用できるようになりました。
- バージョンを 2.1.3 に変更しました

</details>

<details>
<summary>🇰🇷 한국어</summary>

- **포르투갈어(브라질) 번역** — 전체 브라질 포르투갈어 지원이 추가되었습니다. 2171개의 UI 문자열이 모두 번역되었습니다. 언어 아래 메뉴에서 선택할 수 있습니다.
- **README 업데이트** — 치트 모드, `.pstpal` 내보내기/가져오기, 기본 변경 좌표, 기본 너지 및 기타 누락된 기능을 9개의 README 번역 모두에 추가했습니다.
- **로딩 화면 점검** — 로딩 화면이 더 이상 멈추거나 멈추는 일이 없습니다. 애니메이션 시스템을 완전히 다시 작성했습니다. 이제 자체 백그라운드 프로세스에서 실행되므로 저장 작업이 오래 걸리더라도 로딩 창이 원활하고 반응적으로 유지됩니다.
- **더 많은 도구에 로딩 화면 추가** — 이제 저장 파일 변환, 지도 복원(Steam 및 GamePass 모두), 플레이어 인벤토리 최대 모든 통계 버튼이 무거운 작업 중에 멈추는 대신 로딩 화면을 표시합니다.
- **중첩된 로딩 충돌 수정** — Pal 편집기가 열려 있는 동안 Max All Pals와 같은 메뉴 기능을 사용하면 더 이상 UI를 손상시키는 여러 개의 겹치는 로딩 화면이 생성되지 않습니다.
- **지연 탭 충돌 수정** — 아직 특정 탭을 방문하지 않았을 때 메뉴 작업이 더 이상 충돌하지 않습니다. 앱은 열리지 않은 탭의 캐시 업데이트를 건너뛰고, 해당 탭을 처음 방문하면 해당 탭에 새로운 데이터가 로드됩니다.
- **Pal 편집기 토글 툴팁** — 정보 패널의 모든 토글 버튼(성별, 프레데터, 보스, 럭키 등)은 이제 마우스를 올리면 지원되는 모든 언어로 번역된 유용한 툴팁을 표시합니다.
- **이제 백업에는 더 많은 저장 파일이 포함됩니다** — 자동 백업은 Level.sav 및 플레이어뿐만 아니라 WorldOption.sav 및 LocalData.sav도 저장합니다. 저장 내의 백업 폴더는 자동으로 건너뜁니다.
- **게임 버전 툴팁** — 헤더의 게임 버전 라벨 위로 마우스를 가져가면 현재 Palworld 버전이 모든 언어로 표시됩니다.
- **palsav json_tools의 스트림 지원** — 이제 파일 경로뿐만 아니라 메모리 스트림에서 직접 저장 파일을 읽고 쓸 수 있습니다. 작성자: msansen
- **백업에서 로드** — 타임스탬프, 세계 이름, 플레이어 수와 함께 모든 자동 백업을 나열하는 새로운 파일 메뉴 옵션을 제공하므로 이전 저장 상태를 쉽게 복원할 수 있습니다.
- **치트 모드 응축 별 제한** — 값이 높을수록 게임 내 결함이 발생하므로 치트 모드에서도 응축기 등급(별)이 이제 5개로 제한됩니다. 치트 모드에서는 여전히 IV, 소울, 레벨과 같은 다른 한도의 잠금이 해제됩니다.
- **지도 뷰어 기본 작업 향상** — 이제 모든 기본 작업(삭제, 내보내기, 복제, 반경, 재할당, 이동, 살짝 이동)이 실행되기 전에 발광 효과를 사용하여 베이스를 확대하고 완료 시 깜박이는 반짝이는 애니메이션을 재생합니다. 이제 트리 목록 오른쪽 클릭 메뉴에서도 복제 베이스를 사용할 수 있습니다.
- 버전이 2.1.3으로 변경되었습니다.

</details>

<details>
<summary>🇧🇷 Português</summary>

- **Traduções para o português (Brasil)** — adicionado suporte completo ao idioma português brasileiro. Todas as strings da UI 2171 foram traduzidas. Selecionável no menu em Idiomas.
- **READMEs atualizados** — adicionado modo Cheat, exportação/importação `.pstpal`, coordenadas de mudança de base, Nudge de base e outros recursos ausentes em todas as 9 traduções do README.
- **Revisão da tela de carregamento** — a tela de carregamento não pode mais travar ou travar. Reescreveu completamente o sistema de animação – ele agora é executado em seu próprio processo em segundo plano, portanto, mesmo que uma operação de salvamento demore muito, a janela de carregamento permanece suave e responsiva.
- **Telas de carregamento adicionadas a mais ferramentas** — Converter arquivos salvos, restaurar mapa (Steam e GamePass) e o botão Player Inventory Max All Stats agora mostram uma tela de carregamento durante o trabalho pesado em vez de congelar.
- **Conflito de carregamento aninhado corrigido** — usar funções de menu como Max All Pals enquanto o Pal Editor está aberto não gera mais várias telas de carregamento sobrepostas que quebram a interface do usuário.
- **Correção de travamento da guia preguiçosa** — as operações do menu não travam mais quando você ainda não visitou determinadas guias. O aplicativo ignora as atualizações de cache nas guias que não foram abertas e essas guias carregam dados novos quando você as visita pela primeira vez.
- **Dicas de alternância do editor Pal** — todos os botões de alternância no painel de informações (Gênero, Predador, Chefe, Sortudo e mais) agora mostram dicas de ferramentas úteis ao passar o mouse, traduzidas para todos os idiomas suportados.
- **O backup agora inclui mais arquivos salvos** — os backups automáticos também salvam WorldOption.sav e LocalData.sav, não apenas Level.sav e jogadores. As pastas de backup dentro do seu save são ignoradas automaticamente.
- **Dica da versão do jogo** — passar o mouse sobre o rótulo da versão do jogo no cabeçalho mostra a versão atual do Palworld, em todos os idiomas.
- **Suporte a stream em palsav json_tools** — arquivos salvos agora podem ser lidos e gravados diretamente de streams de memória, não apenas de caminhos de arquivo. Por msansen.
- **Carregar do backup** — nova opção de menu Arquivo que lista todos os seus backups automáticos com carimbo de data/hora, nome do mundo e contagem de jogadores, para que você possa restaurar facilmente qualquer estado de salvamento anterior.
- **Estrelas condensadas do modo cheat limitadas** — a classificação do condensador (estrelas) agora é limitada a 5, mesmo no modo cheat, já que valores mais altos causam falhas no jogo. O modo Cheat ainda desbloqueia outros limites como IVs, almas e nível.
- **Ações básicas do visualizador de mapa aprimoradas** — cada operação básica (excluir, exportar, clonar, raio, reatribuir, mover, deslocar) agora amplia a base com um efeito de brilho antes de ser executada e reproduz uma animação de brilho pulsante ao ser concluída. Clone Base agora também está disponível no menu do botão direito da lista em árvore.
- Versão atualizada para 2.1.3

</details>
