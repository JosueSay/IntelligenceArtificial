# Problema 3 - Red Neuronal: Clasificación de Dígitos

Este problema aborda la implementación de una red neuronal feedforward (también conocida como red multicapa o MLP) entrenada para resolver el problema de clasificación de dígitos escritos a mano, utilizando el conjunto de datos MNIST. Cada imagen en este dataset es de 28x28 píxeles, lo que se transforma en vectores de 784 dimensiones.

## Objetivo del Modelo

El objetivo del modelo es recibir una imagen (vector de 784 valores de tipo float) y devolver un vector de 10 dimensiones que representa los puntajes (logits) para cada clase del 0 al 9. El dígito más probable será el de mayor puntaje. Para entrenar esta red, se usa la pérdida de entropía cruzada (cross_entropy), ideal para tareas de clasificación multiclase.

**Importante:** No se debe aplicar activación ReLU en la última capa, ya que los logits deben pasar directamente a la función de pérdida.

## Arquitectura del Modelo

El modelo está definido en la clase `DigitClassificationModel`, y tiene la siguiente arquitectura:

- Capa de Entrada: 784 neuronas (una por píxel)
- Capa Oculta 1: 150 neuronas, activación ReLU
- Capa Oculta 2: 50 neuronas, activación ReLU
- Capa Oculta 3: 50 neuronas, activación ReLU
- Capa de Salida: 10 neuronas (una por clase), sin activación final

```python
self.fc1 = Linear(784, 150)
self.fc2 = Linear(150, 50)
self.fc3 = Linear(50, 50)
self.fc4 = Linear(50, 10)  # logits (sin ReLU aquí)
```

## Funciones Principales

### `run(x)`

Ejecuta una forward pass por la red. Aplica activaciones ReLU en todas las capas excepto la última.

```python
x = relu(self.fc1(x))
x = relu(self.fc2(x))
x = relu(self.fc3(x))
logits = self.fc4(x)
return logits
```

### `get_loss(x, y)`

Calcula la pérdida entre las predicciones (logits) y las etiquetas verdaderas y usando entropía cruzada.

### `train(dataset, epochs=...)`

Entrena el modelo usando descenso de gradiente con Adam (lr=0.001). El entrenamiento se ejecuta por varias épocas sobre el conjunto de entrenamiento.

## Evaluación del Modelo

- Durante el entrenamiento, se calcula la precisión sobre el conjunto de validación con `dataset.get_validation_accuracy()`.
- Se espera que el modelo alcance al menos 97% de precisión en validación, aunque se recomienda apuntar a 97.5%-98% para asegurarse de pasar el calificador automático, que usa un conjunto de prueba oculto.

## Buenas Prácticas de Entrenamiento

- Entrenar durante aproximadamente 5 épocas es suficiente en la mayoría de los casos.
- Si la precisión no mejora después de algunas épocas, puedes detener el entrenamiento antes.
- No aplicar softmax manualmente a la salida, ya que la función `cross_entropy()` se encarga internamente de eso.
- Asegurarse de que los datos estén bien normalizados (por ejemplo, escalados entre 0 y 1).

## Cómo ejecutar en un entorno virtual

### Paso 1: Crear el entorno virtual

Ubícate en el directorio del proyecto y ejecuta:

```bash
python -m venv venv
```

Esto creará un entorno virtual llamado venv.

### Paso 2: Activar el entorno virtual

En bash/zsh:

```bash
source venv/bin/activate
```

### Paso 3: Instalar las dependencias

```bash
pip install -r requirements.txt
```

```bash
pip install -r ../otra_carpeta/requirements.txt
```
