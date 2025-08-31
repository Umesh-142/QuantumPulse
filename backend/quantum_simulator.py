# import numpy as np
# from typing import Dict, List, Any
# import json

# class QuantumSimulator:
#     def __init__(self):
#         self.rng = np.random.RandomState()
    
#     def set_seed(self, seed: int):
#         if seed is not None:
#             self.rng.seed(seed)
#             np.random.seed(seed)
    
#     def generate_rabi_data(self, omega: float, time_max: float, time_steps: int, 
#                           noise_rate: float, shots: int, seed: int = None) -> Dict[str, Any]:
#         """Generate Rabi oscillation synthetic data"""
#         self.set_seed(seed)
        
#         # Time array
#         time = np.linspace(0, time_max, time_steps)
        
#         # Theoretical Rabi oscillation: P(|1⟩) = sin²(Ωt/2)
#         theory_prob = np.sin(omega * time / 2) ** 2
        
#         # Add T2 decay envelope
#         decay_envelope = np.exp(-time / (time_max * 0.3))
#         theory_prob *= decay_envelope
        
#         # Add noise and sample
#         measurements = []
#         measured_prob = []
        
#         for i, prob in enumerate(theory_prob):
#             # Add Gaussian noise to probability
#             noisy_prob = np.clip(prob + self.rng.normal(0, noise_rate), 0, 1)
            
#             # Sample binomial for shot noise
#             ones_count = self.rng.binomial(shots, noisy_prob)
#             measurements.append({
#                 'time': float(time[i]),
#                 'theory_prob': float(prob),
#                 'measured_prob': float(ones_count / shots),
#                 'ones_count': int(ones_count),
#                 'zeros_count': int(shots - ones_count)
#             })
#             measured_prob.append(ones_count / shots)
        
#         # Calculate fit metrics
#         mse = np.mean((np.array(measured_prob) - theory_prob) ** 2)
        
#         return {
#             'experiment_type': 'rabi_oscillation',
#             'parameters': {
#                 'omega': omega,
#                 'time_max': time_max,
#                 'time_steps': time_steps,
#                 'noise_rate': noise_rate,
#                 'shots': shots,
#                 'seed': seed
#             },
#             'measurements': measurements,
#             'statistics': {
#                 'mse': float(mse),
#                 'max_prob': float(np.max(measured_prob)),
#                 'oscillation_period': float(2 * np.pi / omega)
#             },
#             'metadata': {
#                 'total_measurements': time_steps,
#                 'total_shots': shots * time_steps
#             }
#         }
    
#     def generate_decay_data(self, t1: float, t2: float, time_max: float, time_steps: int,
#                            noise_rate: float, shots: int, seed: int = None) -> Dict[str, Any]:
#         """Generate T1/T2 decay synthetic data"""
#         self.set_seed(seed)
        
#         time = np.linspace(0, time_max, time_steps)
        
#         # T1 decay (amplitude decay)
#         t1_decay = np.exp(-time / t1)
        
#         # T2 decay (coherence decay with oscillation)
#         t2_oscillation = t1_decay * np.cos(2 * np.pi * time / 2) * np.exp(-time / t2)
        
#         measurements_t1 = []
#         measurements_t2 = []
        
#         for i, t in enumerate(time):
#             # T1 measurements
#             prob_t1 = np.clip(t1_decay[i] + self.rng.normal(0, noise_rate), 0, 1)
#             ones_t1 = self.rng.binomial(shots, prob_t1)
            
#             measurements_t1.append({
#                 'time': float(t),
#                 'theory_signal': float(t1_decay[i]),
#                 'measured_signal': float(ones_t1 / shots),
#                 'ones_count': int(ones_t1),
#                 'zeros_count': int(shots - ones_t1)
#             })
            
#             # T2 measurements (coherence)
#             signal_t2 = (t2_oscillation[i] + 1) / 2  # Normalize to [0,1]
#             prob_t2 = np.clip(signal_t2 + self.rng.normal(0, noise_rate), 0, 1)
#             ones_t2 = self.rng.binomial(shots, prob_t2)
            
#             measurements_t2.append({
#                 'time': float(t),
#                 'theory_signal': float(signal_t2),
#                 'measured_signal': float(ones_t2 / shots),
#                 'ones_count': int(ones_t2),
#                 'zeros_count': int(shots - ones_t2)
#             })
        
#         return {
#             'experiment_type': 't1_t2_decay',
#             'parameters': {
#                 't1': t1,
#                 't2': t2,
#                 'time_max': time_max,
#                 'time_steps': time_steps,
#                 'noise_rate': noise_rate,
#                 'shots': shots,
#                 'seed': seed
#             },
#             'measurements': {
#                 't1_decay': measurements_t1,
#                 't2_coherence': measurements_t2
#             },
#             'statistics': {
#                 't1_fitted': float(t1 * (1 + self.rng.normal(0, 0.1))),
#                 't2_fitted': float(t2 * (1 + self.rng.normal(0, 0.1)))
#             },
#             'metadata': {
#                 'total_measurements': time_steps * 2,
#                 'total_shots': shots * time_steps * 2
#             }
#         }
    
#     def generate_bell_data(self, noise_rate: float, shots: int, theta: float = 0.0, 
#                           seed: int = None) -> Dict[str, Any]:
#         """Generate Bell state measurement synthetic data"""
#         self.set_seed(seed)
        
#         # Bell state measurement basis
#         bases = ['XX', 'XY', 'YX', 'YY']
#         measurements = {}
        
#         # Theoretical Bell state correlations
#         theory_correlations = {
#             'XX': np.cos(theta),
#             'XY': np.cos(theta + np.pi/2),
#             'YX': np.cos(theta - np.pi/2),
#             'YY': np.cos(theta + np.pi)
#         }
        
#         total_correlation = 0
        
#         for basis in bases:
#             # Theoretical correlation for this basis
#             theory_corr = theory_correlations[basis]
            
#             # Add noise to correlation
#             noisy_corr = theory_corr + self.rng.normal(0, noise_rate)
#             noisy_corr = np.clip(noisy_corr, -1, 1)
            
#             # Generate correlated measurements
#             prob_same = (1 + noisy_corr) / 2  # Convert correlation to probability
            
#             # Generate measurement outcomes
#             same_outcome_count = self.rng.binomial(shots, prob_same)
#             diff_outcome_count = shots - same_outcome_count
            
#             # Distribute between 00+11 and 01+10
#             prob_00 = prob_11 = same_outcome_count / (2 * shots)
#             prob_01 = prob_10 = diff_outcome_count / (2 * shots)
            
#             count_00 = self.rng.binomial(shots, prob_00)
#             count_11 = self.rng.binomial(shots, prob_11)
#             count_01 = self.rng.binomial(shots, prob_01)
#             count_10 = shots - count_00 - count_11 - count_01
            
#             measured_corr = (count_00 + count_11 - count_01 - count_10) / shots
            
#             measurements[basis] = {
#                 'count_00': int(count_00),
#                 'count_01': int(count_01),
#                 'count_10': int(count_10),
#                 'count_11': int(count_11),
#                 'theory_correlation': float(theory_corr),
#                 'measured_correlation': float(measured_corr)
#             }
            
#             total_correlation += abs(measured_corr)
        
#         # CHSH inequality parameter
#         chsh_value = abs(measurements['XX']['measured_correlation'] - measurements['XY']['measured_correlation']) + \
#                     abs(measurements['YX']['measured_correlation'] + measurements['YY']['measured_correlation'])
        
#         return {
#             'experiment_type': 'bell_state',
#             'parameters': {
#                 'noise_rate': noise_rate,
#                 'shots': shots,
#                 'theta': theta,
#                 'seed': seed
#             },
#             'measurements': measurements,
#             'statistics': {
#                 'chsh_value': float(chsh_value),
#                 'violation': chsh_value > 2.0,
#                 'total_correlation': float(total_correlation)
#             },
#             'metadata': {
#                 'total_measurements': len(bases),
#                 'total_shots': shots * len(bases)
#             }
#         }
import numpy as np
from typing import Dict, List, Any
import json

class QuantumSimulator:
    def __init__(self):
        self.rng = np.random.RandomState()
    
    def set_seed(self, seed: int):
        if seed is not None:
            self.rng.seed(seed)
            np.random.seed(seed)
    
    def generate_rabi_data(self, omega: float, time_max: float, time_steps: int, 
                          noise_rate: float, shots: int, seed: int = None) -> Dict[str, Any]:
        """Generate Rabi oscillation synthetic data"""
        self.set_seed(seed)
        
        # Time array
        time = np.linspace(0, time_max, time_steps)
        
        # Theoretical Rabi oscillation: P(|1⟩) = sin²(Ωt/2)
        theory_prob = np.sin(omega * time / 2) ** 2
        
        # Add T2 decay envelope
        decay_envelope = np.exp(-time / (time_max * 0.3))
        theory_prob *= decay_envelope
        
        # Add noise and sample
        measurements = []
        measured_prob = []
        
        for i, prob in enumerate(theory_prob):
            # Add Gaussian noise to probability
            noisy_prob = np.clip(prob + self.rng.normal(0, noise_rate), 0, 1)
            
            # Sample binomial for shot noise
            ones_count = self.rng.binomial(shots, noisy_prob)
            measurements.append({
                'time': float(time[i]),
                'theory_prob': float(prob),
                'measured_prob': float(ones_count / shots),
                'ones_count': int(ones_count),
                'zeros_count': int(shots - ones_count)
            })
            measured_prob.append(ones_count / shots)
        
        # Calculate fit metrics
        mse = np.mean((np.array(measured_prob) - theory_prob) ** 2)
        
        return {
            'experiment_type': 'rabi_oscillation',
            'parameters': {
                'omega': omega,
                'time_max': time_max,
                'time_steps': time_steps,
                'noise_rate': noise_rate,
                'shots': shots,
                'seed': seed
            },
            'measurements': measurements,
            'statistics': {
                'mse': float(mse),
                'max_prob': float(np.max(measured_prob)),
                'oscillation_period': float(2 * np.pi / omega)
            },
            'metadata': {
                'total_measurements': time_steps,
                'total_shots': shots * time_steps
            }
        }
    
    def generate_decay_data(self, t1: float, t2: float, time_max: float, time_steps: int,
                           noise_rate: float, shots: int, seed: int = None) -> Dict[str, Any]:
        """Generate T1/T2 decay synthetic data"""
        self.set_seed(seed)
        
        time = np.linspace(0, time_max, time_steps)
        
        # T1 decay (amplitude decay)
        t1_decay = np.exp(-time / t1)
        
        # T2 decay (coherence decay with oscillation)
        t2_oscillation = t1_decay * np.cos(2 * np.pi * time / 2) * np.exp(-time / t2)
        
        measurements_t1 = []
        measurements_t2 = []
        
        for i, t in enumerate(time):
            # T1 measurements
            prob_t1 = np.clip(t1_decay[i] + self.rng.normal(0, noise_rate), 0, 1)
            ones_t1 = self.rng.binomial(shots, prob_t1)
            
            measurements_t1.append({
                'time': float(t),
                'theory_signal': float(t1_decay[i]),
                'measured_signal': float(ones_t1 / shots),
                'ones_count': int(ones_t1),
                'zeros_count': int(shots - ones_t1)
            })
            
            # T2 measurements (coherence)
            signal_t2 = (t2_oscillation[i] + 1) / 2  # Normalize to [0,1]
            prob_t2 = np.clip(signal_t2 + self.rng.normal(0, noise_rate), 0, 1)
            ones_t2 = self.rng.binomial(shots, prob_t2)
            
            measurements_t2.append({
                'time': float(t),
                'theory_signal': float(signal_t2),
                'measured_signal': float(ones_t2 / shots),
                'ones_count': int(ones_t2),
                'zeros_count': int(shots - ones_t2)
            })
        
        return {
            'experiment_type': 't1_t2_decay',
            'parameters': {
                't1': t1,
                't2': t2,
                'time_max': time_max,
                'time_steps': time_steps,
                'noise_rate': noise_rate,
                'shots': shots,
                'seed': seed
            },
            'measurements': {
                't1_decay': measurements_t1,
                't2_coherence': measurements_t2
            },
            'statistics': {
                't1_fitted': float(t1 * (1 + self.rng.normal(0, 0.1))),
                't2_fitted': float(t2 * (1 + self.rng.normal(0, 0.1)))
            },
            'metadata': {
                'total_measurements': time_steps * 2,
                'total_shots': shots * time_steps * 2
            }
        }
    
    def generate_bell_data(self, noise_rate: float, shots: int, theta: float = 0.0, 
                          seed: int = None) -> Dict[str, Any]:
        """Generate Bell state measurement synthetic data"""
        self.set_seed(seed)
        
        # Bell state measurement basis
        bases = ['XX', 'XY', 'YX', 'YY']
        measurements = {}
        
        # Theoretical Bell state correlations
        theory_correlations = {
            'XX': np.cos(theta),
            'XY': np.cos(theta + np.pi/2),
            'YX': np.cos(theta - np.pi/2),
            'YY': np.cos(theta + np.pi)
        }
        
        total_correlation = 0
        
        for basis in bases:
            # Theoretical correlation for this basis
            theory_corr = theory_correlations[basis]
            
            # Add noise to correlation
            noisy_corr = theory_corr + self.rng.normal(0, noise_rate)
            noisy_corr = np.clip(noisy_corr, -1, 1)
            
            # Generate correlated measurements
            prob_same = (1 + noisy_corr) / 2  # Convert correlation to probability
            
            # Generate measurement outcomes
            same_outcome_count = self.rng.binomial(shots, prob_same)
            diff_outcome_count = shots - same_outcome_count
            
            # Distribute between 00+11 and 01+10
            prob_00 = prob_11 = same_outcome_count / (2 * shots)
            prob_01 = prob_10 = diff_outcome_count / (2 * shots)
            
            count_00 = self.rng.binomial(shots, prob_00)
            count_11 = self.rng.binomial(shots, prob_11)
            count_01 = self.rng.binomial(shots, prob_01)
            count_10 = shots - count_00 - count_11 - count_01
            
            measured_corr = (count_00 + count_11 - count_01 - count_10) / shots
            
            measurements[basis] = {
                'count_00': int(count_00),
                'count_01': int(count_01),
                'count_10': int(count_10),
                'count_11': int(count_11),
                'theory_correlation': float(theory_corr),
                'measured_correlation': float(measured_corr)
            }
            
            total_correlation += abs(measured_corr)
        
        # CHSH inequality parameter
        chsh_value = abs(measurements['XX']['measured_correlation'] - measurements['XY']['measured_correlation']) + \
                    abs(measurements['YX']['measured_correlation'] + measurements['YY']['measured_correlation'])
        
        return {
            'experiment_type': 'bell_state',
            'parameters': {
                'noise_rate': noise_rate,
                'shots': shots,
                'theta': theta,
                'seed': seed
            },
            'measurements': measurements,
            'statistics': {
                'chsh_value': float(chsh_value),
                'violation': chsh_value > 2.0,
                'total_correlation': float(total_correlation)
            },
            'metadata': {
                'total_measurements': len(bases),
                'total_shots': shots * len(bases)
            }
        }
