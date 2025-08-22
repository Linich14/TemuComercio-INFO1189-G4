# ANTES (ISP)
from abc import ABC, abstractmethod


class Worker(ABC):
    @abstractmethod
    def work(self) -> None: ...
    @abstractmethod
    def eat(self) -> None: ...
    @abstractmethod
    def attend_meeting(self) -> None: ...

class Robot(Worker):
    def work(self) -> None:
        print("Produciendo")
    def eat(self) -> None:
        raise NotImplementedError("Un robot no come")
    def attend_meeting(self) -> None:
        print("¿Tiene sentido que un robot asista?")

if __name__ == "__main__":
    Robot().eat()  # explota/absurdo

# DESPUÉS (ISP)
class Worker(ABC):
    @abstractmethod
    def work(self) -> None: ...

class Eater(ABC):
    @abstractmethod
    def eat(self) -> None: ...

class Attendee(ABC):
    @abstractmethod
    def attend_meeting(self) -> None: ...

class Robot(Worker, Attendee):
    def work(self) -> None:
        print("Produciendo")
        
    def attend_meeting(self) -> None:
        print("¿Tiene sentido que un robot asista?")

if __name__ == "__main__":
    Robot().eat()  # explota/absurdo