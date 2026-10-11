# LabVIEW To Python Industrial Rule 日本語要約

ルール版 2.1.0。この文書は派生要約です。唯一の運用仕様は
`skills/labview-to-python-industrial/SKILL.md` です。

外観より先に測定ロジック、データ処理、装置呼出順序、fail-closed 動作を保持します。全 UI、シミュレーター、実機アダプターは一つの workflow を使います。表示値は実行する resolved scan plan と一致させます。quick preview は完全 parity の証拠ではありません。目標 CSV 由来の再構成は roundtrip fixture と表示します。UI は実イベント、新しい対象ウィンドウのスクリーンショット、自動画像検査、人による再確認が必要です。workflow、保存再読込、表示データを別々に比較し、source UI、simulator、EXE、real hardware を別判定にします。実機 dry run 前は `unvalidated_blocked` を維持します。
