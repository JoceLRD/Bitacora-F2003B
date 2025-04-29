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
b1 = 1e4     # densidad de pasto cuchilla 1
b2 = 1       # densidad de pasto cuchilla 2
c_disk = 1     # fricción viscosa del disco
c_th1 = 1    # amortiguamiento pivote cuchilla 1
c_th2 = 0.1    # amortiguamiento pivote cuchilla 2
k1 = 5.0         # constante de resorte torsional cuchilla 1
k2 = 0         # constante de resorte torsional cuchilla 2
theta01 = 3.14   # ángulo “full extend” cuchilla 1
theta02 = 0    # ángulo “full extend” cuchilla 2

def tau_motor(t):
    return 2.0

# Momentos de inercia
I_disc  = 0.5 * M * R**2
I_blade = (1/3) * m * L**2

def tau_disc_b(phi_dot, theta, theta_dot, b):
    """
    Torque que ejerce el pasto sobre el disco (reacción)
    """
    term_phi  = b * phi_dot   * np.sin(theta) * (r*L**2/2 + (L**3/3)*np.cos(theta))
    term_th   = b * theta_dot * np.sin(theta) * (L**3/3)
    return term_phi + term_th

def tau_blade_b(phi_dot, theta, theta_dot, b):
    """
    Torque que ejerce el pasto sobre la cuchilla (resistencia local)
    """
    term_cut  = b * phi_dot   * np.sin(theta) * (r*L**2/2)
    term_drag = b * theta_dot * np.sin(theta) * (L**3/3)
    return term_cut + term_drag

def theta_dd(phi_dot, theta, theta_dot, b, c_th, k, theta0):
    """
    Aceleración angular de la cuchilla:
      I_blade * θ¨ = -centrífugos - τ_blade_b - c_th*θ˙ - k*(θ-θ0)
    """
    # términos centrífugos
    cent1 = 0.5 * m * r * L * phi_dot**2 * np.sin(theta)
    cent2 = (1/3) * m * L**2 * phi_dot**2 * np.sin(theta) * np.cos(theta)
    # torque de pasto sobre cuchilla
    tau_g = tau_blade_b(phi_dot, theta, theta_dot, b)
    # resorte y amortiguamiento
    tau_s = -k * (theta - theta0)
    tau_d = -c_th * theta_dot
    # ecuación final
    return (-cent1 - cent2 - tau_g + tau_s + tau_d) / I_blade

def odes(t, y):
    phi, phidot, th1, dth1, th2, dth2 = y
    I_tot = I_disc + 2*(m*r**2 + I_blade)

    # torques de pasto sobre el disco
    t1 = tau_disc_b(phidot, th1, dth1, b1)
    t2 = tau_disc_b(phidot, th2, dth2, b2)

    # ecuación del disco
    phidd = (tau_motor(t) - t1 - t2 - c_disk*phidot) / I_tot

    # aceleraciones de las cuchillas
    dth1dd = theta_dd(phidot, th1, dth1, b1, c_th1, k1, theta01)
    dth2dd = theta_dd(phidot, th2, dth2, b2, c_th2, k2, theta02)

    return [phidot, phidd, dth1, dth1dd, dth2, dth2dd]

# Condiciones iniciales y resolución
y0 = [0, 0, theta01, 0, theta02, 0]
t_span = (0, 100)
t_eval = np.linspace(*t_span, 1000)
sol = solve_ivp(odes, t_span, y0, t_eval=t_eval)

# Extracción y gráficos (igual que antes
# Extraer ángulos
t = sol.t
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