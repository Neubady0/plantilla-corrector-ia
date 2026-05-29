# Informe de Corrección Automática - gerardgomez

## Calificación Final: 10 / 10

## Desglose Detallado de los Criterios Evaluados:

### 1. POO_y_Encapsulamiento (3 puntos)
*   **Evaluación:** El alumno ha implementado la clase `BankAccount` con atributos privados (`accountNumber`, `accountHolder`, `balance`) y métodos públicos para su acceso (`getAccountNumber`, `getAccountHolder`, `getBalance`). Los métodos `deposit` y `withdraw` encapsulan correctamente la lógica de negocio para modificar el saldo. La clase `Main` también demuestra una buena estructura, encapsulando la colección de cuentas y el `Scanner`.
*   **Puntuación:** 3 / 3 puntos.

### 2. Manejo_de_Excepciones_y_Errores (3 puntos)
*   **Evaluación:** El código utiliza bloques `try-catch` de manera consistente y efectiva para manejar `NumberFormatException` en todas las entradas numéricas del usuario (`createAccount`, `processDeposit`, `processWithdrawal`, `run`). Se ha creado una excepción personalizada `InsufficientFundsException` que hereda correctamente de `Exception`, y es lanzada (`throw`) desde el método `withdraw` de `BankAccount` y capturada (`catch`) en `processWithdrawal`.
*   **Puntuación:** 3 / 3 puntos.

### 3. Uso_de_Colecciones (2 puntos)
*   **Evaluación:** Se ha utilizado un `ArrayList<BankAccount>` (`accounts`) en la clase `Main` para gestionar múltiples cuentas bancarias. Se demuestra la capacidad de añadir cuentas (`accounts.add`) y de iterar sobre ellas para buscar (`findAccount`) y listar (`listAccounts`) de forma adecuada.
*   **Puntuación:** 2 / 2 puntos.

### 4. Funcionalidad_del_Menu_Interactivo (2 puntos)
*   **Evaluación:** El programa presenta un menú interactivo robusto implementado con un bucle `do-while` que continúa hasta que el usuario selecciona la opción de salir (5). La lógica de selección se maneja eficazmente mediante una estructura `switch` que invoca las funciones correspondientes (crear cuenta, depositar, retirar, listar, salir). La interacción es fluida y los mensajes para el usuario son claros.
*   **Puntuación:** 2 / 2 puntos.

## Aspectos Positivos Destacados:
*   **Adherencia Estricta a la Rúbrica:** El proyecto cumple impecablemente con cada uno de los requisitos establecidos en la rúbrica, incluyendo las instrucciones extra de no usar comentarios y de utilizar Java.
*   **Diseño POO Sólido:** La implementación de las clases `BankAccount` y `Main` demuestra una comprensión clara de los principios de la Programación Orientada a Objetos y el encapsulamiento.
*   **Manejo de Errores Robusto:** La gestión de excepciones para entradas de usuario inválidas y la creación y uso de la excepción personalizada `InsufficientFundsException` son ejemplares, contribuyendo a la estabilidad del programa.
*   **Claridad del Código:** A pesar de la ausencia de comentarios (según lo solicitado), el código es legible y su lógica es fácil de seguir.

## Errores Detectados y Propuestas de Mejora Específicas:
El proyecto cumple con todos los requisitos de la rúbrica, por lo que no se detectan errores que impidan la calificación máxima. Sin embargo, como profesor, siempre es bueno pensar en la mejora continua y en la robustez de un sistema real. A continuación, algunas propuestas de mejora para futuras iteraciones del proyecto:

1.  **Cierre del Recurso `Scanner`:**
    *   **Lógica/Archivo:** `Main.java`
    *   **Detalle:** El objeto `Scanner` (`this.scanner`) se inicializa en el constructor de `Main` pero nunca se cierra explícitamente. Aunque para `System.in` no siempre es crítico, es una buena práctica liberar recursos.
    *   **Propuesta de mejora:** Implementar el método `close()` del `Scanner` cuando la aplicación finalice, por ejemplo, añadiendo un `scanner.close()` justo antes de `System.out.println("Saliendo de la aplicación...");` en el método `run()`.

2.  **Validación de Unicidad de Número de Cuenta:**
    *   **Lógica/Archivo:** `Main.java` (método `createAccount` y `findAccount`)
    *   **Detalle:** Actualmente, el sistema permite crear múltiples cuentas bancarias con el mismo número de cuenta. En un sistema bancario real, los números de cuenta deben ser únicos para evitar conflictos y asegurar la integridad de los datos.
    *   **Propuesta de mejora:** Antes de añadir una nueva cuenta en `createAccount`, verificar si el `accountNumber` ya existe utilizando el método `findAccount`. Si ya existe, se debería informar al usuario y no crear la cuenta, o solicitar un número diferente.

3.  **Manejo de la Validación de Montos Positivos en `BankAccount`:**
    *   **Lógica/Archivo:** `BankAccount.java` (métodos `deposit` y `withdraw`)
    *   **Detalle:** Los métodos `deposit` y `withdraw` imprimen un mensaje de error si el monto es <= 0. Aunque funcional, una práctica más orientada a objetos sería lanzar una `IllegalArgumentException` (una excepción estándar de Java) desde `BankAccount` para que la capa de presentación (`Main` en este caso) sea quien capture y muestre el mensaje al usuario. Esto mantiene la lógica de negocio pura y desacoplada de la interfaz de usuario.
    *   **Propuesta de mejora:** Modificar `deposit` para que lance una `IllegalArgumentException` si `amount <= 0`. Similarmente para `withdraw` si `amount <= 0`. Luego, en `processDeposit` y `processWithdrawal`, añadir un `catch (IllegalArgumentException e)` para mostrar el mensaje adecuado.