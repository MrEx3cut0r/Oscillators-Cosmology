import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp
from scipy.special import jv

class ParametricResonance:
    def __init__(self, inflaton_mass=1e13, coupling=1e-7, hubble=1e-5):
        self.m = inflaton_mass
        self.g = coupling
        self.H = hubble

    def mathieu_parameters(self, phi_amplitude, k):
        q = (self.g**2 * phi_amplitude**2) / (4 * self.m**2)
        a = (k**2 / self.m**2) + 2*q
        return a, q

    def floquet_exponent(self, a, q):
        M = self.monodromy_matrix(a, q)
        trace = np.trace(M)
        if np.abs(trace) <= 2:
            return 0.0
        else:
            mu = np.arccosh(np.abs(trace)/2)
            return mu

    def stability_chart(self, k_range=(0,5), q_range=(0,5), resolution=100):
        k_vals = np.linspace(k_range[0], k_range[1], resolution)
        q_vals = np.linspace(q_range[0], q_range[1], resolution)
        floquet = np.zeros((resolution, resolution))

        for i, q in enumerate(q_vals):
            for j, k in enumerate(k_vals):
                a = k**2 + 2*q
                M = self.monodromy_matrix(a, q)
                trace = np.trace(M)
                if np.abs(trace) <= 2:
                    floquet[i, j] = 0.0
                else:
                    floquet[i, j] = np.arccosh(np.abs(trace)/2)
        return k_vals, q_vals, floquet

    def monodromy_matrix(self, a, q, n_cycles=50):
        def mathieu_system(t, y):
            return [y[1], -(a - 2*q*np.cos(2*t)) * y[0]]

        sol1 = solve_ivp(mathieu_system, [0, np.pi], [1, 0], 
                         method='DOP853', rtol=1e-10, atol=1e-12)
        sol2 = solve_ivp(mathieu_system, [0, np.pi], [0, 1],
                         method='DOP853', rtol=1e-10, atol=1e-12)
        
        M = np.array([
            [sol1.y[0][-1], sol2.y[0][-1]],
            [sol1.y[1][-1], sol2.y[1][-1]]
        ])
        return M

    def particle_prod_rate(self, phi_amplitude, k):
        a, q = self.mathieu_parameters(phi_amplitude, k)
        mu = self.floquet_exponent(a, q)
        if mu > 0:
            return 2 * mu * self.m
        return 0.0

class LeptogenesisModel:
    def __init__(self, M=1e10, Yukawa=1e-6, CP_viol=1e-6):
        self.M = M
        self.h = Yukawa
        self.epsilon = CP_viol

    def decay_rate(self):
        return (self.h**2 * self.M) / (8 * np.pi)

    def scattering_rate(self):
        return self.decay_rate() * 0.1

    def hubble_param(self, z):
        T = self.M / z
        return 1.66 * np.sqrt(100) * T**2 / 1.22e19 

    def Y_N_eq(self, z):
        if z < 1:
            return 0.4  
        else:
            return 0.4 * np.exp(-z) / z**1.5

    def boltzmann_eq(self, z, Y):
        Y_N, Y_L = Y
        gamma_D = self.decay_rate()
        gamma_S = self.scattering_rate()

        K = gamma_D / (2 * self.hubble_param(z))
        dY_N_dz = -K * z * (Y_N / self.Y_N_eq(z) - 1)
        dY_L_dz = -self.epsilon * dY_N_dz - K * z * Y_L / (2 * self.Y_N_eq(z))
        return [dY_N_dz, dY_L_dz]

    def solve(self, z_range=(0.1, 100)):
        z_span = z_range
        Y0 = [self.Y_N_eq(z_range[0]), 0]
        
        sol = solve_ivp(
            self.boltzmann_eq, 
            z_span,
            Y0,
            method="Radau",
            dense_output=True,
            rtol=1e-6,
            atol=1e-8
        )
        
        Y_L_final = sol.y[1][-1]
        Y_B = (28/79) * Y_L_final

        eta = Y_B / 7.04
        return eta

class QuantumCreationInExpandingUniverse:
    def __init__(self, mass=0.1, exp_rate=0.01):
        self.m = mass
        self.H = exp_rate

    def scale_factor(self, t):
        return np.exp(self.H * t)

    def mode_equation(self, t, y, k):
        a = self.scale_factor(t)
        omega2 = k**2 + self.m**2 * a**2
        return [y[1], -omega2 * y[0]]

    def bogoliubov_cf(self, k, t_max=100):
        t0 = -t_max
        a0 = self.scale_factor(t0)
        omega0 = np.sqrt(k**2 + self.m**2 * a0**2)
        chi0 = 1.0 / np.sqrt(2 * omega0)
        chi_dot0 = -1j * omega0 * chi0

        sol = solve_ivp(
            lambda t, y: self.mode_equation(t, y, k),
            [t0, 0],
            [chi0.real, chi0.imag, chi_dot0.real, chi_dot0.imag],
            method='DOP853',
            rtol=1e-8,
            atol=1e-10
        )

        chi_f = sol.y[0][-1] + 1j * sol.y[1][-1]
        chi_dot_f = sol.y[2][-1] + 1j * sol.y[3][-1]
        
        omega_f = np.sqrt(k**2 + self.m**2)

        alpha = (omega_f * chi_f + 1j * chi_dot_f) / np.sqrt(2 * omega_f)
        beta = (omega_f * chi_f - 1j * chi_dot_f) / np.sqrt(2 * omega_f)
        
        n_k = np.abs(beta)**2
        return alpha, beta, n_k
