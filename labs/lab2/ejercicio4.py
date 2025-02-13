import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generar_muestra_gaussiana(n, media, covarianza):
    """
    Genera una muestra aleatoria de una distribución gaussiana multivariada
    de dimensión n con la media y covarianza especificadas.
    """
    muestra = np.random.multivariate_normal(media, covarianza, size=1000)
    df_muestra = pd.DataFrame(muestra, columns=[f'Variable_{i+1}' for i in range(n)])
    return df_muestra

def verificar_media_covarianza(muestra, media_teorica, covarianza_teorica):
    """
    Compara la media y la covarianza de la muestra con los valores teóricos.
    """
    media_muestra = muestra.mean()
    covarianza_muestra = muestra.cov()

    print(f'Media teórica: {media_teorica}')
    print(f'Media de la muestra:\n{media_muestra}')
    print(f'Covarianza teórica:\n{covarianza_teorica}')
    print(f'Covarianza de la muestra:\n{covarianza_muestra}')
    
    return media_muestra, covarianza_muestra

def graficar_pairplot(muestra):
    """
    Graficar un pairplot para visualizar las densidades y nubes de puntos
    entre las variables de la muestra. Se guarda en la carpeta images/.
    """
    os.makedirs("./images", exist_ok=True)
    pairplot = sns.pairplot(muestra)
    pairplot.fig.suptitle('Pairplot de la Muestra Aleatoria Gaussiana', y=1.02)
    pairplot.savefig("./images/pairplot_gaussiano.png")
    print("Gráfico guardado como './images/pairplot_gaussiano.png'")

n = 4 
media_teorica = np.array([0, 0, 0, 0]) 
covarianza_teorica = np.array([[1, 0.5, 0.3, 0.1],
                                [0.5, 1, 0.6, 0.2],
                                [0.3, 0.6, 1, 0.4],
                                [0.1, 0.2, 0.4, 1]]) 

muestra = generar_muestra_gaussiana(n, media_teorica, covarianza_teorica)
verificar_media_covarianza(muestra, media_teorica, covarianza_teorica)
graficar_pairplot(muestra)

