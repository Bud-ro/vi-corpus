# LabVIEW 转 Python 工业软件规则

规则版本：2.1.0。本文件是派生摘要，唯一运行规范源是
`skills/labview-to-python-industrial/SKILL.md`。

必须先保证测量逻辑、数据处理、硬件调用顺序和失效安全，再优化视觉；所有 UI、模拟器与真实硬件适配器共用同一 workflow。可见参数必须等于实际 resolved scan plan。quick preview 不得证明完整数据；目标 CSV 回灌只属于 roundtrip fixture。UI 必须通过真实交互、新截图、自动图像检查和人工二审。必须分别比较 workflow、落盘回读和图表数据，并分别报告源码 UI、模拟器、EXE、真实硬件和未验证子系统。新源码或 verifier 变更后不得复用旧截图或旧 EXE。终止进程前必须核对命令行和项目路径。真实硬件在安全 dry run 前保持 `unvalidated_blocked`。
