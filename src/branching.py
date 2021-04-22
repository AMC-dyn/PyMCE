import numpy as np



def branching_ratios(B):
    ntraj = B.ntraj
    nstates = B.nstates

    c_l=np.zeros(ntraj)
    for i in range(ntraj):
        c_l[i] = B.Traj[i].amp

    cse = np.zeros((nstates, ntraj))

    for i in range(ntraj):
        cse[:, i] = B.Traj[i].stateAmp

    s_l = B.get_calc_set_overlaps()

    ratio = np.zeros(nstates)
    for i in range(nstates):
        ratio[i] = np.real(np.dot(c_l * cse[i, :], np.matmul(s_l, c_l * cse[i, :])))

    return ratio


