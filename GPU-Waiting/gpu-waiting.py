import os
import sys
import time
import re
from multiprocessing import Process, process

MAX_WAITING_TIME = 24 # hour

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
        if status['Memory-Usage'] < 1000 and status['GPU-Util'] < 10:
           return gpu_id
    else:
        return -1

def record():
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    write_log(f'{now}: ')
    gpu_status_list = gpus_info()
    for gpu_id, status in enumerate(gpu_status_list):
        write_log('GPU:{} Memory-Usage:{} GPU-Util:{}'.format(gpu_id, status['Memory-Usage'], status['GPU-Util']))

def do_cmd(cmd):
    os.system(cmd)

if __name__ == '__main__':
    write_log(f"current process PID: {os.getpgid()}")
    task_commands = ["command 1", "command 2", "command 3"] # 待启动的任务列表
    task_index = 0
    process_list = []
    gpu_id_list = [0, 1, 2] # 排队的显卡id， 两张显卡则为[0, 1] 

    t = 0
    while(t < MAX_WAITING_TIME * 60):
        if task_index == len(task_commands):
            write_log("start all tasks ...")
            break
        
        # 记录
        if t % 10 == 0:
            record()
        # 检查
        gpu_id = check()
        if gpu_id in gpu_id_list:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            p = Process(target=do_cmd, args=(task_commands[task_index])) # 开启新的进程
            p.start()
            process_list.append(p)
            # 如果启动的是shell脚本， 请自行存储训练脚本的pid
            write_log(f'{now}: GPU {gpu_id} is free... start task{task_index} cmd:{task_commands[task_index]} name:{p.name} pid:{p.pid}') 
            task_index += 1
        # 检查频率
        time.sleep(60)
        t += 1

    write_log("waiting for subprocess end ...")
    for i, p in enumerate(process_list):
        p.join()
        write_log(f"Process{i}:{p.name} PID:{p.pid} is_alive:{p.is_alive()}")