import matplotlib.pyplot as plt
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D

def plot_stability_chart(k_vals, q_vals, floquet):
    fig, ax = plt.subplots(figsize=(10,8))
    im = ax.pcolormesh(k_vals, q_vals, floquet, shading='auto', cmap='RdBu')
    ax.set_xlabel('k / m (wave number)')
    ax.set_xlabel('q (amplitude of motion)')
    ax.set_title('parametric resonance stability map')
    plt.colorbar(im, label="floquet index")
    plt.tight_layout()
    return fig

def plot_genesis_results(history):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0,0].semilogy(history['time'], history['inflaton_energy'])
    axes[0,0].set_xlabel('time')
    axes[0,0].set_ylabel('Energy of inflaton')
    axes[0,0].set_title('inflaton decay')
    axes[0,0].grid(True)
    
    axes[0,1].loglog(history['time'], history['particle_density'])
    axes[0,1].set_xlabel('time')
    axes[0,1].set_ylabel('density of particles')
    axes[0,1].set_title('matteria birth')
    axes[0,1].grid(True)
    
    axes[1,0].semilogx(history['time'], history['baryon_asymmetry'])
    axes[1,0].axhline(y=6.1e-10, color='r', linestyle='--', label='Observable')
    axes[1,0].set_xlabel('time')
    axes[1,0].set_ylabel('η = n_b/n_γ')
    axes[1,0].set_title('evolution of barrion symmetry')
    axes[1,0].legend()
    axes[1,0].grid(True)
    
    axes[1,1].loglog(history['time'], history['temperature'])
    axes[1,1].set_xlabel('time')
    axes[1,1].set_ylabel('temperature')
    axes[1,1].set_title('Universe cooling')
    axes[1,1].grid(True)
    
    plt.tight_layout()
    return fig
