import numpy as np

rho = 1000. # desired density at P0, T0
P0 = 1.E7  # initial pressure [Pa]
T0 = 300.  # initial temp [K]
Kf = 2.e9 #bulk modulus of fluid (inverse of compressibility) [Pa]
alpha_f = .0002 #fluid thermal expansion coefficient

rho0 = rho/np.exp((P0/Kf)-alpha_f*T0)

print 'for T0: ', str(T0), 'and P0: ', str(P0), 'we want rho = ', str(rho)
print 'rho0 is: ', str(rho0)
