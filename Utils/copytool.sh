#!/bin/bash

# bash copytool.sh [SourceDir] [TargetDir]
# 复制 [SourceDir] 目录下前100个文件到 [TargetDir] 下
# 第一个参数是要复制的文件夹的根目录，第二个参数目标文件夹
# 注意： 路径请以 / 结尾

SourceDir=$1
TargetDir=$2
N=2

TopNFiles=$(ls ${SourceDir} | sed "s:^:${SourceDir}:" | head -n ${N} | tr "\n" " ")
echo $TopNFiles > copyFiles.log
cp -R ${TopNFiles} ${TargetDir}

# Last900Files=$(ls ${SourceDir} | sed "s:^:`pwd`/:" | tail -n ${N} | tr "\n" " ")
# echo $Last900Files > copyFiles.log
# cp -R ${Last900Files} ${TargetDir}

