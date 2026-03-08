import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from .simulation import MatterGenesisSimulation
from .visualization import plot_genesis_results
from .calibration import calibrate_planck

def main():
    parser = argparse.ArgumentParser(description='Oscillators-Cosmology: modeling of matteria birth')
    
    parser.add_argument('--quick', action='store_true', help='fast demonstration')
    parser.add_argument('--time', type=float, default=1000.0, help='time of demonstration')
    parser.add_argument('--output', type=str, default='./report', help='directory for results')
    parser.add_argument('--save-report', action='store_true', help='save report')
    parser.add_argument('--calibrate', action='store_true', help='calibrate data for Planck')
    
    args = parser.parse_args()
    
    if args.calibrate:
        print("calibration...")
        params = calibrate_planck()
        print(f"optimal parameters: {params}")
        return

    sim = MatterGenesisSimulation(
        volume_size=10.0,
        initial_inflaton_energy=1e16,
        hubble_parameter=1e-5
    )
    
    print(f"starting simulation at time t={args.time}...")
    history = sim.evolve_universe(total_time=args.time)
    
    fig = plot_genesis_results(history)
    
    if args.save_report:
        import os
        os.makedirs(args.output, exist_ok=True)
        fig.savefig(f"{args.output}/genesis_results.png")
        np.save(f"{args.output}/history.npy", history)
        print(f"results saved in {args.output}")
    else:
        plt.show()

if __name__ == "__main__":
    main()
