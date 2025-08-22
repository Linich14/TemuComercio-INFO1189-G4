# ANTES (OCP)

class PaymentMethod:
    def __init__(self, name: str):
        self.name = name

    def process_payment(self, amount: float):
        raise NotImplementedError("Este método debe ser implementado por subclases")
    
class CashPayment(PaymentMethod):
    def process_payment(self, amount: float):
        print(f"Efectivo: {amount}")

class CardPayment(PaymentMethod):
    def process_payment(self, amount: float):
        print(f"Tarjeta: {amount}")

class TransferPayment(PaymentMethod):
    def process_payment(self, amount: float):
        print(f"Transferencia: {amount}")

class PaymentProcessor:
    def process(self, payment_method: PaymentMethod, amount: float):
        payment_method.process_payment(amount)

if __name__ == "__main__":
    PaymentProcessor().process(CardPayment(), 100.0)
