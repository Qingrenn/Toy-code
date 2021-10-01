import cv2 as cv
import numpy as np
import argparse
import os.path as osp

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default="wujin.jpeg",help="your input avatar path")
parser.add_argument('-o', '--output', default='ch_avatar.png', help="your output avatar path")
parser.add_argument('-r', '--ratio', type=float, default=1, help="guoqi scaling ratio")
parser.add_argument('-s', '--is_show', type=bool, default=False, help="start windows for debug")

def create_mask(h, w):
    mask = np.zeros((h,w), dtype=np.float32)
    for row in range(h):
        start = np.int(np.abs(np.sin(row * np.pi / (h//2)) * w//6)) # 红旗覆盖到w//6的左边界
        mask[row, start:w] = np.linspace(0, 255, w - start)
    mask = mask / 255.0;
    return mask

if __name__ == "__main__":
    args = parser.parse_args()
    assert osp.exists(args.input), "Can not find your input avatar ..."
    assert osp.exists("./output"), "Can not find your output path ..."
    assert 0.5 <= args.ratio <= 1.2, "Ratio is not suitable ..."
    
    # 读取输入头像和国旗
    input_avatar = cv.imread(args.input)
    h, w , _ = input_avatar.shape
    gq = cv.imread("./guoqi/gq_1024.png") # (683, 1024, 3) 

    # 按ratio调整国旗尺寸
    gq = cv.resize(gq, (int(h*args.ratio/683*1024), int(h*args.ratio)), interpolation=cv.INTER_CUBIC)
    if args.ratio < 1.0: # 用红色做pading，pading至头像大小
        red = np.array([37, 28, 238], dtype=np.float32)
        red = np.tile(red, [h, w, 1])
        cv.imshow("red", red)
        red[: gq.shape[0], : gq.shape[1], :] = gq[:, :, :]
        gq = red

    # 创建mask
    mask = create_mask(h, w)

    # 生成新头像
    output_avatar = np.zeros_like(input_avatar)
    for row in range(h):
        for col in range(w):
            m1 = mask[row, col]
            m2 = 1 - m1
            output_avatar[row, col] = m2*np.array(gq[row, col]) + m1*np.array(input_avatar[row, col])
    
    cv.imwrite(osp.join("./output", args.output), output_avatar)
    print(f"your new avatar saved in ./output/{args.output} ...")

    if args.is_show:
        cv.imshow("input", input_avatar)
        cv.imshow("Step1-gq", gq)
        cv.imshow("Step2-mask", mask)
        cv.imshow("Step3-output", output_avatar)
        cv.waitKey(10)
        cv.destroyAllWindows()
   

