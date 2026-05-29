# Informe de Corrección Automática - ericlopez

## Calificación Final: 3.5 / 10

## Desglose Detallado de los Criterios Evaluados

*   **POO y Encapsulamiento (3 puntos): 0 / 3**
    *   **Evaluación:** Se observa la definición de clases (`BankAccount`, `Main`) y métodos de lógica de negocio. Sin embargo, los atributos de la clase `BankAccount` (`account_number`, `account_holder`, `balance`) no están definidos como privados. En Java, la convención para atributos privados es usar la palabra clave `private`. Al no aplicar este principio fundamental de encapsulamiento, el requisito esencial de este punto no se cumple.

*   **Manejo de Excepciones y Errores (3 puntos): 1.5 / 3**
    *   **Evaluación:** Se ha implementado correctamente el uso de bloques `try-except` para manejar entradas de usuario inválidas (`ValueError` en Python, equivalente a `NumberFormatException` en Java) en varias secciones del código (creación de cuenta, depósitos, retiros y selección del menú principal), lo cual evita el cierre inesperado del programa. No obstante, no se ha creado ni utilizado al menos una excepción personalizada, tal como se especificaba en la rúbrica (ej. para fondos insuficientes).

*   **Uso de Colecciones (2 puntos): 0 / 2**
    *   **Evaluación:** El sistema utiliza una lista de Python (`self.accounts = []`) para gestionar múltiples cuentas, y se itera sobre ella para buscar y listar, lo cual es funcionalmente correcto para Python. Sin embargo, la rúbrica especifica explícitamente el uso de "colecciones de Java, concretamente un `ArrayList`". Dado que el código no está en Java, no se cumple con el tipo de colección requerido en el lenguaje especificado por las instrucciones.

*   **Funcionalidad del Menú Interactivo (2 puntos): 2 / 2**
    *   **Evaluación:** El programa implementa un bucle `while` que cumple la función de un `do-while` y una estructura `if-elif-else` que emula un `switch` para el menú interactivo. Todas las funcionalidades requeridas (crear cuentas, depositar, retirar, listar y salir) están presentes y operativas, permitiendo una interacción fluida con el usuario.

## Aspectos Positivos Destacados del Código

*   **Estructura del Menú:** El menú interactivo está bien organizado y permite al usuario navegar por las opciones principales del sistema bancario de manera clara.
*   **Manejo Básico de Errores:** La implementación de `try-except ValueError` para las entradas numéricas es un buen comienzo para robustecer la aplicación contra errores de usuario comunes.
*   **Claridad de Lógica:** La lógica de las operaciones bancarias básicas (depósito, retiro, visualización) y la gestión de cuentas son comprensibles y funcionales.
*   **Ausencia de Comentarios:** Cumple con la instrucción de no contener comentarios.

## Errores Detectados y Propuestas de Mejora Específicas

1.  **Violación de Requisito de Lenguaje (Crítico):**
    *   **Error:** Las `instrucciones_extra` de la rúbrica establecían de forma categórica: "El código debe estar estrictamente en Java." El proyecto ha sido entregado en Python. Esta es una falta grave y fundamental que invalida gran parte de la evaluación, ya que el proyecto no cumple con el entorno tecnológico principal solicitado. En un entorno universitario real, esto resultaría en una calificación muy baja o nula.
    *   **Propuesta de Mejora:** El alumno debe rehacer *íntegramente* el proyecto en **Java**, prestando especial atención a la sintaxis y buenas prácticas de dicho lenguaje.

2.  **Incumplimiento de Encapsulamiento (POO):**
    *   **Error:** Los atributos de la clase `BankAccount` (ej. `self.balance`) son públicos. No se utilizan modificadores de acceso (`private` en Java) para proteger los datos internos de la clase.
    *   **Propuesta de Mejora:**
        *   **Archivo:** `BankAccount.java` (cuando se migre a Java).
        *   **Cambio:** Declare todos los atributos (`account_number`, `account_holder`, `balance`) como `private`.
        *   **Cambio:** Implemente métodos `public` `getters` (ej. `getBalance()`) para acceder a la información si es necesario y métodos específicos para modificar la información (`deposit`, `withdraw`) que contengan la lógica de negocio.

3.  **Falta de Excepción Personalizada:**
    *   **Error:** La rúbrica exigía la creación y uso de al menos una excepción personalizada (ej. para "fondos insuficientes"). El código actual maneja esta situación con un simple `print`.
    *   **Propuesta de Mejora:**
        *   **Archivo:** Crear un nuevo archivo (ej. `InsufficientFundsException.java` cuando se migre a Java).
        *   **Cambio:** Defina una clase que herede de `Exception` (o `RuntimeException` en Java) y utilícela en el método `withdraw` de `BankAccount` para lanzar la excepción en caso de fondos insuficientes. El bloque `try-catch` correspondiente deberá capturar esta excepción en el método `process_withdrawal` de la clase `Main`.

4.  **Uso Incorrecto de Colecciones (contexto Java):**
    *   **Error:** La rúbrica demandaba específicamente un `ArrayList` de Java. El uso de una `list` de Python no cumple con esta especificación de lenguaje y tipo.
    *   **Propuesta de Mejora:**
        *   **Archivo:** `Main.java` (cuando se migre a Java).
        *   **Cambio:** Sustituya la declaración de la colección por `private List<BankAccount> accounts = new ArrayList<>();`. Asegúrese de importar `java.util.List` y `java.util.ArrayList`.

5.  **Simulación de `do-while` y `switch` (contexto Java):**
    *   **Error:** Aunque funcionalmente correctas para Python, las estructuras `while` y `if-elif-else` no son las que se esperan si la rúbrica menciona `do-while` y `switch` en un contexto de Java.
    *   **Propuesta de Mejora:**
        *   **Archivo:** `Main.java` (cuando se migre a Java).
        *   **Cambio:** Reemplace el bucle `while (option != 5)` por un `do-while` equivalente en Java.
        *   **Cambio:** Reemplace la cadena `if-elif-else` para la selección del menú por una sentencia `switch` en Java.