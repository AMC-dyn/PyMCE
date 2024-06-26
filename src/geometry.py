from src.constants import physconst
import numpy as np

class singlepart(): #Madeup for a single particle moving in a model potential
    def __init__(self):

        ''' Use the data for H2 system'''

        ph=physconst()
        self.natoms=1
        self.atnum=1
        masses_dict=get_atomic_masses()
        self.massH=mass2au(masses_dict['H'])
        self.mass=self.massH/2
        self.K=0.35
        self.rkinit=np.zeros(3)
        self.ndf=3



class initgeom():
    def __init__(self,filegeom):
        ph = physconst()  # Call to a dict of physical constants

        self.natoms, self.atnames, self.rk, self.comments = process_geometry(filegeom)  # Process xyz file and output required parameters

        massesdict = get_atomic_masses()  # Mass of each atom
        mass = np.zeros((self.natoms), dtype=np.double)
        for i in range(0, self.natoms):
            mass[i] = massesdict[self.atnames[i]]*np.double(1822.89)
        self.masses = np.double(mass)
        self.rkangs = np.double(self.rk)  # List of initial atomic xyz coords, 3*N dim
       # self.rk = CofMass(self.rk, self.masses, self.natoms)
        # Set the geometry in the center of mass
        count = 0

        rkbohr_mass = np.zeros((self.natoms * 3))  # Convert the coordinates to massweighted au
        masses_rk = np.zeros((self.natoms * 3), dtype=np.double)
        for i in range(0, self.natoms):
            for j in range(0, 3):
                rkbohr_mass[count] = self.rk[count] / ph.bohr * np.sqrt(self.masses[i])
                masses_rk[count] = self.masses[i]
                count = count + 1

        self._rkinit = self.rk/ph.bohr

        self.ndf = self.natoms * 3
        self.massrk = masses_rk

    @property
    def rkinit(self):
        return self._rkinit

    @rkinit.setter
    def rkinit(self, value):
        self._rkinit = value


def process_geometry(geom_file='geometry.xyz'):
    """
    This function takes a standard xyz file as input where
    first line is number of atoms
    second line contains comment
    the rest of the lines contain 3D coordinates
    Returns a tuple of:
    1. Number of atoms
    2. Atom names
    3. Coordinates
    4. Comment
    """

    with open(geom_file, 'r') as open_file:

        atom_names = []
        atoms = []
        n = 0
        for i, line in enumerate(open_file):
            if i == 0:
                assert len(line.split()) == 1
                n_atoms = int(line)

            elif i == 1:
                comment = line
            else:
                line_list = line.split()
                if len(line_list) > 0:
                    assert len(line_list) == 4, 'wrong xyz file format'
                    print(line_list)
                    coord = [float(num.replace('d', 'e')) for num in line_list[1:4]]
                    atoms.append(coord)
                    n = n + 1
                    atom_names.append(line_list[0])
        idf = 0

        atoms = np.transpose(np.asarray(atoms))

        coords = np.zeros(n_atoms * 3)
        for l in range(n_atoms):
            for j in range(3):
                coords[idf] = atoms[j, l]
                idf += 1
    # converting coordinates into 1D numpy array
    array = np.asarray(coords)

    return n_atoms, atom_names, array, comment


def get_atomic_masses():
    masses_dict = {'H': 1.00, 'HE': 4.003, 'LI': 6.941, 'BE': 9.012, \
                   'B': 10.811, 'C': 12.00000000, 'N': 14.007, 'O': 15.999, \
                   'F': 18.998, 'NE': 20.180, 'NA': 22.990, 'MG': 24.305, \
                   'AL': 26.982, 'SI': 28.086, 'P': 30.974, 'S': 32.066, \
                   'CL': 35.453, 'AR': 39.948, 'K': 39.098, 'CA': 40.078, \
                   'SC': 44.956, 'TI': 47.867, 'V': 50.942, 'CR': 51.996, \
                   'MN': 54.938, 'FE': 55.845, 'CO': 58.933, 'NI': 58.693, \
                   'CU': 63.546, 'ZN': 65.38, 'GA': 69.723, 'GE': 72.631, \
                   'AS': 74.922, 'SE': 78.971, 'BR': 79.904, 'KR': 84.798, \
                   'RB': 84.468, 'SR': 87.62, 'Y': 88.906, 'ZR': 91.224, \
                   'NB': 92.906, 'MO': 95.95, 'TC': 98.907, 'RU': 101.07, \
                   'RH': 102.906, 'PD': 106.42, 'AG': 107.868, 'CD': 112.414, \
                   'IN': 114.818, 'SN': 118.711, 'SB': 121.760, 'TE': 126.7, \
                   'I': 126.904, 'XE': 131.294, 'CS': 132.905, 'BA': 137.328, \
                   'LA': 138.905, 'CE': 140.116, 'PR': 140.908, 'ND': 144.243, \
                   'PM': 144.913, 'SM': 150.36, 'EU': 151.964, 'GD': 157.25, \
                   'TB': 158.925, 'DY': 162.500, 'HO': 164.930, 'ER': 167.259, \
                   'TM': 168.934, 'YB': 173.055, 'LU': 174.967, 'HF': 178.49, \
                   'TA': 180.948, 'W': 183.84, 'RE': 186.207, 'OS': 190.23, \
                   'IR': 192.217, 'PT': 195.085, 'AU': 196.967, 'HG': 200.592, \
                   'TL': 204.383, 'PB': 207.2, 'BI': 208.980, 'PO': 208.982, \
                   'AT': 209.987, 'RN': 222.081, 'FR': 223.020, 'RA': 226.025, \
                   'AC': 227.028, 'TH': 232.038, 'PA': 231.036, 'U': 238.029, \
                   'NP': 237, 'PU': 244, 'AM': 243, 'CM': 247, 'BK': 247, \
                   'CT': 251, 'ES': 252, 'FM': 257, 'MD': 258, 'NO': 259, \
                   'LR': 262, 'RF': 261, 'DB': 262, 'SG': 266, 'BH': 264, \
                   'HS': 269, 'MT': 268, 'DS': 271, 'RG': 272, 'CN': 285, \
                   'NH': 284, 'FL': 289, 'MC': 288, 'LV': 292, 'TS': 294, \
                   'OG': 294}
    return masses_dict


def mass2au(partmass):
    """This function converts the atomic masses in atomic units"""
    ph = physconst()
    aum = partmass * ph.amu
    return aum

def CofMass(rk, mass, natom):
    totmass = np.sum(mass)
    center = [0., 0., 0.]
    count = 0
    for i in range(0, natom):
        fac = mass[i] / totmass
        for j in range(0, 3):
            center[j] = center[j] + rk[count] * fac
            count += 1

    count = 0
    for i in range(natom):
        for j in range(3):
            rk[count] = rk[count] - center[j]
            count += 1

    return rk
