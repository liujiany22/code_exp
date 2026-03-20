# Learning Cycle

视频学习任务当前按“单组正式材料”运行，正式 protocol 只启用 `fourier_protocol`。

## 当前正式结构

当前正式流程只运行 1 组视频学习材料：

1. 前测
2. 视频播放
3. 后测

其中：

- 前测 = 先口头复述，再完成 10 道判断题
- 后测 = 先口头复述，再完成 10 道判断题
- 判断题按键为 `F = 对`、`J = 错`
- 判断题时序为：陈述 `4s` + 作答 `4s` + 间隔 `1s`

## 视频播放

- 视频文件从 `code_exp/stimuli/videos/` 读取
- 当前正式材料文件名为 `fourier_protocol.mp4`
- 播放前会在临时缓存目录中按 `3 分钟`切分视频片段
- 每段播放结束后都会插入一个 `1-5` 评分条
- 最后一段播放结束后也会再出现一次 `1-5` 评分条

评分支持两种输入方式：

- 鼠标点击 `1-5`
- 键盘数字 `1-5`

## 当前题表与问卷

正式 protocol 条件表：

- [learning_cycle_trials_protocol.csv](/Users/liujiany/work/CognitiveLoad/code_exp/stimuli/conditions/learning_cycle_trials_protocol.csv)

当前已接入的傅立叶问卷：

- [pretest_fourier_protocol.csv](/Users/liujiany/work/CognitiveLoad/code_exp/stimuli/questionnaires/pretest_fourier_protocol.csv)
- [posttest_fourier_protocol.csv](/Users/liujiany/work/CognitiveLoad/code_exp/stimuli/questionnaires/posttest_fourier_protocol.csv)

两份文件当前均为 `10` 道判断题。

## 输出文件

任务会写出：

- `learning_cycle_trial_log.csv`
- `learning_cycle_questionnaire_responses.csv`
- `learning_cycle_recall_responses.csv`
- `learning_cycle_segment_ratings.csv`
- `learning_cycle_events.csv`
- `learning_cycle_order.csv`
- `learning_cycle_config.json`

## 运行

```bash
python launcher.py --task learning_cycle --participant sub01 --session 001
```

如果只想在 protocol 里单独测试这一阶段：

```bash
python launcher.py --test-mode --test-stage learning_cycle --auto-advance
```
