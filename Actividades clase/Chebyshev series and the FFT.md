# Chebyshev Series and la FFT

## Introducción

Las **series de Chebyshev** y la **Transformada Rápida de Fourier** (FFT) se combinan en los llamados **métodos espectrales** para resolver ecuaciones diferenciales de forma muy eficiente.  
- Una serie de Chebyshev aproxima una función \(f(x)\) en \([-1,1]\) como  
  \[
    f(x)\approx\sum_{n=0}^N a_n\,T_n(x),
  \]  
  donde \(T_n(x)=\cos\bigl(n\arccos(x)\bigr)\) es el polinomio de Chebyshev de grado \(n\).  
- La FFT permite calcular los coeficientes \(\{a_n\}\) en \(\mathcal O(N\log N)\) en lugar de \(\mathcal O(N^2)\).

---

## 1. Series de Chebyshev

1. **Nodos de Chebyshev**:  
   \[
     x_j = \cos\Bigl(\tfrac{\pi j}{N}\Bigr),\quad j=0,\dots,N.
   \]
2. **Interpolación**:  
   Se muestrea \(f(x_j)\) y se obtiene un polinomio de grado \(N\) que coincide con \(f\) en los \(N+1\) nodos.
3. **Coeficientes**:  
   \[
     a_n = \frac{2}{N}\sum_{j=0}^N{}^{\prime\prime} f(x_j)\cos\!\Bigl(\tfrac{\pi n j}{N}\Bigr),
   \]  
   donde las comillas dobles indican que el primer y último término van con peso \(1/2\).

---

## 2. FFT para la transformada de Chebyshev

- La suma anterior es equivalente a una **Transformada Discreta de Coseno** (DCT) de tipo I, que se implementa con un par de llamadas a la FFT estándar.  
- Ventaja: reduce la complejidad de \(\mathcal O(N^2)\) a \(\mathcal O(N\log N)\).

---

## 3. Métodos espectrales para EDOs

Para resolver una ecuación diferencial (por ejemplo,
\[
  y''(x) - y(x) = g(x),\quad x\in[-1,1],\quad y(-1)=y(1)=0,
\]
) se sigue el siguiente esquema:

1. **Interpolación** de \(y\) en nodos de Chebyshev:  
   \(y(x)\approx\sum_{n=0}^N a_n\,T_n(x)\).
2. **Matrices de diferenciación**:  
   Construir la matriz \(D\in\mathbb R^{(N+1)\times(N+1)}\) tal que  
   \[
     (D\mathbf y)_j \approx y'(x_j),\quad (D^2\mathbf y)_j \approx y''(x_j).
   \]
3. **Sistema lineal**:  
   En los **nodos interiores** \(j=1,\dots,N-1\),
   \[
     (D^2\mathbf y)_j - \mathbf y_j = g(x_j).
   \]
4. **Condiciones de frontera**:  
   Se imponen \(y(x_0)=y(x_N)=0\) eliminando las dos primeras ecuaciones y ajustando el sistema.
5. **Resolución** de un sistema \((N-1)\times(N-1)\) en coeficientes \(\mathbf y\).

---

## 4. Ejemplo resuelto

**Problema**:  
\[
  y''(x) - y(x) = \sin(\pi x),\quad y(-1)=y(1)=0,\quad x\in[-1,1].
\]

### 4.1 Construcción de nodos y matriz de diferenciación

```python
import numpy as np

def cheb(N):
    """
    Devuelve la matriz de diferenciación D y los nodos x de Chebyshev.
    """
    if N == 0:
        return np.array([[0]]), np.array([1.])
    # Nodos
    x = np.cos(np.pi * np.arange(N+1) / N)
    # Pesos c_i
    c = np.ones(N+1)
    c[0] = 2
    c[-1] = 2
    c = c * ((-1)**np.arange(N+1))
    # Matriz de diferenciación
    X = np.tile(x, (N+1, 1))
    dX = X - X.T
    D = (c[:,None] / c[None,:]) / (dX + np.eye(N+1))
    D = D - np.diag(np.sum(D, axis=1))
    return D, x

# Ejemplo con N=30
N = 30
D, x = cheb(N)
D2 = D.dot(D)  # Segunda derivada

