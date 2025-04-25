import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ------------------------
# Parámetros del sistema
# ------------------------
M = 5.0            # masa del disco
m = 0.1            # masa de cada cuchilla
R = 1.0            # radio del disco
r = 0.8            # distancia pivote
L = 0.8            # longitud de la cuchilla

# ------------------------
# Coeficientes ajustables
# ------------------------
b1 = b2= 0.0       # densidad del pasto
c_disk = 0.0       # fricción viscosa del disco
c_th1 = 0.0        # amortiguamiento pivote cuchilla 1
c_th2 = 0.0        # amortiguamiento pivote cuchilla 2
k1 = 0.0           # constante de resorte torsional cuchilla 1
k2 = 0.0           # constante de resorte torsional cuchilla 2
theta01 = np.pi/2  # ángulo “full extend” cuchilla 1
theta02 = np.pi/2  # ángulo “full extend” cuchilla 2

# Torque del motor (constante o función de t)
def tau_motor(t):
    return 2.0

# Sistema de EDOs
def odes(t, y):
    phi, phidot, th1, dth1, th2, dth2 = y
    
    # Momentos de inercia
    I_disc  = 0.5 * M * R**2
    I_blade = (1/3) * m * L**2
    I_tot   = I_disc + 2 * I_blade
    
    # Torque resistivo por pasto
    def tau_res_blade(phi_dot, theta, theta_dot, b):
        disc_term  = b * phi_dot * np.sin(theta) * (r*L**2/2 + L**3*np.cos(theta)/3)
        blade_term = (1/3) * b * L**3 * theta_dot * np.sin(theta)
        return disc_term + blade_term
    
    t_res1 = tau_res_blade(phidot, th1, dth1, b1)
    t_res2 = tau_res_blade(phidot, th2, dth2, b2)
    
    # Ecuación de φ̈ con fricción del disco
    phidd = (tau_motor(t) - (t_res1 + t_res2) - c_disk * phidot) / I_tot
    
    # Ecuación de θ̈ para cada cuchilla
    def theta_ddot(phi_dot, theta, theta_dot, b, c_th, k, theta0):
        # Si no hay pasto, fricción ni resorte, mantenemos θ constante
        if b == 0 and c_th == 0 and k == 0:
            return 0.0
        
        cent1      = 0.5 * m * r * L * phi_dot**2 * np.sin(theta)
        cent2      = (1/3) * m * L**2 * phi_dot**2 * np.sin(theta) * np.cos(theta)
        res_blade  = (1/2)*b * r * L**2 * phi_dot * np.sin(theta) + (1/3)*b * L**3 * theta_dot * np.sin(theta)
        spring     = -k * (theta - theta0)
        damp       = -c_th * theta_dot
        
        return (cent1 + cent2 - res_blade + spring + damp) / I_blade
    
    dth1dd = theta_ddot(phidot, th1, dth1, b1, c_th1, k1, theta01)
    dth2dd = theta_ddot(phidot, th2, dth2, b2, c_th2, k2, theta02)
    
    return [phidot, phidd, dth1, dth1dd, dth2, dth2dd]

# Condiciones iniciales: ponemos las palas en full extend
y0    = [0, 0, theta01, 0, theta02, 0]
t_span = (0, 30)
t_eval = np.linspace(*t_span, 400)

# Resolver
sol = solve_ivp(odes, t_span, y0, t_eval=t_eval)

# Graficar φ(t)
plt.figure()
plt.plot(sol.t, sol.y[0] % (2*np.pi))
plt.ylim(0, 2*np.pi)
plt.xlabel('Tiempo (s)')
plt.ylabel('φ mod 2π (rad)')
plt.title('Disco φ(t) [0,2π]')
plt.grid(True)

# Graficar θ1(t) y θ2(t)
for idx, label in zip([2, 4], ['θ1', 'θ2']):
    plt.figure()
    plt.plot(sol.t, sol.y[idx] % (2*np.pi))
    plt.ylim(0, 2*np.pi)
    plt.xlabel('Tiempo (s)')
    plt.ylabel(f'{label} mod 2π (rad)')
    plt.title(f'Cuchilla {label}(t) [0,2π]')
    plt.grid(True)

plt.show()

# asumimos que ya tienes: sol = solve_ivp(...), y R definido

# extraer φ(t)
phi = sol.y[0]      # φ en cada instante

# calcular coordenadas del borde del disco
x_disk = R * np.cos(phi)
y_disk = R * np.sin(phi)

# y para graficar de nuevo:
import matplotlib.pyplot as plt
plt.figure()
plt.plot(x_disk, y_disk, '.', markersize=2)
plt.axis('equal')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Borde del disco')
plt.grid(True)
plt.show()
