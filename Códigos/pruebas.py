import numpy as np
import matplotlib.pyplot as plt

# Parámetros del sistema
m = 1.0       # masa de cada cuchilla (kg)
L = 1.0       # longitud de las cuchillas (m)
r = 0.5       # distancia pivote-centro (m)
b1 = b2 = 0.05  # coeficientes de rozamiento (kg·m^2/s)
phi_dot = 2.0  # velocidad angular constante del disco (rad/s)

# Función que calcula las derivadas
def deriv(y, t):
    th1, th1_dot, th2, th2_dot = y
    # Torque centrífugo y resistivo cuchilla 1
    term_cent1 = 0.5*m*r*L*phi_dot*2*np.sin(th1) + (1/3)*m*L2*phi_dot*2*np.sin(th1)*np.cos(th1)
    term_res1  = 0.5*b1*r*L*2*phi_dot*np.sin(th1) + (1/3)*b1*L*3*th1_dot
    th1_ddot   = 3/(m*L**2) * (term_cent1 - term_res1)
    # Torque centrífugo y resistivo cuchilla 2
    term_cent2 = 0.5*m*r*L*phi_dot*2*np.sin(th2) + (1/3)*m*L2*phi_dot*2*np.sin(th2)*np.cos(th2)
    term_res2  = 0.5*b2*r*L*2*phi_dot*np.sin(th2) + (1/3)*b2*L*3*th2_dot
    th2_ddot   = 3/(m*L**2) * (term_cent2 - term_res2)
    return np.array([th1_dot, th1_ddot, th2_dot, th2_ddot])

# Condiciones iniciales y malla temporal
t0, tf, dt = 0.0, 10.0, 0.01
t = np.arange(t0, tf + dt, dt)
y = np.zeros((len(t), 4))
y[0] = [0.1, 0.0, -0.1, 0.0]  # [θ1, θ1˙, θ2, θ2˙] en t=0

# Integración con RK4
for i in range(len(t) - 1):
    k1 = deriv(y[i], t[i])
    k2 = deriv(y[i] + dt*k1/2, t[i] + dt/2)
k3 = deriv(y[i] + dt*k2/2, t[i] + dt/2)
    k4 = deriv(y[i] + dt*k3, t[i] + dt)
    y[i+1] = y[i] + dt*(k1 + 2*k2 + 2*k3 + k4)/6

theta1 = y[:, 0]
theta2 = y[:, 2]

# Gráfica
plt.figure()
plt.plot(t, theta1, label='θ1')
plt.plot(t, theta2, label='θ2')
plt.xlabel('t (s)')
plt.ylabel('θ (rad)')
plt.title('Ángulos de las cuchillas vs tiempo')
plt.legend()
plt.grid(True)
plt.show()

