import numpy as np
import scipy.special as sp 


def f1(x):
    return 2*x**4-3*x**3+x-5

def f2(x):
    return 5*x*np.exp(-2*x)

def gauss_legendre(f,a,b,n):
    xi,w = sp.roots_legendre(n)
    x = 0.5*(b-a)*xi+0.5*(a+b)
    I=0.5*(b-a)*np.sum(w*f(x))
    return I

def main():
    a,b=-1,1
    n=5
    integral1=gauss_legendre(f1,a,b,n)
    integral2=gauss_legendre(f2,a,b,n)
    print(integral1)
    print(integral2)

main()