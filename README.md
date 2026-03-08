# Oscillators-Cosmology
This package simulates the birth of matter in the early universe through three fundamental mechanisms:

    Parametric Resonance - Preheating after inflation (Mathieu equation)

    Leptogenesis - Generation of baryon asymmetry via CP-violating decays

    Quantum Creation - Particle production in expanding universe (Bogoliubov formalism)

The model reproduces the observed baryon asymmetry η ≈ 6×10⁻¹⁰ and the present-day composition of the universe (68% dark energy, 27% dark matter, 5% baryons).

## Installation
```
# Basic installation
pip install oscillators-cosmology

# With plotting support
pip install "oscillators-cosmology[plot]"

# For development
git clone https://github.com/MrEx3cut0r/Oscillators-Cosmology.git
cd Oscillators-Cosmology
pip install -e ".[dev]"
```

## Quick start
### Command Line Interface
```
# Run simulation (1000 time units)
oscillators-sim --time 1000

# Quick demonstration
oscillators-sim --quick

# Save results to file
oscillators-sim --save-report --output ./my_results

# Calibrate parameters to Planck data (may take 20-40 minutes)
oscillators-calibrate
```

## Python API
```
from oscillators import MatterGenesisSimulation, plot_genesis_results

# Create simulation
sim = MatterGenesisSimulation(
    volume_size=10.0,
    initial_inflaton_energy=1e16,
    hubble_parameter=1e-5
)

# Run evolution
history = sim.evolve_universe(total_time=1000.0)

# Plot results
fig = plot_genesis_results(history)

# Check baryon asymmetry
print(f"Final baryon asymmetry: {history['baryon_asymmetry'][-1]:.2e}")
print(f"Present temperature: {history['temperature'][-1]:.2e} GeV")
```

## Physics model 
### Parametric Resonance
```
from oscillators import ParametricResonance

res = ParametricResonance(inflaton_mass=1e13, coupling=1e-7)
k_vals, q_vals, floquet = res.stability_chart()
# Plot instability bands of Mathieu equation
```
### Leptogenesis
```
from oscillators import LeptogenesisModel

lepto = LeptogenesisModel(M=1e10, Yukawa=1e-6, CP_viol=1e-6)
eta = lepto.solve()  # baryon asymmetry
print(f"η = {eta:.2e}")
```
### Quantum creation
```
from oscillators import LeptogenesisModel

lepto = LeptogenesisModel(M=1e10, Yukawa=1e-6, CP_viol=1e-6)
eta = lepto.solve()  # baryon asymmetry
print(f"η = {eta:.2e}")
```
# Reference

Kofman, Linde, Starobinsky (1997) - "Towards the theory of reheating after inflation"

Fukugita, Yanagida (1986) - "Baryogenesis without grand unification"

Parker (1968) - "Particle creation in expanding universes"

Planck Collaboration (2020) - "Planck 2018 results. VI. Cosmological parameters"

# License

MIT License - see LICENSE file for details

# Author

Gumar Arutunyan

	Email: legendary.killtell@gmail.com

	GitHub: @MrEx3cut0r

If you use this code in your research, please cite:
```
@software{arutunyan2024oscillators,
  author = {Arutunyan, Gumar},
  title = {Oscillators-Cosmology: Matter Genesis Simulation},
  year = {2026},
  url = {https://github.com/MrEx3cut0r/Oscillators-Cosmology}
}
```
