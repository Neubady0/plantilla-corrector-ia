# Informe de Corrección Automática - gerardgomez

---

## Nota Final: 10 / 10

---

### Desglose Detallado de los Criterios Evaluados:

*   **POO y Encapsulamiento:** 3 / 3 puntos
    *   Se han definido clases claras como `BankAccount` y `InsufficientFundsException`.
    *   Los atributos de `BankAccount` (`accountNumber`, `accountHolder`, `balance`) son privados, garantizando el encapsulamiento.
    *   Se utilizan métodos públicos (`getters`, `deposit`, `withdraw`, `displayInfo`) para interactuar con la información y la lógica de negocio, respetando el principio de encapsulamiento.

*   **Manejo de Excepciones y Errores:** 3 / 3 puntos
    *   El código hace un uso correcto de los bloques `try-catch` para manejar `NumberFormatException` en la entrada de datos numéricos (saldo inicial, montos de depósito/retiro, selección del menú), previniendo cierres inesperados del programa.
    *   Se ha implementado una excepción personalizada `InsufficientFundsException` que hereda de `Exception` y se lanza adecuadamente cuando el saldo es insuficiente durante un retiro, siendo capturada y manejada correctamente.

*   **Uso de Colecciones:** 2 / 2 puntos
    *   Se utiliza un `ArrayList<BankAccount>` (`accounts`) en la clase principal para gestionar múltiples cuentas bancarias, cumpliendo con el requisito de colecciones de Java.
    *   Se itera sobre esta colección para buscar cuentas (`findAccount`) y para listar todas las cuentas registradas (`listAccounts`), demostrando un uso efectivo de la colección.

*   **Funcionalidad del Menú Interactivo:** 2 / 2 puntos
    *   El programa contiene un bucle `do-while` en el método `run()` que gestiona la interacción del usuario.
    *   Se utiliza una estructura `switch` dentro del bucle para manejar las diferentes opciones del menú (crear cuenta, depositar, retirar, listar, salir).
    *   Todas las funcionalidades requeridas están presentes y operativas, proporcionando una interacción fluida al usuario.

---

### Aspectos Positivos Destacados del Código:

*   **Claridad y Organización:** El código está bien estructurado y es fácil de leer, con una separación lógica de responsabilidades entre las clases.
*   **Robustez:** La implementación de manejo de excepciones es sólida, abordando las entradas inválidas del usuario y condiciones de negocio específicas como los fondos insuficientes.
*   **Coherencia:** Se siguen las buenas prácticas de POO y encapsulamiento de manera consistente a lo largo del proyecto.
*   **Completitud:** El proyecto cumple con todos los requisitos funcionales y técnicos establecidos en la rúbrica.

---

### Errores Detectados y Propuestas de Mejora Específicas:

No se han detectado errores que impidan el cumplimiento de los criterios de la rúbrica o que causen fallos críticos en la ejecución del programa. Sin embargo, en aras de la mejora continua y las buenas prácticas, se ofrecen las siguientes propuestas:

*   **Gestión de Recursos (main.java - línea 76 y otras):** El objeto `Scanner` (`scanner`) se inicializa en el constructor de la clase `main` (que en este caso actúa como la aplicación principal) pero nunca se cierra explícitamente. Aunque para aplicaciones de consola simples esto a menudo se pasa por alto, es una buena práctica cerrar los recursos que implementan `AutoCloseable` (como `Scanner`) para liberar los recursos del sistema.
    *   **Propuesta de mejora:** Considere cerrar el `Scanner` cuando la aplicación termina. Esto se puede lograr añadiendo un método `close()` a la clase `main` y llamándolo antes de que la aplicación finalice, o gestionándolo dentro del método `run()` si el `Scanner` se inicializara localmente (lo cual requeriría un cambio de diseño). Para la estructura actual, se podría llamar a `scanner.close();` justo antes de `System.out.println("Saliendo de la aplicación...");` en el `case 5` o en un bloque `finally` si el `Scanner` se gestionase de otra forma.

*   **Nomenclatura de la Clase Principal (main.java - línea 74):** Si bien Java permite que una clase se llame `main` si contiene el método `main`, es una convención común dar a la clase principal de una aplicación un nombre más descriptivo que refleje su rol, como `BankingSystem`, `BankApp` o `Program`. El nombre `main` puede causar confusión en proyectos más grandes o al referenciar la clase.
    *   **Propuesta de mejora:** Renombrar la clase `main` a un nombre más significativo como `BankingSystem` o `BankApp`. Esto implicaría cambiar `public class main {` a `public class BankingSystem {` y, consecuentemente, en el método `main` al crear la instancia: `BankingSystem program = new BankingSystem();`.