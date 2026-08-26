import numpy as np
import matplotlib.pyplot as plt

R = 10000
L = 1e-1
tau = L/R
F = 5000
period = (1.0 / F)
def pwm(t, frequency=F, duty=0.5, V=3.3):
    period = (1.0 / frequency)
    return (V if ((t % period) < (duty * period)) else 0.0)

def derriv (x,y):
    return (1/tau)*(x-y)


def integral(x, t_last, n=200000, y0=0.0):
     t = np.linspace(0.0, t_last, n)
     dt = (t[1] - t[0])
     y = np.empty(n)
     xs = np.empty(n)
     y[0] = y0
     xs[0] = x(t[0])
     for k in range(1, n):
         xs[k] = x(t[k])
         y[k] = y[k - 1] + (derriv(xs[k], y[k - 1]) * dt)
     return t, y, xs

t, y, xs = integral(pwm, (2*period))

def rk4(x, t_last, n=20000, y0=0.0):
    t = np.linspace(0.0, t_last, n)
    dt = t[1] - t[0]
    y =  np.empty(n)
    y = np.empty(n)
    xs = np.empty(n)
    y[0] = y0
    xs[0] = x(t[0])
    for k in range(1, n):
        tk, yk = t[k-1], y[k-1]
        k1 = derriv(x(tk),        yk)
        k2 = derriv(x(tk + dt/2), yk + dt*k1/2)
        k3 = derriv(x(tk + dt/2), yk + dt*k2/2)
        k4 = derriv(x(tk + dt),   yk + dt*k3)
        y[k] = yk + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
        xs[k] = x(t[k])
    return t, y, xs
    
def trapez(x, t_last, n=20000, y0=0.0):
    t = np.linspace(0.0, t_last, n)
    dt = (t[1] - t[0])
    y = np.empty(n)
    xs = np.empty(n)
    y[0] = y0
    xs[0] = x(t[0])
    for k in range(1, n):
        xs[k] = x(t[k])
        y[k] = (((y[k - 1] * (1 - ((dt / tau) / 2))) + ((dt / tau) * xs[k]))
                / (1 + ((dt / tau) / 2)))
    return t, y, xs

t, y, xs = integral(pwm, (2*period))
I = y/R
Vl = (xs - y)
plt.ion()
for k in range(0, len(t), 200):
    plt.clf()
    plt.plot(t[:k + 1], (I[:k + 1] * 1e6), color="tab:blue")
    plt.xlabel("t (s)")
    plt.ylabel("I (uA)", color="tab:blue")
    plt.grid(True)
    plt.twinx()
    plt.plot(t[:k + 1], Vl[:k + 1], color="tab:red")
    plt.ylabel("Vl (V)", color="tab:red")
    plt.pause(0.001)
plt.ioff()
plt.show()
