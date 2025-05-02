
# Modelo de Disco Rotatorio con Cuchillas

Este repositorio contiene el código para simular un disco con dos cuchillas sometidas a torques de fricción, resortes y amortiguamiento. A continuación se listan las principales ecuaciones y parámetros del modelo.

---

## Parámetros del Sistema

- Masa del disco: $M$
- Masa de cada cuchilla: $m$
- Radio del disco: $R$
- Distancia pivote: $r$
- Longitud de la cuchilla: $L$
- Densidad de pasto cuchilla 1: $b_1$
- Densidad de pasto cuchilla 2: $b_2$
- Fricción viscosa del disco: $c_{\mathrm{disk}}$
- Amortiguamiento pivote cuchilla 1: $c_{th1}$
- Amortiguamiento pivote cuchilla 2: $c_{th2}$
- Constante de resorte torsional cuchilla 1: $k_1$
- Constante de resorte torsional cuchilla 2: $k_2$
- Ángulo “full extend” cuchilla 1: $\theta_{01}$
- Ángulo “full extend” cuchilla 2: $\theta_{02}$

---

## Momentos de Inercia

$$
I_{disc}=\frac{1}{2}MR^2
$$

$$
I_{blade}=\frac{1}{3}mL^2
$$

---

## Torque del Motor

$$
\tau_{\mathrm{motor}}(t)\;=\;2.0
$$

---
