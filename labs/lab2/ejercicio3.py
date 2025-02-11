import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import ks_2samp

def primer_digito(n):
    """Extrae el primer dígito de un número positivo."""
    while n >= 10:
        n //= 10
    return n

def distribucion_benford():
    """Devuelve la distribución teórica de la Ley de Benford."""
    return {d: math.log10(1 + 1/d) for d in range(1, 10)}

def analizar_ley_benford(ruta_archivo):
    df = pd.read_csv(ruta_archivo, delimiter=';')
    print(df.columns)
    
    df["Area en kilómetros cuadrados"] = pd.to_numeric(df["Area in square kilometres"], errors='coerce')
    
    primeros_digitos = df["Area en kilómetros cuadrados"].dropna().astype(int).apply(primer_digito)
    
    frecuencias_observadas = primeros_digitos.value_counts(normalize=True).sort_index()
    
    probabilidades_benford = distribucion_benford()
    
    observadas = [frecuencias_observadas.get(d, 0) for d in range(1, 10)] 
    teoricas = [probabilidades_benford[d] for d in range(1, 10)]
    
    ks_statistic, ks_p_value = ks_2samp(observadas, teoricas)
    print(f"Estadístico de Kolmogorov-Smirnov: {ks_statistic}")
    print(f"Valor p de la prueba: {ks_p_value}")
    
    if ks_p_value < 0.05:
        print("Rechazamos la hipótesis nula: Los datos no siguen la Ley de Benford.")
    else:
        print("No rechazamos la hipótesis nula: Los datos siguen la Ley de Benford.")

    plt.figure(figsize=(10, 6))
    plt.bar(frecuencias_observadas.index, frecuencias_observadas.values, width=0.5, label='Observado', color='b', alpha=0.6)
    plt.plot(list(probabilidades_benford.keys()), list(probabilidades_benford.values()), marker='o', linestyle='-', color='r', label='Benford')
    plt.xlabel('Primer Dígito')
    plt.ylabel('Frecuencia Relativa')
    plt.title('Distribución de Primeros Dígitos vs. Ley de Benford')
    plt.xticks(range(1, 10))
    plt.legend()
    plt.grid()
    plt.savefig("./images/benford_plot.png") 
    print("Gráfico guardado como './images/benford_plot.png'")

analizar_ley_benford('areas.csv')
