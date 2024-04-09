from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt

R = 100

initial_coords = [
    (0, 0),
    (100, 0),
    (98, 40.10),
    (112, 80.21),
    (105, 119.75),
    (98, 159.86),
    (112, 199.96),
    (105, 240.07),
    (98, 280.17),
    (112, 320.28)
]

def positioning_model(a1_deg, a2_deg, number):

    a1 = np.radians(a1_deg)
    a2 = np.radians(a2_deg)
    def equations(vars):
            d, b1, b2 = vars
            f1 = R / np.sin(a1) - d / np.sin(b1)
            f2 = R / np.sin(a2) - d / np.sin(b2)
            if number == 2 or number == 3:
                f3 = a1 + a2 + b1 + b2 - 4*np.pi / 3
            elif number == 5:
                f3 = a2 + b2 -a1 - b1 - 2*np.pi / 3
            elif number == 9:
                f3 = a1 + b1 - a2 - b2 - 2*np.pi / 3
            else:
                f3 = a1 + a2 + b1 + b2 - 2*np.pi / 3
            return [f1, f2, f3]

    x0 = [50, 0.15, 0.15]

    solution = fsolve(equations, x0)

    if number > 5:
        degree = np.pi + solution[1] + a1
    else :
        degree = np.pi - solution[1] - a1

    return {
        "d": solution[0],
        "b1_deg": np.degrees(solution[1]),  
        "b2_deg": np.degrees(solution[2]),   
        "x": np.cos(degree) * R,
        "y": np.sin(degree) * R,
        "degree": np.degrees(degree)
    }


def angle_calculating(firstDis, firstAng, secondDis, secondAng):
    firstAng = np.radians(firstAng)
    secondAng = np.radians(secondAng)
     
    ang1 = np.pi - secondAng
    ang2 = secondAng - firstAng

    def equations(vars):
          a4, b4, a7, b7, c1, c2 = vars
          f1 = secondDis / np.sin(b4) - firstDis / np.sin(b7)
          f2 = np.pi - ang2 - b4 - b7
          f3 = firstDis / np.sin(c1) - 100 / np.sin(a4)
          f4 = secondDis / np.sin(c2) - 100 / np.sin(a7)
          f5 = secondAng - a7 - c2 - np.pi
          f6 = c1 + a4 + firstAng - np.pi
          return [f1, f2, f3, f4, f5, f6]

    x0 = [30, 30, 30, 30, 30, 30]

    solution = fsolve(equations, x0)

    return {
          "a4":solution[0],
          "b4":solution[1],
          "a7":solution[2],
          "b7":solution[3],
          "c1":solution[4],
          "c2":solution[5]
    }

def adjust_down(upDis, upAng):
     upAng = np.radians(upAng)
     def eqations(vars):
          b4, c2, d = vars
          f1 = d / np.sin(c2) - 200
          f2 = d / np.sin(b4) - 2 * upDis
          f3 = c2 + b4 - upAng + np.pi / 3
          return [f1, f2, f3]
     
     x0 = [0.15, 0.15, 100]

     solution = fsolve(eqations, x0)
     return {
          "b4": np.degrees(solution[0]),
          "c2": np.degrees(solution[1]),
          "newDis": solution[2],
          "newDeg": np.degrees(5 * np.pi / 6 - solution[0] + upAng)
     }

def adjust_up(bottomDis, bottomAng):
     bottomAng = np.radians(bottomAng)
     def eqations(vars):
          b7, c1, d = vars
          f1 = d / np.sin(c1) - 200
          f2 = d / np.sin(b7) - 2 * bottomDis
          f3 = c1 + b7 + bottomAng - 5 * np.pi / 3
          return [f1, f2, f3]
     
     x0 = [0.15, 0.15, 100]

     solution = fsolve(eqations, x0)
     return {
          "b7": np.degrees(solution[0]),
          "c1": np.degrees(solution[1]),
          "newDis": solution[2],
          "newDeg": np.degrees(5 * np.pi / 6 - solution[1])
     }

def base_adjustment(coords): 
     while(abs(coords[4][0] - 100) > 0.0001 or abs(coords[7][0] - 100) > 0.0001 or abs(coords[4][1] - 120) > 0.0001 or abs(coords[7][1] - 240) > 0.0001):
          newDown = adjust_down(coords[4][0], coords[4][1])
          coords[7] = (newDown["newDis"], newDown["newDeg"])
          newUp = adjust_up(coords[7][0], coords[7][1])
          coords[4] = (newUp["newDis"], newUp["newDeg"])

def main_adjustment(coords):
     for i in range(2, 10):
          if i!=4 and i!=7:
                top_ang1 = 40 * (i - 1)
                if top_ang1 < 180:
                    a1 = (180 - top_ang1) / 2
                else:
                    a1 = (top_ang1 - 180) / 2
                top_ang2 = 40 * abs(i - 4)
                if top_ang2 < 180: 
                    a2 = (180 - top_ang2) / 2
                else:
                    a2 = (top_ang2 - 180) / 2
                newPos = positioning_model(a1, a2, i)
                coords[i] = (newPos["d"], newPos["degree"])
               
               

def paint(polar_coords):
    x = [r * np.cos(np.radians(theta)) for r, theta in polar_coords]
    y = [r * np.sin(np.radians(theta)) for r, theta in polar_coords]

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.scatter([np.radians(theta) for _, theta in polar_coords], [r for r, _ in polar_coords])

    ax.set_theta_zero_location('E')
    ax.set_theta_direction(-1) 

    plt.title('Polar Coordinates Plot')
    plt.show()

example_solution = positioning_model(30, 30, 7)

#angles = angle_calculating(105, 119.75, 105, 240.07)



#print(adjust_down(105, 119.75))
#print(adjust_up(102.04167447741602, 240.6777103181801))
#print(adjust_down(99.97239538539297, 120.00913111303957))


#print(positioning_model(70, 50, 2))


paint(initial_coords)

base_adjustment(initial_coords)

print(initial_coords)

main_adjustment(initial_coords)

print(initial_coords)

paint(initial_coords)
