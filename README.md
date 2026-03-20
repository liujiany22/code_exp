# code_exp

认知负荷实验程序框架。

## 项目结构

- `launcher.py`：整套实验的统一入口
- `config/`：全局配置、事件码、设备参数
- `eeg/`：EEG / EyeLink trigger 接口与测试脚本
- `common/`：共享的数据、UI、外部任务包装工具
- `tasks/protocol/`：练习段 + 正式段的完整流程
- `tasks/`：可单独调试或重跑的任务模块
- `cognitiveabilitytest/`：数字记忆与柯西方块的参考 PsychoPy 导出工程
- `stimuli/`：视频、图片、条件表、问卷接口文件
- `data/`：行为数据与日志输出目录

## 后续重点

1. 将 `dummy` trigger 替换为真实的 NeusenW32 / TriggerBox 通信实现。
2. 决定 `wm_pretest` 是否需要更细粒度的 trial 级 EEG marker。
3. 将视频学习任务中的问卷占位接口替换为真实问卷。
4. 在最终的 Windows 采集机上完成整套 PsychoPy 联调。

## 当前状态

- trigger 层已统一收敛在 `eeg/trigger.py`。
- 默认使用 `dummy` 模式，适合在硬件未接入前做联调。
- 同一个事件现在可以同时广播到 EEG 和 EyeLink。
- EyeLink 默认是 message-only 模式，校准和录制可继续由眼动主试机独立控制。
- EyeLink 支持两种后端：`direct` 和 `relay`。当主实验必须使用 Python 3.10、而 PyLink 只能在独立 Python 3.9 环境运行时，应使用 `relay`。
- `launcher` 默认会运行完整的 `protocol`，包含练习段和正式段。
- 静息态支持固定或随机的睁闭眼顺序，也支持阶段切换提示音。
- 工作记忆前测支持分别运行 `digit span`、`corsi blocks`，或顺序运行两者。
- 心算任务已支持 block 结构，以及“题干 / 中央+过渡 / 蓝色数字判等 / 中央+过渡”的时序控制。
- 视频学习任务支持 1 / 2 / 6 试次结构；当前正式 protocol 只启用 `fourier_protocol` 一组。
- `fourier_protocol` 的正式前测和后测均已接入真实判断题，答题键为 `F=对`、`J=错`。
- 视频学习前测/后测现支持“先口头复述，再完成 10 道判断题”；判断题默认时序为 `4s + 4s + 1s`。
- 视频会在播放前临时切分为 3 分钟片段，并在段间及播放结束后插入 1-5 评分条。

## 运行完整实验

```bash
python launcher.py --participant sub01 --session 001
```

程序启动后会先进入被试信息录入步骤。默认会弹出录入框，当前要求填写：

- 姓名
- 被试号
- 年龄
- Session

这些信息会随本次 run 一起保存到输出目录中的 `participant_info.json` 和
`participant_info.csv`。

如果命令行里已经提供了 `--participant`、`--session`、`--name`、`--age`，
它们会作为录入框默认值显示。

默认情况下，实验界面会以全屏方式运行。只有在调试时，才建议使用
`--ma-windowed`、`--lc-windowed` 或修改 `config/local_settings.py` 将窗口切回非全屏。

默认情况下，`launcher` 会自动运行完整 protocol，主要包含：

1. 练习引导与练习演示
2. 正式静息态
3. 正式数字记忆
4. 正式柯西方块
5. 正式心算
6. 正式视频学习

只有在调试或单独重跑某个模块时，才建议使用 `--task`。

## 实验流程

默认 `protocol` 目前按以下流程组织。
目前仅“视频学习练习演示”仍是说明页；数字记忆和柯西方块不再单独弹介绍页。

### 练习段

1. 练习环节：提示开始进入练习
2. 静息练习：说明睁眼/闭眼练习要求
3. 静息练习：共 6 秒，先睁眼后闭眼，各 3 秒，在 3 秒切换点播放提示音
4. 数字记忆演示：一轮短演示
5. 柯西方块演示：一轮短演示
6. 心算练习：说明黑色题干、中央“+”过渡、蓝色数字与鼠标左/右键判等规则
7. 心算演示：一轮短演示
8. 视频学习练习：说明前测、视频和后测的组块结构
9. 视频学习练习：当前仍为说明页，真实演示接口已预留
10. 短暂休息：提示练习结束，准备进入正式实验

### 正式段

11. 正式实验：提示开始进入正式实验
12. 静息态：说明正式静息态要求与随机睁闭眼顺序
13. 正式静息态：共 360 秒，睁眼 180 秒 + 闭眼 180 秒，顺序随机，切换阶段时播放提示音
14. 数字记忆任务：直接进入任务，不再单独弹介绍页
15. 柯西方块任务：直接进入任务，不再单独弹介绍页
16. 心算任务：任务说明 + 3 个 block + 休息
    每个 block：25 ×【黑色加法题呈现 6 秒 -> 中央“+”过渡 1 秒 -> 蓝色数字判等 4 秒（左键=相等，右键=不等）-> 中央“+”过渡 1 秒】+ 30 秒休息
17. 视频学习任务：说明当前傅立叶组“前测 + 视频 + 后测”的结构
18. 视频学习任务：当前运行 1 组实验，结构为前测 + 视频 + 后测
19. 实验结束

### 当前实现说明

- protocol 调度器位于 `tasks/protocol/task.py`。
- 静息、心算、视频学习仍保留单独介绍页。
- 数字记忆和柯西方块已改为直接进入任务，不再单独弹介绍页。
- 视频学习练习演示当前仍是说明页，尚未替换为真实视频演示。
- 练习阶段的 `digit span` 和 `corsi blocks` 目前使用包装层控制的短演示，而不是完全定制的单 trial 演示实现。

## 运行缩短版测试流程

```bash
python launcher.py --participant test --session 001 --test-mode --auto-advance
```

`--test-mode` 会保留 protocol 的整体结构，但将主要任务压缩为便于联调的短版：

1. 直接跳过练习段，只运行缩水后的正式段
2. 静息态在测试模式下为 3 秒 + 3 秒
3. 数字记忆和柯西方块使用 pilot mode，并加更短的包装层时间上限
4. 心算缩短为单个短 block
5. 视频学习保持正式阶段配置，不再压缩
6. 本次运行的所有输出都会写入临时目录，并在结束后自动删除，不会保留正式数据

如果只想单独查看某一个正式阶段，可在测试模式下增加 `--test-stage`：

```bash
python launcher.py --test-mode --test-stage resting_state --auto-advance
python launcher.py --test-mode --test-stage digit_span --auto-advance
python launcher.py --test-mode --test-stage corsi_blocks --auto-advance
python launcher.py --test-mode --test-stage mental_arithmetic --auto-advance
python launcher.py --test-mode --test-stage learning_cycle --auto-advance
```

可选阶段名为：

- `resting_state`
- `digit_span`
- `corsi_blocks`
- `mental_arithmetic`
- `learning_cycle`

如果在无图形环境下调试，或你希望直接使用命令行参数而不弹出录入框，可加：

```bash
python launcher.py --participant test --session 001 --name test --age 20 --skip-subject-dialog
```

## 单独运行静息态

```bash
python launcher.py --task resting_state --auto-advance --eyes-open 3 --eyes-closed 3
```

静息态默认时长为睁眼 180 秒、闭眼 180 秒。

如需接 Neuracle TriggerBox，请在 `config/local_settings.py` 中配置：

```python
TRIGGER_MODE = "neuracle_serial"
TRIGGER_PORT = "COM3"
```

此模式会按 `Neuracle/` 目录中的官方串口协议发送 trigger，而不是直接向串口裸写一个字节。
如果需要并行写入 EyeLink message，则另外设置 `EYELINK_ENABLED=1`。

如果主实验运行在 Python 3.10 下，请将 `EYELINK_BACKEND` 设为 `relay`，并在独立的 Python 3.9 进程中运行 EyeLink relay server：

```bash
py -3.9 eeg/eyelink_relay_server.py
```

主实验随后会默认连接到 `127.0.0.1:18765`。

如果使用 `EYELINK_BACKEND="direct"`，则当前 Python 必须能够直接 `import pylink`。只有在 PyLink 不在当前 Python 环境里时，才需要设置 `EYELINK_PYLINK_PATH`。

只有在你希望 EyeLink 一侧同时发送 `screen_pixel_coords`、`DISPLAY_COORDS` 和 `calibration_type` 时，才需要设置 `EYELINK_INITIALIZE_CONTEXT=1`。

如果不想每次都在终端里设置这些参数，直接编辑 `config/local_settings.py`
即可。如果环境变量和配置文件同时存在，环境变量优先。

## 单独运行工作记忆前测

```bash
python launcher.py --task wm_pretest --participant sub01 --session 001
```

PsychoPy 相关环境说明见 `tasks/wm_pretest/README.md`。

## 单独运行心算

```bash
python launcher.py --task mental_arithmetic --participant sub01 --session 001
```

任务说明见 `tasks/mental_arithmetic/README.md`。

## 单独运行视频学习

```bash
python launcher.py --task learning_cycle --participant sub01 --session 001
```

任务说明见 `tasks/learning_cycle/README.md`。
