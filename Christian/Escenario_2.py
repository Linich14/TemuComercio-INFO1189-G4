# ANTES (OCP)
class PaymentProcessor:
    def process(self, payment_type: str, amount: float):
        if payment_type == "cash":
            print(f"Efectivo: {amount}")
        elif payment_type == "card":
            print(f"Tarjeta: {amount}")
        elif payment_type == "transfer":
            print(f"Transferencia: {amount}")
        else:
            raise ValueError("Tipo no soportado")

if __name__ == "__main__":
    PaymentProcessor().process("card", 100.0)


# Despues (OCP)
class PaymentMethod:
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
    PaymentProcessor().process(TransferPayment(), 100.0)
