"""

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


"""

from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, to: str, msg: str) -> None:
        pass

class EmailSender(Notifier):
    def send(self, to: str, msg: str) -> None:
        print(f"SMTP -> {to}: {msg}")


class SmsSender(Notifier):
    def send(self, to: str, msg: str) -> None:
        print(f"SMS -> {to}: {msg}")


class OrderService:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def place_order(self, to: str, msg: str) -> None:
        # ... lógica de orden ...
        self.notifier.send(to, msg)


if __name__ == "__main__":
    # Puedes cambiar EmailSender por SmsSender sin tocar OrderService
    notifier = EmailSender()
    # notifier = SmsSender()  # alternativo

    service = OrderService(notifier)
    service.place_order("user@test.com", "Gracias por su compra")
