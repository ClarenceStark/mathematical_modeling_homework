import numpy as np
from scipy.optimize import fsolve

R = 100

def positioning_model(a1_deg, a2_deg, number):

    a1 = np.radians(a1_deg) 
    a2 = np.radians(a2_deg) #先将输入角度转换为弧度（numpy期望三角函数的单位为弧度）
    def equations(vars):
            d, b1, b2 = vars #设定待解变量d b1 b2
            f1 = R / np.sin(a1) - d / np.sin(b1)
            f2 = R / np.sin(a2) - d / np.sin(b2) #两个正弦定理方程 对所有情况适用
            if number == 2 or number == 3:
                f3 = a1 + a2 + b1 + b2 - 4*np.pi / 3
            elif number == 5:
                f3 = a2 + b2 -a1 - b1 - 2*np.pi / 3
            elif number == 9:
                f3 = a1 + b1 - a2 - b2 - 2*np.pi / 3
            else:
                f3 = a1 + a2 + b1 + b2 - 2*np.pi / 3 #因为我们假设待定位飞机知道自己的编号，所以我们这里分编号情况讨论，列出第三个角度关系方程
            return [f1, f2, f3]

    x0 = [50, 0.15, 0.15] #设定估计值

    solution = fsolve(equations, x0)

    if number > 5:
        degree = np.pi + solution[1] + a1
    else :
        degree = np.pi - solution[1] - a1 #分情况计算极角

    return {
        "d": solution[0],
        "b1_deg": np.degrees(solution[1]),  
        "b2_deg": np.degrees(solution[2]),   
        "x": np.cos(degree) * R,
        "y": np.sin(degree) * R,
        "degree": np.degrees(degree)
    }