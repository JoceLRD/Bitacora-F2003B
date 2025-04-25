import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# -- Parámetros del sistema (ajusta según tu modelo) --
M = 5.0      # masa del disco
m = 0.1      # masa de cada cuchilla
R = 1.0      # radio del disco
r = 0.8      # distancia pivote
L = 0.8      # longitud de la cuchilla

# ------------------------
# Coeficientes ajustables
# ------------------------
b1 = 0          # densidad del pasto cuchilla 1
b2 = 0     # densidad del pasto cuchilla 2
c_disk = 1       # fricción viscosa del disco
c_th1 = 0        # amortiguamiento pivote cuchilla 1
c_th2 = 0        # amortiguamiento pivote cuchilla 2
k1 = 0           # constante de resorte torsional cuchilla 1
k2 = 0           # constante de resorte torsional cuchilla 2
theta01 = np.pi/2  # ángulo “full extend” cuchilla 1
theta02 = np.pi/2  # ángulo “full extend” cuchilla 2

def tau_motor(t):
    return 2.0

def odes(t, y):
    phi, phidot, th1, dth1, th2, dth2 = y
    I_disc  = 0.5*M*R**2
    I_blade = (1/3)*m*L**2
    I_tot   = I_disc + 2*I_blade

    # torque de pasto
    def tau_res_blade(phi_dot, theta, theta_dot, b):
        disc_term  = b*phi_dot*np.sin(theta)*(r*L**2/2 + L**3*np.cos(theta)/3)
        blade_term = (1/3)*b*L**3*theta_dot*np.sin(theta)
        return disc_term + blade_term

    t_res1 = tau_res_blade(phidot, th1, dth1, b1)
    t_res2 = tau_res_blade(phidot, th2, dth2, b2)

    phidd = (tau_motor(t) - (t_res1 + t_res2) - c_disk*phidot) / I_tot

    # aceleración de cuchilla
    def theta_ddot(phi_dot, theta, theta_dot, b, c_th, k, theta0):
        if b==0 and c_th==0 and k==0:
            return 0.0
        cent1     = 0.5*m*r*L*phi_dot**2*np.sin(theta)
        cent2     = (1/3)*m*L**2*phi_dot**2*np.sin(theta)*np.cos(theta)
        res_blade = (1/2)*b*r*L**2*phi_dot*np.sin(theta) + (1/3)*b*L**3*theta_dot*np.sin(theta)
        spring    = -k*(theta-theta0)
        damp      = -c_th*theta_dot
        return (cent1 + cent2 - res_blade + spring + damp) / I_blade

    dth1dd = theta_ddot(phidot, th1, dth1, b1, c_th1, k1, theta01)
    dth2dd = theta_ddot(phidot, th2, dth2, b2, c_th2, k2, theta02)

    return [phidot, phidd, dth1, dth1dd, dth2, dth2dd]

# Condiciones iniciales
y0 = [0, 0, theta01, 0, theta02, 0]
t_span = (0, 30)
t_eval = np.linspace(*t_span, 400)

# Resolver ODEs
sol = solve_ivp(odes, t_span, y0, t_eval=t_eval)

# Extraer ángulos
phi    = sol.y[0]
theta1 = sol.y[2]
theta2 = sol.y[4]

# Coordenadas del borde del disco
x_disk = R * np.cos(phi)
y_disk = R * np.sin(phi)

# Coordenadas de las puntas
x_piv  = r * np.cos(phi)
y_piv  = r * np.sin(phi)
x_tip1 = x_piv + L * np.cos(phi + theta1)
y_tip1 = y_piv + L * np.sin(phi + theta1)
x_tip2 = x_piv + L * np.cos(phi + theta2)
y_tip2 = y_piv + L * np.sin(phi + theta2)


# 1) Borde del disco
plt.figure()
plt.scatter(x_disk, y_disk)
plt.title('Borde del disco')
plt.axis('equal')
plt.grid(True)

# 2) Puntas de las cuchillas
plt.figure()
plt.scatter(x_tip1, y_tip1)
plt.title('Trayectorias puntas de cuchilla 1')
plt.axis('equal')
plt.grid(True)

plt.show()

plt.figure()
plt.scatter(x_tip2, y_tip2)
plt.title('Trayectorias puntas de cuchilla 2')
plt.axis('equal')
plt.grid(True)

plt.show()

# -------------------- 
# Extraer tiempo y ángulos de la solución
t = sol.t
phi    = sol.y[0]    # ángulo del disco
theta1 = sol.y[2]    # ángulo cuchilla 1
theta2 = sol.y[4]    # ángulo cuchilla 2

# 1) φ(t)
plt.figure()
plt.plot(t, phi)
plt.xlabel('Tiempo (s)')
plt.ylabel('φ (rad)')
plt.title('Ángulo del disco φ(t)')
plt.grid(True)

# 2) θ1(t)
plt.figure()
plt.plot(t, theta1)
plt.xlabel('Tiempo (s)')
plt.ylabel('θ₁ (rad)')
plt.title('Ángulo cuchilla 1 θ₁(t)')
plt.grid(True)

# 3) θ2(t)
plt.figure()
plt.plot(t, theta2)
plt.xlabel('Tiempo (s)')
plt.ylabel('θ₂ (rad)')
plt.title('Ángulo cuchilla 2 θ₂(t)')
plt.grid(True)

plt.show()
