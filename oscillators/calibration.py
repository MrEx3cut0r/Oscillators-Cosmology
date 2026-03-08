import numpy as np
from scipy.optimize import minimize

from .simulation import MatterGenesisSimulation

def calibrate_planck():
    def chi_squared(params):
        m_inf, g_coup, M_nu, cp_viol = params
        sim = MatterGenesisSimulation(
            volume_size=10.0,
            initial_inflaton_energy=1e16,
            hubble_parameter=1e-5
        )
        history = sim.evolve_universe(total_time=500.0)
        eta_sim = history['baryon_asymmetry'][-1]

        chi2 = ((eta_sim - 6.1e-10) / 1e-11)**2
        return chi2
    x0 = [1e13, 1e-7, 1e10, 1e-6]
    result = minimize(chi_squared, x0, method='Nelder-Mead')
    return result.x
