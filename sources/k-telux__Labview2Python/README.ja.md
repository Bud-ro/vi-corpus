<div align="center">

# LabVIEW to Python Industrial

**LabVIEW 計測アプリを監査可能な Python 産業ソフトウェアへ。**

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

[![Validation](https://github.com/k-telux/labview-to-python/actions/workflows/validate.yml/badge.svg)](https://github.com/k-telux/labview-to-python/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-111827)](https://agentskills.io/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2563EB.svg)](LICENSE)

<img src="examples/showcase/assets/pump-probe-industrial-ui.png" width="100%" alt="シミュレーション走査を完了したポンププローブ Python UI">

</div>

LabVIEW の研究・産業計測アプリを Python へ移行し、測定ロジック、データ
lineage、装置安全、操作性、配布 EXE を独立した証拠ゲートで検証する
**telux** の Agent Skill です。

> **独立コミュニティプロジェクト。** ベンダー SDK は配布しません。
> simulator やスクリーンショットの成功を実機成功として扱いません。

## この Skill の価値

| 測定の真実性 | オペレーター UI | 配布証拠 |
|---|---|---|
| VI/subVI の動作を棚卸しし、一つの resolved scan plan と workflow/file/plot/heatmap の独立比較を要求します。 | Industrial UI と LabVIEW-style UI、実クリック、hover、複数解像度、画像検査を扱います。 | simulator、source UI、EXE、shortcut、real hardware を別判定し、古いバイナリを拒否します。 |

## 実際の移行結果

| Pump-probe acquisition | Spectroscopy / TCSPC mapping |
|---|---|
| <img src="examples/showcase/assets/pump-probe-industrial-ui.png" width="100%" alt="ポンププローブ Python UI"> | <img src="examples/showcase/assets/spectroscopy-tcspc-ui.png" width="100%" alt="分光 TCSPC Python UI"> |

画像は実際の移行検証から匿名化した完了状態です。
[Visual case study](examples/showcase/README.md) と
[input/output examples](examples/README.md) に証拠境界を記載しています。

## インストール

```bash
npx skills add k-telux/labview-to-python \
  --skill labview-to-python-industrial \
  --agent codex
```

## クイックスタート

```text
Use $labview-to-python-industrial to migrate this LabVIEW measurement VI to
Python. Preserve the resolved scan plan, add a deterministic simulator, prove
saved/displayed data parity, and package only after source UI approval.
```

```text
Audit this migration with independent simulator, source UI, packaged EXE, and
real hardware verdicts. Keep untested hardware unvalidated.
```

## ワークフロー

1. VI/subVI の状態、単位、エラー、ファイル、装置呼出しを棚卸しする。
2. 表示コントロールから一つの不変 scan plan を解決する。
3. real adapter と deterministic simulator に同じ workflow を使う。
4. workflow、保存再読込、plot、heatmap を独立比較する。
5. 実操作と新しい target-window screenshot で source UI を検証する。
6. source gate 承認後にだけ、現在のソースから EXE を再構築して実行する。

## 独立した証拠ゲート

| Gate | 必要な証拠 | 自動的には証明しないもの |
|---|---|---|
| Logic/data | scan plan、配列、mask、単位、保存再読込 | UI、EXE、hardware |
| Simulator | 決定論的 workflow と adapter 境界 | vendor driver、instrument |
| Source UI | 実操作、完了状態、plot、screenshot | packaged runtime |
| EXE | source lineage、hash、shortcut、workflow、output | real hardware |
| Real hardware | safety limit、通信、cleanup、取得結果 | 未接続の optional device |

## 実務上の利点

- 表示値だけ変わり実行条件が固定された UI を不合格にします。
- target-vs-target 比較や setter による自己証明を認めません。
- simulator/source/EXE/hardware の状態を混在させません。
- partial stop は mask と `NaN` を保持します。
- source または verifier の変更後は古い EXE を無効にします。

## リポジトリ

```text
skills/labview-to-python-industrial/   canonical English skill
rules/                                 derived project rules
examples/showcase/                     sanitized visual case
examples/01..03/                       history-derived input/output cases
README.zh-CN.md                        Chinese entry point
README.ja.md                           Japanese entry point
scripts/validate_repo.py               dependency-free release gate
```

技術上の正規仕様は
[SKILL.md](skills/labview-to-python-industrial/SKILL.md) です。翻訳との差異が
ある場合は英語版 Skill を優先します。

## 検証と制限

```bash
python scripts/validate_repo.py
```

SDK inventory、スクリーンショット、ビルド成功だけでは実機または配布 EXE の
動作を証明できません。実機検証にはマニュアル、安全限界、承認済み dry run が
必要です。

Maintained by [telux](https://github.com/k-telux) · [MIT License](LICENSE)
