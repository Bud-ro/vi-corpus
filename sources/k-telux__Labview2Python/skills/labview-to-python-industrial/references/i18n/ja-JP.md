# 日本語オペレーター要約

この文書は英語仕様への案内です。正規の仕様は英語の `SKILL.md` と各 reference です。

1. VI、subVI、型定義、フロントパネル、既知出力、SDK とドライバー版を固定する。
2. UI、シミュレーター、実機アダプターは同じ workflow を使用する。
3. inventory、logic/data、simulator、source UI、EXE、real hardware の順にゲートを通す。
4. quick preview は操作確認専用で、完全な分解能やデータ parity の証拠にしない。
5. 目標 CSV 由来の入力を復元した結果は roundtrip fixture であり、独立した LabVIEW algorithm parity ではない。
6. UI 検証では実際のクリック、入力、スクロール、マウス移動を使い、内部 setter を pass に使わない。
7. workflow 結果、保存ファイルの再読込、表示配列を同一 run で別々に比較する。
8. Scan クリックから終了状態までを計測し、worker 待機には `processEvents + sleep` を使う。
9. source UI、simulator、packaged EXE、real hardware、未検証 subsystem を別々に報告する。
10. 証拠がなければ `incomplete` または `blocked_unverified` とする。
