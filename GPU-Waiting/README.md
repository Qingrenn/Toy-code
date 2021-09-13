将你的终端指令添加入task_commands列表中。

脚本每隔1分钟扫描一次显卡状态，选择空闲的显卡去启动任务。

当等待时间超过最大限制MAX_WAITING_TIME，则会放弃等待。

在等待的最大限制MAX_WAITING_TIME内，会逐个启动你的任务列表中的指令。

**运行日志会打印当前进程和子进程的PID，发现问题，及时Kill。**

如果cmd启动的是shell脚本，请自行存储训练脚本pid:

```shell
nohup python your_py_script.py 2>&1 & echo $! > pid.txt
```