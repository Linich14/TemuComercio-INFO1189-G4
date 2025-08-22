# ANTES (DIP)
class EmailSender:
    def send(self, to: str, msg: str) -> None:
        print(f"SMTP -> {to}: {msg}")

class OrderService:
    def __init__(self):
        self.email = EmailSender()  # dependencia rígida a un detalle

    def place_order(self, to: str, msg: str) -> None:
        # ... lógica de orden ...
        self.email.send(to, msg)

if __name__ == "__main__":
    OrderService().place_order("user@test.com", "Gracias por su compra")