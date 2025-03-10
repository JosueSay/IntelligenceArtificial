# Perceptrón Binario

## Descripción

En esta sección, implementarás un perceptrón binario. Tu tarea consistirá en completar la implementación de la clase `PerceptronModel` en el archivo `models.py`.

Para el perceptrón, las etiquetas de salida serán 1 o −1, lo que significa que los puntos de datos (x, y) del conjunto de datos tendrán valores de `y` como un `torch.Tensor` que contendrá 1 o −1 como sus entradas.

## Tareas

1. **Completar la función `init(self, dimensions)`**:  
   Esta función debe inicializar el parámetro de peso en `PerceptronModel`. Debes asegurarte de que la variable de peso se guarde como un objeto `Parameter()` de dimensión 1 por el número de dimensiones. Esto permitirá que nuestro sistema de calificación automática (autograder), así como Pytorch, reconozcan el peso como un parámetro de tu modelo.

   [Ones](https://pytorch.org/docs/stable/generated/torch.ones_like.html)

   [Parameter](https://pytorch.org/docs/stable/generated/torch.nn.parameter.Parameter.html)

2. **Implementar el método `run(self, x)`**:  
   Este método debe calcular el producto punto del vector de peso almacenado y la entrada proporcionada, devolviendo un objeto `Tensor`.

   [tensorDot](https://pytorch.org/docs/stable/generated/torch.tensordot.html)

3. **Implementar el método `get_prediction(self, x)`**:  
   Este método debe devolver 1 si el producto punto es no negativo, o −1 en caso contrario.

4. **Escribir el método `train(self)`**:  
   Este método debe recorrer el conjunto de datos repetidamente y hacer actualizaciones en los ejemplos mal clasificados. Cuando se complete un pase completo por el conjunto de datos sin cometer errores, se habrá alcanzado una precisión de entrenamiento del 100%, y el entrenamiento puede finalizar.

   Afortunadamente, Pytorch facilita la ejecución de operaciones sobre tensores. Si deseas actualizar el peso por alguna dirección de tensor y una magnitud constante, puedes hacerlo de la siguiente manera:

   ```python
   self.w += direction * magnitude
   ```

## Datos

Para esta tarea, así como para las tareas restantes, cada lote devuelto por el `DataLoader` será un diccionario en el formato:

```python
{'x': features, 'label': label}
```

Donde `label` es el valor o los valores que queremos predecir en función de las características `features`.

## Prueba

Para probar tu implementación, ejecuta el autograder:

```bash
python autograder.py -q q1
```

**Nota**: El autograder debería tomar como máximo unos 20 segundos para ejecutarse correctamente. Si el autograder tarda demasiado, es probable que haya un error en tu código.
