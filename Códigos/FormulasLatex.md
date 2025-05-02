
<!-- Incluir MathJax para renderizar LaTeX -->
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

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
I_{\mathrm{disc}} \;=\; \tfrac{1}{2}\,M\,R^2
$$

$$
I_{\mathrm{blade}} \;=\; \tfrac{1}{3}\,m\,L^2
$$

---

## Torque del Motor

$$
\tau_{\mathrm{motor}}(t)\;=\;2.0
$$

---

## Torque del Pasto sobre el Disco

$$
\tau_{\mathrm{disc},b}
= b\,\dot{\phi}\,\sin\!\theta\;\Bigl(\tfrac{r\,L^2}{2} + \tfrac{L^3}{3}\cos\!\theta\Bigr)
+ b\,\dot{\theta}\,\sin\!\theta\;\Bigl(\tfrac{L^3}{3}\Bigr)
$$

---

## Torque del Pasto sobre la Cuchilla

$$
\tau_{\mathrm{blade},b}
= b\,\dot{\phi}\,\sin\!\theta\;\Bigl(\tfrac{r\,L^2}{2}\Bigr)
+ b\,\dot{\theta}\,\sin\!\theta\;\Bigl(\tfrac{L^3}{3}\Bigr)
$$

---

## Aceleración Angular de la Cuchilla

Términos centrífugos:
$$
C_1 = \tfrac{1}{2}\,m\,r\,L\,\dot{\phi}^{2}\sin\!\theta
\quad,\quad
C_2 = \tfrac{1}{3}\,m\,L^{2}\,\dot{\phi}^{2}\sin\!\theta\,\cos\!\theta
$$

Ecuación de movimiento:
$$
I_{\mathrm{blade}}\,\ddot{\theta}
= -\,C_1 \;-\; C_2 \;-\;\tau_{\mathrm{blade},b}
\;-\; c_{th}\,\dot{\theta}
\;-\; k\,(\theta - \theta_{0})
$$

o bien
$$
\ddot{\theta}
= 
\frac{ 
  -C_1 \;-\; C_2 \;-\; \tau_{\mathrm{blade},b}
  \;-\; c_{th}\,\dot{\theta}
  \;-\; k\,(\theta - \theta_{0})
}{I_{\mathrm{blade}}}
$$

---

## Ecuaciones de Movimiento del Sistema

Definiendo
\[
y = [\phi,\;\dot{\phi},\;\theta_1,\;\dot{\theta}_1,\;\theta_2,\;\dot{\theta}_2]
\quad,\quad
I_{\mathrm{tot}} = I_{\mathrm{disc}} + 2\,\bigl(m\,r^2 + I_{\mathrm{blade}}\bigr)
\]

### Disco

$$
\ddot{\phi}
= \frac{
  \tau_{\mathrm{motor}}(t)
  \;-\;\tau_{\mathrm{disc},b}(\dot{\phi},\theta_1,\dot{\theta}_1,b_1)
  \;-\;\tau_{\mathrm{disc},b}(\dot{\phi},\theta_2,\dot{\theta}_2,b_2)
  \;-\;c_{\mathrm{disk}}\,\dot{\phi}
}{I_{\mathrm{tot}}}
$$

### Cuchilla 1

$$
\ddot{\theta}_1
= \frac{
  -C_{1,1} - C_{2,1}
  -\tau_{\mathrm{blade},b}(\dot{\phi},\theta_1,\dot{\theta}_1,b_1)
  - c_{th1}\,\dot{\theta}_1
  - k_1\,(\theta_1 - \theta_{01})
}{I_{\mathrm{blade}}}
$$

### Cuchilla 2

$$
\ddot{\theta}_2
= \frac{
  -C_{1,2} - C_{2,2}
  -\tau_{\mathrm{blade},b}(\dot{\phi},\theta_2,\dot{\theta}_2,b_2)
  - c_{th2}\,\dot{\theta}_2
  - k_2\,(\theta_2 - \theta_{02})
}{I_{\mathrm{blade}}}
$$

---

## Coordenadas Geométricas

**Borde del disco:**

$$
x_{\mathrm{disk}} = R \cos\!\phi
\quad,\quad
y_{\mathrm{disk}} = R \sin\!\phi
$$

**Punto de pivote:**

$$
x_{\mathrm{piv}} = r \cos\!\phi
\quad,\quad
y_{\mathrm{piv}} = r \sin\!\phi
$$

**Punta de cuchilla 1:**

$$
x_{\mathrm{tip}1} = x_{\mathrm{piv}} + L \cos(\phi + \theta_1)
\quad,\quad
y_{\mathrm{tip}1} = y_{\mathrm{piv}} + L \sin(\phi + \theta_1)
$$

**Punta de cuchilla 2:**

$$
x_{\mathrm{tip}2} = x_{\mathrm{piv}} + L \cos(\phi + \theta_2)
\quad,\quad
y_{\mathrm{tip}2} = y_{\mathrm{piv}} + L \sin(\phi + \theta_2)
$$
