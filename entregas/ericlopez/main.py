class BankAccount:
    def __init__(self, account_number, account_holder, initial_balance):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Depósito exitoso de {amount}€. Nuevo saldo: {self.balance}€.")
        else:
            print("Error: El monto a depositar debe ser positivo.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Error: El monto a retirar debe ser positivo.")
            return
        if amount > self.balance:
            print(f"Fondos insuficientes. Saldo actual: {self.balance}€.")
        else:
            self.balance -= amount
            print(f"Retiro exitoso de {amount}€. Nuevo saldo: {self.balance}€.")

    def display_info(self):
        print(f"Cuenta: {self.account_number} | Titular: {self.account_holder} | Saldo: {self.balance}€")


class Main:
    def __init__(self):
        self.accounts = []

    def create_account(self):
        number = input("Ingrese el número de cuenta: ")
        holder = input("Ingrese el nombre del titular: ")
        try:
            initial_balance = float(input("Ingrese el saldo inicial: "))
        except ValueError:
            print("Saldo inicial no válido, se asignará 0.0€.")
            initial_balance = 0.0
        
        new_account = BankAccount(number, holder, initial_balance)
        self.accounts.append(new_account)
        print("Cuenta bancaria creada correctamente.")

    def find_account(self, number):
        for acc in self.accounts:
            if acc.account_number == number:
                return acc
        return None

    def process_deposit(self):
        number = input("Ingrese el número de cuenta para depósito: ")
        acc = self.find_account(number)
        if acc:
            try:
                amount = float(input("Ingrese el monto a depositar: "))
                acc.deposit(amount)
            except ValueError:
                print("Monto inválido.")
        else:
            print("Cuenta no encontrada.")

    def process_withdrawal(self):
        number = input("Ingrese el número de cuenta para retiro: ")
        acc = self.find_account(number)
        if acc:
            try:
                amount = float(input("Ingrese el monto a retirar: "))
                acc.withdraw(amount)
            except ValueError:
                print("Monto inválido.")
        else:
            print("Cuenta no encontrada.")

    def list_accounts(self):
        if not self.accounts:
            print("No hay cuentas registradas en el sistema.")
            return
        print("\n--- LISTA DE CUENTAS BANCARIAS ---")
        for acc in self.accounts:
            acc.display_info()

    def run(self):
        option = 0
        while option != 5:
            print("\n=== SISTEMA BANCARIO (Prueba Gerard) ===")
            print("1. Crear nueva cuenta")
            print("2. Realizar depósito")
            print("3. Realizar retiro")
            print("4. Mostrar todas las cuentas")
            print("5. Salir")
            
            try:
                option = int(input("Seleccione una opción: "))
                if option == 1:
                    self.create_account()
                elif option == 2:
                    self.process_deposit()
                elif option == 3:
                    self.process_withdrawal()
                elif option == 4:
                    self.list_accounts()
                elif option == 5:
                    print("Saliendo de la aplicación...")
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Por favor, introduzca un número válido.")
                option = 0


if __name__ == "__main__":
    program = Main()
    program.run()