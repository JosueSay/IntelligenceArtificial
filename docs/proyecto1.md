# Funciones Proporcionadas por Pytorch (Parte I)

## `tensor()`

Los tensores son la estructura de datos principal en Pytorch. Funcionan de manera similar a los arreglos de Numpy, en los que puedes realizar operaciones como suma y multiplicación. Para garantizar que tu entrada esté en la forma correcta, deberías asegurarte de que esté en forma de tensor. Puedes convertir una lista de Python en un tensor de la siguiente manera:

```python
tensor(data)
```

Donde `data` es tu lista n-dimensional.

## `relu(input)`

La función de activación ReLU en Pytorch se usa de la siguiente manera:

```python
relu(input)
```

Esta función toma un valor de entrada y devuelve el máximo entre `input` y 0.

## `Linear`

Utiliza esta clase para implementar una capa lineal. Una capa lineal toma el producto punto entre un vector de pesos y la entrada. Debes inicializar la capa en el constructor `__init__` de la siguiente manera:

```python
self.layer = Linear(longitud_del_vector_de_entrada, longitud_del_vector_de_salida)
```

Y llamarla al ejecutar el modelo:

```python
self.layer(input)
```

Pytorch crea automáticamente los pesos y los actualiza durante el entrenamiento cuando defines una capa lineal de esta manera.

## `movedim(input_vector, initial_dimension_position, final_dimension_position)`

Esta función toma una matriz y cambia la posición de la dimensión inicial (pasada como un entero) con la posición de la dimensión final.

### Ejemplo

```python
movedim(input_vector, 0, 1)
```

Este cambio será útil en la pregunta 4.

## `cross_entropy(prediction, target)`

Esta función es la función de pérdida recomendada para tareas de clasificación (Preguntas 3-5). Cuanto más alejada esté la predicción del objetivo, mayor será el valor que devolverá.

### Ejemplo

```python
cross_entropy(prediction, target)
```

## `mse_loss(prediction, target)`

Esta función se usa para tareas de regresión (Pregunta 2) y funciona de manera similar a `cross_entropy`. Es la función de pérdida adecuada para problemas de regresión.

### Ejemplo

```python
mse_loss(prediction, target)
```

## Uso de `DataLoader`

Todos los datos en la versión de Pytorch se proporcionarán en forma de un objeto `Dataset`, que se transformará en un `DataLoader` para facilitar la creación de tamaños de lotes.

### Ejemplo

```python
>>> data = DataLoader(training_dataset, batch_size=64)
>>> for batch in data:
>>>   # Código de entrenamiento aquí
```

Para todas estas preguntas, cada lote devuelto por el `DataLoader` será un diccionario en el formato:

```python
{'x': features, 'label': label}
```

Donde `label` es el valor o valores que queremos predecir basándonos en las características.
