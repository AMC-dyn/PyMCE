from input import initgeom
from input import initdyn
from initialize_traj import trajectory
from src import abinitio
from src.constants import physconst
from src.propagators import velocityverlet
import Wigner_dist
import numpy as np
import Traj
import Constants
import molpro_call_read
import os
import time
import integrator
import derivatives
from matplotlib import pyplot as plt

'''AIMCE propagation'''

''' First, common variables are initialized using the class Traj, based on the dynamics and geometry inputs'''
'''q,p initial values, taken from the wigner dist and d,s,a'''

'''Remove previous files if needed'''
os.system('rm molpro.pun')
os.system('rm molpro_traj*')

''' call initial geometry and dynamic parameters along with pyhisical constants'''
dyn = initdyn()
geo = initgeom()
ph = physconst()

'''First initialize and populate one trajectory'''


qin, pin = Wigner_dist.WignerSampling()

# As I am doing everything mass-weighted, also applied to the widths

dt = dyn.dt
tr = Traj.traj()

# tr.n = 1
tr.iprop = 0

tr.q = qin
tr.p = pin
tr.d = np.zeros(dyn.nstates, dtype=np.cdouble)
tr.d[dyn.inipes - 1] = np.cdouble(1)
tr.s = np.zeros(dyn.nstates)
tr.a = tr.d * np.exp(1j * tr.s)

with open('initialqp.dat', 'r') as f:
    f.readline()
    for i in range(geo.ndf):
        N, M = f.readline().strip().split()
        tr.q[i] = np.double(float(N.replace('D', 'E')))
        tr.p[i] = np.double(float(M.replace('D', 'E')))
#     f.readline()
#     f.readline()
#     idf=0
#     for i in range(geo.natoms):
#         for j in range(3):
#             N = f.readline().strip().split()
#             geo.rkinit[idf] = np.double(float(N[0].replace('D', 'E')))
#             idf+=1
# molpro_call_read.create_input(tr.n, tr.iprop, tr.q)
# if not os.path.isfile('scratch_files/'):
#     os.system('mkdir scratch_files')
# os.system('E:/Molpro/bin/molpro.exe -d scratch_files/ -s molpro_traj_1_0.inp')

time_to_wait = 1000
T=trajectory()
T.setmomentum_traj(tr.p)
T.setposition_traj(tr.q)
pes, grads, nacs = molpro_call_read.inp_out(i, 0, tr.q, geo)

der = np.zeros((geo.ndf, T.nstates, T.nstates))
    for i in range(T.nstates):
        der[:, i, i] = grads[:, i]
        for j in range(T.nstates):
            if i!=j:
                der[:, i, j] = nacs[:, i, j]




tr.d = np.zeros(dyn.nstates, dtype=np.cdouble)
tr.d[dyn.inipes - 1] = np.cdouble(1)
tr.s = np.zeros(dyn.nstates)
tr.a = tr.d * np.exp(1j * tr.s)

T.setamplitudes_traj(tr.a)

amp = np.zeros((1500, dyn.nstates), dtype=complex)
t_sim = 0.0
ekin_tr=0.0
# r = derivatives.der(tr.q,tr.p,tr.s,tr.d,tr.epot,tr.grad,tr.nac)
for i in range(1500):
    t_sim = t_sim + 0.1
    # pes, grads, nacs = molpro_call_read.inp_out(i, 0, tr.q, geo)
    # tr.nac = nacs
    # tr.grad = grads
    # tr.epot = pes
    #
    #
    # ampli, dnorm, tr.q, tr.p, tr.s, tr.d, ekin_tr = integrator.rk_method_4(tr.q, tr.p, tr.s, tr.d, tr.epot, tr.grad,
    #                                                                        tr.nac,
    #
    #
    #                                                                        tr.time, tr._dt, ekin_tr, i, geo)



    print('step ', i)
    print('norm', dnorm)
    print('pop s0: ', np.abs(tr.d[0] * np.conj(tr.d[0])) / dnorm)
    print('pop s1: ', np.abs(tr.d[1] * np.conj(tr.d[1])) / dnorm)

    # plt.scatter(t_sim, np.double(toten), c='blue')
    # plt.scatter(t_sim, np.abs(tr.d[0] * np.conj(tr.d[0]) / dnorm), c='blue')
    # plt.scatter(t_sim, np.abs(tr.d[1] * np.conj(tr.d[1]) / dnorm), c='red')
    # plt.pause(0.01)

plt.show()
