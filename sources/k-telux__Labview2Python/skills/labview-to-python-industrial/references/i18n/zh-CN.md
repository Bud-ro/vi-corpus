# 中文操作摘要

本文件是英文规范的简体中文导航，英文 `SKILL.md` 与各 reference 为唯一规范源。

1. 先冻结 VI、subVI、控件、驱动版本、front panel 和已知输出，再建立功能对应表。
2. UI、模拟器和真实硬件必须共用同一 workflow；UI 不能复制扫描状态机。
3. 依次通过功能清单、逻辑/数据、模拟器、源码 UI、EXE、真实硬件门禁。
4. quick preview 只能证明交互，不能证明完整分辨率和完整数据。
5. 目标 CSV 回灌后再还原只能标记为 roundtrip fixture，不能当独立 LabVIEW 算法等价证据。
6. UI 验收必须使用真实点击、输入、下拉框、滚动和鼠标悬停；内部 setter 不得计入通过。
7. 必须比较同一次运行的 workflow 内存结果、落盘文件回读和图表实际数据。
8. 性能应从真实点击 Scan 到最终状态计时；等待 worker 时使用 `processEvents + sleep`，避免 `QTest.qWait` 造成假回归。
9. 源码、EXE、模拟器、真实硬件和未验证子系统必须分别报告。
10. 没有新截图、哈希/时间谱系或真实硬件证据时，必须报告 incomplete/blocked，不得补成 pass。
