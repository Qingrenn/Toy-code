import os
import sys
import time
import re
from multiprocessing import Process, process

# 最大等待时间 (hour)
MAX_WAITING_TIME = 24 
# 待启动的任务列表
task_commands = ["command 1", "command 2", "command 3"] 
# 排队的显卡id， 两张显卡则为[0, 1] 
gpu_id_list = [0, 1, 2] 

def write_log(writting_line, re_init=False, file_name='./waiting.log'):
    if re_init:
        f = open(file_name, 'w')
        f.close()
    print(writting_line.strip())
    f = open(file_name, 'a')
    f.write('{}\n'.format(writting_line.strip()))
    f.close()

# | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
def gpus_info():
    gpus_status = os.popen('nvidia-smi | grep %').read().strip().split('\n')
    split_col = lambda info: info.split('|')[1:-1]
    split_unit = lambda info: re.split(r'[ ]+', info.strip())
    
    gpus_status_list = []
    for gpu_status in gpus_status:
        cols_info = [split_unit(info) for info in split_col(gpu_status)] # 将一行划分为三个列，每列再划分为多个单元
        
        gpu_status = {}
        gpu_status["Fan"] = int(cols_info[0][0][:-1]) # 第一列 第一个数据 去掉单位
        gpu_status["Temp"] = int(cols_info[0][1][:-1])
        gpu_status["Perf"] = cols_info[0][2]
        gpu_status["Pwr:Usage"] = int(cols_info[0][3][:-1])
        gpu_status["Pwr:Cap"] = int(cols_info[0][-1][:-1])
        gpu_status["Memory-Usage"] =  int(cols_info[1][0][:-3]) # 第二列 第一个数据 去掉单位
        gpu_status["Memory-Total"] = int(cols_info[1][-1][:-3])
        gpu_status["GPU-Util"] = int(cols_info[2][0][:-1]) # 第三列 第一个数据 去掉单位
        
        gpus_status_list.append(gpu_status)
    return gpus_status_list

def check():
    gpu_status_list = gpus_info()
    for gpu_id, status in enumerate(gpu_status_list): 
        if status['Memory-Usage'] < 1024 and status['GPU-Util'] < 10:
           return gpu_id
    else:
        return -1

def record():
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    write_log(f'{now}: ')
    gpu_status_list = gpus_info()
    for gpu_id, status in enumerate(gpu_status_list):
        write_log('GPU:{} Memory-Usage:{} GPU-Util:{}'.format(gpu_id, status['Memory-Usage'], status['GPU-Util']))

"""
当 cmd = "python [YOUR SCRIPT]"
可以在[YOUR SCRIPT]中添加参数解析(argparse), 解析传入的gpu_id

e.g.

1. 首先在主程序中向do_cmd传入id参数
p = Process(target=do_cmd, args=(task_commands[task_index], id=gpu_id)) # 开启新的进程

2. 补充id参数到命令上
def do_cmd(cmd, **kwargs):
    gpu_id = kwargs["id"]
    cmd = cmd + " --gpu_id id"
    os.system(cmd)
"""
def do_cmd(cmd, **kwargs):
    os.system(cmd)

if __name__ == '__main__':
    write_log(f"current process PID: {os.getpid()}")
    
    task_index = 0
    process_list = []

    t = 0
    while(t < MAX_WAITING_TIME * 60):
        if task_index == len(task_commands):
            write_log("Have started all tasks ...")
            break
        
        # 记录
        if t % 10 == 0:
            record()
        # 检查
        gpu_id = check()
        if gpu_id in gpu_id_list:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 创建进程，启动任务
            p = Process(target=do_cmd, args=(task_commands[task_index])) 
            p.start()
            process_list.append(p)
            write_log(f'{now}: GPU {gpu_id} is free... start task{task_index} cmd:{task_commands[task_index]} name:{p.name} pid:{p.pid}') 
            task_index += 1
        # 检查频率
        time.sleep(60)
        t += 1

    write_log("waiting for subprocess end ...")
    for i, p in enumerate(process_list):
        p.join()
        write_log(f"Process{i}:{p.name} PID:{p.pid} is_alive:{p.is_alive()}")