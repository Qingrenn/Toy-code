将你的终端指令添加入task_commands列表中。

脚本每隔1分钟扫描一次显卡状态，选择空闲的显卡去启动任务。

当等待时间超过最大限制MAX_WAITING_TIME，则会放弃等待。

在等待的最大限制MAX_WAITING_TIME内，会逐个启动你的任务列表中的指令。

## 如何使用

1. 将shell指令添加至 `task_commands` 列表
2. 修改需要等待的显卡id， 若等待多张显卡，那么请为自己的代码增加对命令行参数gpu_id的解析
3. 修改等待条件, 在`check()`初始化的条件是GPU显存占用不超过1G, GPU利用率不超过10%才执行命令。该条件可能较严格，按需求更改。


PS: 如果cmd启动的是shell脚本，请自行存储训练脚本pid:
```shell
nohup python your_py_script.py 2>&1 & echo $! > pid.txt
```