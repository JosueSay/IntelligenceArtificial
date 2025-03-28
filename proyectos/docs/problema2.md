# Problema 2 - Red Neuronal: Cálculo de la función sen(x)

Este problema aborda la implementación de una red neuronal feedforward (también conocida como red multicapa o MLP) queimplementa un algoritmo de regresión no lineal para calcular la función sen(x) con x .

## Objetivo del Modelo

El objetivo del modelo es recibir un valor x entre  y devolver un vector de 10 dimensiones que representa los puntajes (logits) para cada clase del 0 al 9. El dígito más probable será el de mayor puntaje. Para entrenar esta red, se usa la pérdida de entropía cruzada (cross_entropy), ideal para tareas de clasificación multiclase.

**Importante:** No se debe aplicar activación ReLU en la última capa, ya que los logits deben pasar directamente a la función de pérdida.

## Arquitectura del Modelo

El modelo está definido en la clase `RegressionModel`, y tiene la siguiente arquitectura:

- Capa de Entrada: 1 entrada y 150 salidas, activación RelU
- Capa Oculta 1: 150 entradas y 150 salidas, activación ReLU
- Capa de salida 150 entradas y 1 salida, sin activación final

```python
super().__init__()
self.inp = Linear(1, 150)
self.layer = Linear(150, 150)
self.out = Linear(150, 1)
```

## Funciones Principales

### `forward(x)`
Aplica la función de activación en la capa de entrada y en la capa oculta de la red neuronal, retorna la salida de la capa final de la red.

```python
 x = relu(self.inp(x))  
x = relu(self.layer(x))
x = self.out(x) 
return x
```

### `get_loss(x, y)`
Calcula la pérdida entre las predicciones de la red neuronal y los valores reales utilizando la función mse_loss.
```python
predictions = self.forward(x)
return mse_loss(predictions, y)
```


### `train(dataset, epochs=...)`
Entrena el modelo usando descenso de gradiente con Adam (lr=0.001). El entrenamiento se ejecuta por varias épocas sobre el conjunto de entrenamiento. En cada época se calcula la pérdida total de cada batch en el dataset, luego, al final de iterar sobre cada batch se calcula la pérdida promedio, si esta es menor que 0.001 la iteración termina. 

data = DataLoader(dataset, batch_size=70, shuffle=True)
        optimizer = optim.Adam(self.parameters(), lr=0.001)
        epochs = 2000
```python
        
for epoch in range(epochs):
  total_loss = 0.0
  for batch in data:
    x_batch, y_batch = batch['x'], batch['label']
    optimizer.zero_grad()
    predictions = self(x_batch)
    loss = self.get_loss(x_batch, y_batch)  
    loss.backward()  
    optimizer.step()  
    total_loss += loss.item()

  avg_loss = total_loss / len(data)  

  if epoch % 200 == 0:
    print(f"Epoch {epoch}/{epochs} - Perdida: {avg_loss:.6f}")

if avg_loss <= 0.001:
    print(f"Deteniendo en la itreación {epoch} con perdida de {avg_loss:.6f}")
      break
```
## Evaluación del Modelo

- Se calcula la pérdida total de cada batch y se mejoran los parámetros de la ecuación con el optimizador de Adam, luego de evaluar la pérdida en cada batch, se calcula la pérdida en promedio .
- Se espera que el modelo alcance al menos una pérdida menor a 0.02.

## Resultados del modelo

- El modelo alcanza el valor de pérdida menor a 0.01 entre las 250 y 310 iteraciones en cada intento.
- La pérdida promedio oscila entre 0.0007 y 0.0008 en cada intento. 



## Cómo ejecutar este modelo

### Paso 1: Crear el entorno virtual

Ubícate en el directorio del proyecto y ejecuta:

```bash
python autograder.py -q q2
```

