import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definisi universe variabel fuzzy
deadline = ctrl.Antecedent(np.arange(0, 31, 1), 'deadline')  # 0 sampai 30 hari tersisa
kesulitan = ctrl.Antecedent(np.arange(0, 11, 1), 'kesulitan')  # 0-10
urgensi = ctrl.Antecedent(np.arange(0, 11, 1), 'urgensi')      # 0-10
prioritas = ctrl.Consequent(np.arange(0, 11, 1), 'prioritas')  # 0-10

# Fungsi keanggotaan untuk deadline (hari tersisa)
deadline['dekat'] = fuzz.trimf(deadline.universe, [0, 0, 2])
deadline['sedang'] = fuzz.trimf(deadline.universe, [2, 7, 12])
deadline['jauh'] = fuzz.trimf(deadline.universe, [10, 30, 30])

# Fungsi keanggotaan untuk kesulitan
kesulitan['mudah'] = fuzz.trimf(kesulitan.universe, [0, 0, 5])
kesulitan['sedang'] = fuzz.trimf(kesulitan.universe, [2, 5, 8])
kesulitan['sulit'] = fuzz.trimf(kesulitan.universe, [5, 10, 10])

# Fungsi keanggotaan untuk urgensi
urgensi['rendah'] = fuzz.trimf(urgensi.universe, [0, 0, 5])
urgensi['sedang'] = fuzz.trimf(urgensi.universe, [2, 5, 8])
urgensi['tinggi'] = fuzz.trimf(urgensi.universe, [5, 10, 10])

# Fungsi keanggotaan untuk prioritas
prioritas['rendah'] = fuzz.trimf(prioritas.universe, [0, 0, 3])
prioritas['sedang'] = fuzz.trimf(prioritas.universe, [3, 5, 7])
prioritas['tinggi'] = fuzz.trimf(prioritas.universe, [7, 10, 10])

# Aturan fuzzy (bisa disesuaikan lagi)
rule1 = ctrl.Rule(deadline['dekat'] & urgensi['tinggi'], prioritas['tinggi'])
rule2 = ctrl.Rule(deadline['dekat'] & kesulitan['mudah'], prioritas['tinggi'])
rule3 = ctrl.Rule(deadline['sedang'] & urgensi['tinggi'], prioritas['tinggi'])
rule4 = ctrl.Rule(deadline['jauh'] & urgensi['rendah'], prioritas['rendah'])
rule5 = ctrl.Rule(kesulitan['sulit'] & urgensi['rendah'], prioritas['sedang'])
rule6 = ctrl.Rule(deadline['jauh'] & kesulitan['mudah'], prioritas['rendah'])
rule7 = ctrl.Rule(deadline['sedang'] & kesulitan['sedang'] & urgensi['sedang'], prioritas['sedang'])
rule8 = ctrl.Rule(deadline['dekat'] & urgensi['rendah'], prioritas['sedang'])
rule9 = ctrl.Rule(deadline['dekat'] & urgensi['tinggi'] & kesulitan['sulit'], prioritas['tinggi'])
rule10 = ctrl.Rule(deadline['jauh'] & urgensi['rendah'], prioritas['rendah'])

# Membuat sistem kontrol fuzzy
prioritas_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
prioritas_simulasi = ctrl.ControlSystemSimulation(prioritas_ctrl)

# Fungsi untuk menghitung prioritas berdasarkan input
def hitung_prioritas(deadline_hari, kesulitan_val, urgensi_val):
    prioritas_simulasi = ctrl.ControlSystemSimulation(prioritas_ctrl)
    prioritas_simulasi.input['deadline'] = deadline_hari
    prioritas_simulasi.input['kesulitan'] = kesulitan_val
    prioritas_simulasi.input['urgensi'] = urgensi_val
    prioritas_simulasi.compute()
    return prioritas_simulasi.output['prioritas']

__all__ = ['deadline', 'kesulitan', 'urgensi', 'prioritas', 'hitung_prioritas']