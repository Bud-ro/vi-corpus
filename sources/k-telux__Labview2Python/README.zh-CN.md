<div align="center">

# LabVIEW 转 Python 工业软件

**把 LabVIEW 测量程序迁移为可审计、可交付的 Python 工业软件。**

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

[![Validation](https://github.com/k-telux/labview-to-python/actions/workflows/validate.yml/badge.svg)](https://github.com/k-telux/labview-to-python/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-111827)](https://agentskills.io/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2563EB.svg)](LICENSE)

<img src="examples/showcase/assets/pump-probe-industrial-ui.png" width="100%" alt="完成模拟扫描的泵浦探测 Python 工业界面">

</div>

由 **telux** 创建的证据门禁式 Agent Skill，用于迁移和审核实验室/工业
LabVIEW 程序，同时保留测量逻辑、数据血缘、硬件安全、操作可用性和最终
EXE 的运行证据。

> **独立社区项目。** 本仓库不分发厂家 SDK，也不会把模拟器或截图通过自动
> 升级为真实硬件通过。实际仪器必须经过用户批准的失效安全测试。

## 为什么使用它

| 测量逻辑真实 | 工业操作界面 | 可验证交付 |
|---|---|---|
| 盘点 VI/subVI 行为，生成唯一 resolved scan plan，独立比较 workflow、文件、曲线与热图数据。 | 同时覆盖工业 UI 和 LabVIEW 风格 UI，要求真实点击、悬停、不同分辨率截图与人工二审。 | 分离模拟器、源码 UI、EXE、快捷方式和真实硬件状态，拒绝旧二进制和继承的 PASS。 |

## 真实迁移效果

| 泵浦探测采集 | 光谱与 TCSPC 扫描 |
|---|---|
| <img src="examples/showcase/assets/pump-probe-industrial-ui.png" width="100%" alt="泵浦探测 Python 工业 UI"> | <img src="examples/showcase/assets/spectroscopy-tcspc-ui.png" width="100%" alt="光谱和 TCSPC Python 工业 UI"> |

图片来自真实迁移任务的完成态验证产物，并已移除私有路径。详见
[视觉案例](examples/showcase/README.md)；监督、热图与 EXE 的脱敏输入/输出见
[案例索引](examples/README.md)。

## 安装

```bash
npx skills add k-telux/labview-to-python \
  --skill labview-to-python-industrial \
  --agent codex
```

也可以把 `skills/labview-to-python-industrial` 复制到 Agent 的 skills 目录。

## 快速使用

### 迁移程序

```text
使用 $labview-to-python-industrial 把这个 LabVIEW 测量 VI 迁移为 Python。
保留真实扫描逻辑，加入确定性模拟器，证明保存数据与显示数据一致；只有源码
UI 门禁通过后才能打包 EXE。
```

### 审核已有项目

```text
审核这个 LabVIEW 转 Python 项目。把每个可见参数追踪到 resolved scan plan，
独立比较 workflow、落盘和图表数组，并分别报告模拟器、源码 UI、EXE 与真实硬件。
```

### 诊断性能或热图

```text
在不减少扫描点、重复次数和原始保存的前提下诊断慢扫描与热图错位；分别测量
核心耗时和点击 Scan 到 Completed 的耗时，并用真实鼠标验证首/中/末数据点。
```

## 工作流程

1. 盘点 VI/subVI 状态、参数、单位、错误、文件和硬件调用。
2. 让所有可见控件生成唯一且不可变的扫描计划。
3. 真实适配器和模拟器共用同一 workflow。
4. 独立证明 workflow、保存回读、曲线和热图数据。
5. 用真实交互和新截图审核源码 UI。
6. 源码门禁批准后才从当前源码重建并运行 EXE。

## 五个独立门禁

| 门禁 | 必须证明 | 不能自动证明 |
|---|---|---|
| 逻辑与数据 | 扫描计划、数组、mask、单位、保存回读 | UI、EXE、硬件 |
| 模拟器 | 确定性 workflow 与适配器边界行为 | 厂家驱动或仪器 |
| 源码 UI | 真实交互、终态、图表、截图与视觉二审 | 打包运行时 |
| EXE | 源码血缘、哈希、快捷方式、工作流与输出 | 真实硬件 |
| 真实硬件 | 安全限制、稳定通信、清理和真实采集结果 | 未连接的可选设备 |

## 核心优势

- 可见参数必须真正改变执行计划，拒绝“只有界面变化”。
- 拒绝 target-vs-target、自调用 helper 或 setter 形成的自证。
- 模拟器、源码、EXE、硬件结论相互独立，不抬高状态。
- 部分停止保留 mask 和 `NaN`，不伪装成完整零值数据。
- 源码或 verifier 改变后，旧截图与旧 EXE 自动失效。
- 终止进程前核对 PID、命令行和项目归属。

## 项目结构

```text
skills/labview-to-python-industrial/   英文权威 Skill 与参考资料
rules/                                 派生项目规则
examples/showcase/                     脱敏视觉案例
examples/01..03/                       真实历史输入/输出案例
README.zh-CN.md                        中文入口
README.ja.md                           日文入口
scripts/validate_repo.py               无依赖发布检查
```

唯一技术规范源是
[SKILL.md](skills/labview-to-python-industrial/SKILL.md)。翻译页面出现歧义时，
以英文 Skill 为准。

## 验证与边界

```bash
python scripts/validate_repo.py
```

SDK 文件只证明清单；截图只证明与真实交互、数据绑定的可见状态；成功编译也不
等于 EXE 运行通过。真实硬件仍需要厂家手册、安全限制、操作者批准和受控测试。

维护者：[telux](https://github.com/k-telux) · [MIT License](LICENSE)
