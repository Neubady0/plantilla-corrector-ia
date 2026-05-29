import java.util.ArrayList;
import java.util.Scanner;

class InsufficientFundsException extends Exception {
    public InsufficientFundsException(String message) {
        super(message);
    }
}

class BankAccount {
    private String accountNumber;
    private String accountHolder;
    private double balance;

    public BankAccount(String accountNumber, String accountHolder, double initialBalance) {
        this.accountNumber = accountNumber;
        this.accountHolder = accountHolder;
        this.balance = initialBalance;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public String getAccountHolder() {
        return accountHolder;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Depósito exitoso de " + amount + "€. Nuevo saldo: " + balance + "€.");
        } else {
            System.out.println("Error: El monto a depositar debe ser positivo.");
        }
    }

    public void withdraw(double amount) throws InsufficientFundsException {
        if (amount <= 0) {
            System.out.println("Error: El monto a retirar debe ser positivo.");
            return;
        }
        if (amount > balance) {
            throw new InsufficientFundsException("Fondos insuficientes. Saldo actual: " + balance + "€.");
        }
        balance -= amount;
        System.out.println("Retiro exitoso de " + amount + "€. Nuevo saldo: " + balance + "€.");
    }

    public void displayInfo() {
        System.out.println("Cuenta: " + accountNumber + " | Titular: " + accountHolder + " | Saldo: " + balance + "€");
    }
}

public class main {
    private ArrayList<BankAccount> accounts;
    private Scanner scanner;

    public main() {
        accounts = new ArrayList<>();
        scanner = new Scanner(System.in);
    }

    public void createAccount() {
        System.out.print("Ingrese el número de cuenta: ");
        String number = scanner.nextLine();
        System.out.print("Ingrese el nombre del titular: ");
        String holder = scanner.nextLine();
        System.out.print("Ingrese el saldo inicial: ");
        double initialBalance = 0;
        try {
            initialBalance = Double.parseDouble(scanner.nextLine());
        } catch (NumberFormatException e) {
            System.out.println("Saldo inicial no válido, se asignará 0.0€.");
        }

        BankAccount newAccount = new BankAccount(number, holder, initialBalance);
        accounts.add(newAccount);
        System.out.println("Cuenta bancaria creada correctamente.");
    }

    public BankAccount findAccount(String number) {
        for (BankAccount acc : accounts) {
            if (acc.getAccountNumber().equals(number)) {
                return acc;
            }
        }
        return null;
    }

    public void processDeposit() {
        System.out.print("Ingrese el número de cuenta para depósito: ");
        String number = scanner.nextLine();
        BankAccount acc = findAccount(number);
        if (acc != null) {
            System.out.print("Ingrese el monto a depositar: ");
            try {
                double amount = Double.parseDouble(scanner.nextLine());
                acc.deposit(amount);
            } catch (NumberFormatException e) {
                System.out.println("Monto inválido.");
            }
        } else {
            System.out.println("Cuenta no encontrada.");
        }
    }

    public void processWithdrawal() {
        System.out.print("Ingrese el número de cuenta para retiro: ");
        String number = scanner.nextLine();
        BankAccount acc = findAccount(number);
        if (acc != null) {
            System.out.print("Ingrese el monto a retirar: ");
            try {
                double amount = Double.parseDouble(scanner.nextLine());
                acc.withdraw(amount);
            } catch (NumberFormatException e) {
                System.out.println("Monto inválido.");
            } catch (InsufficientFundsException e) {
                System.out.println("Error: " + e.getMessage());
            }
        } else {
            System.out.println("Cuenta no encontrada.");
        }
    }

    public void listAccounts() {
        if (accounts.isEmpty()) {
            System.out.println("No hay cuentas registradas en el sistema.");
            return;
        }
        System.out.println("\n--- LISTA DE CUENTAS BANCARIAS ---");
        for (BankAccount acc : accounts) {
            acc.displayInfo();
        }
    }

    public void run() {
        int option = 0;
        do {
            System.out.println("\n=== SISTEMA BANCARIO (Prueba Gerard) ===");
            System.out.println("1. Crear nueva cuenta");
            System.out.println("2. Realizar depósito");
            System.out.println("3. Realizar retiro");
            System.out.println("4. Mostrar todas las cuentas");
            System.out.println("5. Salir");
            System.out.print("Seleccione una opción: ");

            try {
                option = Integer.parseInt(scanner.nextLine());
                switch (option) {
                    case 1:
                        createAccount();
                        break;
                    case 2:
                        processDeposit();
                        break;
                    case 3:
                        processWithdrawal();
                        break;
                    case 4:
                        listAccounts();
                        break;
                    case 5:
                        System.out.println("Saliendo de la aplicación...");
                        break;
                    default:
                        System.out.println("Opción inválida.");
                }
            } catch (NumberFormatException e) {
                System.out.println("Por favor, introduzca un número válido.");
                option = 0;
            }
        } while (option != 5);
    }

    public static void main(String[] args) {
        main program = new main();
        program.run();
    }
}