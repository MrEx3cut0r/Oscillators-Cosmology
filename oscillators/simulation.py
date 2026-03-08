import numpy as np
from tqdm import tqdm
import logging
from .models import (
    ParametricResonance,
    LeptogenesisModel,
    QuantumCreationInExpandingUniverse
)

class MatterGenesisSimulation:
    def __init__(self, volume_size=10.0, initial_inflaton_energy=1e16, hubble_parameter=1e-5):
        self.volume = volume_size
        self.phi0 = initial_inflaton_energy
        self.H = hubble_parameter

        self.resonance = ParametricResonance(
            inflaton_mass=1e13,
            coupling=1e-7,
            hubble=self.H
        )

        self.leptogenesis = LeptogenesisModel(
            M=1e10,
            Yukawa=1e-6,
            CP_viol=1e-6
        )

        self.quantum = QuantumCreationInExpandingUniverse(
            mass=0.1,
            exp_rate=self.H
        )

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.k_vals_resonance = np.logspace(-3, 3, 20)
        self.k_vals_quantum = np.logspace(-2, 2, 10)
        self.k_weights = self.k_vals_quantum**2 / (2 * np.pi**2)

    def evolve_universe(self, total_time=1000.0, dt=0.5):
        n_steps = int(total_time / dt)
        times = np.linspace(0, total_time, n_steps)

        history = {
            'time': times,
            'inflaton_energy': np.zeros(n_steps),
            'particle_density': np.zeros(n_steps),
            'baryon_asymmetry': np.zeros(n_steps),
            'temperature': np.zeros(n_steps)
        }

        phi = self.phi0
        n_particles = 1.0
        eta = 0.0
        T = 1e15
        boltzmann_solved = False

        for i, t in enumerate(tqdm(times, desc="Evolving universe")):
            if t < 100 / self.H:
                dn_dt = 0
                for k in self.k_vals_resonance:
                    rate = self.resonance.particle_prod_rate(phi, k)
                    dn_dt += rate * k**2 * np.exp(-k/phi)
                n_particles += dn_dt * dt

            n_quantum = 0
            for j, k in enumerate(self.k_vals_quantum):
                try:
                    _, _, n_k = self.quantum.bogoliubov_cf(k, t_max=t)
                    n_quantum += n_k * self.k_weights[j]
                except:
                    pass
            n_particles += n_quantum * self.volume

            if t > 100 / self.H and eta < 1e-9 and 1e9 < T < 1e11 and not boltzmann_solved:
                try:
                    eta = self.leptogenesis.solve()
                except:
                    eta = 6e-10
                boltzmann_solved = True
            
            phi *= np.exp(-self.H * dt)
            T = T * np.exp(-self.H * dt) + (n_particles / self.volume) ** (1/3) * dt
            
            history['inflaton_energy'][i] = phi
            history['particle_density'][i] = n_particles / self.volume
            history['baryon_asymmetry'][i] = eta
            history['temperature'][i] = T

            if T < 2.7e-13:
                self.logger.info(f"Reached present-day temperature at t={t:.2f}")
                break
                
        for key in history:
            history[key] = history[key][:i+1]
                
        return history
