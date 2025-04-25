import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parámetros del sistema
M = 0.5       # masa del disco
m = 0.1      # masa de cada cuchilla
R = 3.0       # radio del disco
r = 2.4       # distancia pivote
L = 0.8       # longitud de la cuchilla
b1 = 1     # coeficiente viscocidad cuchilla 1
b2 = 1     # coeficiente viscocidad cuchilla 2

# Torque del motor, aquí constante
def tau_motor(t):
    return 2.0

# Sistema de ecuaciones ODE
def odes(t, y):
    phi, phidot, theta1, th1dot, theta2, th2dot = y
    
    # Momentos de inercia
    I_disc = 0.5 * M * R**2
    I_blade = (1/3) * m * L**2
    I_tot = I_disc + 2*I_blade
    
    # Torques resistivos (disco corregido) para cada pala
    def tau_res_blade(phi_dot, theta, theta_dot, b):
        term_disc = b * phi_dot * np.sin(theta) * (r*L**2/2 + L**3*np.cos(theta)/3)
        term_blade = (1/3)*b * L**3 * theta_dot * np.sin(theta)
        return term_disc + term_blade
    
    # Ecuación para phï
    t_res1 = tau_res_blade(phidot, theta1, th1dot, b1)
    t_res2 = tau_res_blade(phidot, theta2, th2dot, b2)
    phidd = (tau_motor(t) - (t_res1 + t_res2)) / I_tot
    
    # Ecuación para θ̈_i (cuchilla)
    def theta_ddot(phi_dot, theta, theta_dot, b):
        # Términos centrífugos
        term_cent1 = 0.5 * m * r * L * phi_dot**2 * np.sin(theta)
        term_cent2 = (1/3) * m * L**2 * phi_dot**2 * np.sin(theta) * np.cos(theta)
        # Resistivo de cuchilla
        term_res_blade_only = (1/2)*b * r * L**2 * phi_dot * np.sin(theta) + (1/3)*b * L**3 * theta_dot * np.sin(theta)
        return (term_cent1 + term_cent2 - term_res_blade_only) / ((1/3) * m * L**2)
    
    th1dd = theta_ddot(phidot, theta1, th1dot, b1)
    th2dd = theta_ddot(phidot, theta2, th2dot, b2)
    
    return [phidot, phidd, th1dot, th1dd, th2dot, th2dd]

# Condiciones iniciales [φ, φ̇, θ1, θ̇1, θ2, θ̇2]
y0 = [0, 0, 0.1, 0, 0.1, 0]

# Intervalo de tiempo
t_span = (0, 100)
t_eval = np.linspace(*t_span, 500)

# Resolver ODE
sol = solve_ivp(odes, t_span, y0, t_eval=t_eval, vectorized=False)

# Graficar φ(t)
plt.figure()
plt.plot(sol.t, sol.y[0])
plt.xlabel('Tiempo (s)')
plt.ylabel('φ (rad)')
plt.title('Ángulo del disco φ(t)')
plt.grid(True)

# Graficar θ1(t)
plt.figure()
plt.plot(sol.t, sol.y[2])
plt.xlabel('Tiempo (s)')
plt.ylabel('θ1 (rad)')
plt.title('Ángulo cuchilla 1 θ1(t)')
plt.grid(True)

# Graficar θ2(t)
plt.figure()
plt.plot(sol.t, sol.y[4])
plt.xlabel('Tiempo (s)')
plt.ylabel('θ2 (rad)')
plt.title('Ángulo cuchilla 2 θ2(t)')
plt.grid(True)

plt.show()


