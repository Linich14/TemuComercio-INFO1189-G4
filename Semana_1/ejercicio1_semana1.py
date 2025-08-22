"""
# ANTES (SRP)
import json
from datetime import datetime

class ReportManager:
    def run_report(self):
        # cargar datos
        data = {"ventas": 1200, "fecha": str(datetime.now())}

        # formatear
        text = f"REPORTE: ventas={data['ventas']} fecha={data['fecha']}"

        # persistir
        with open("reporte.txt", "w", encoding="utf-8") as f:
            f.write(text)

        # presentar
        print(text)

if __name__ == "__main__":
    ReportManager().run_report()


"""

from datetime import datetime


#funcion con responsabilidad que obtiene los datos
class DataSource:
    def get_data(self):
        return {
            "ventas": 1200,
            "fecha": datetime.now()
        }

#Funcion con responsabilidad que escribe el archivo
class FileOutput:
    def write(self, text, filename="reporte.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

#funcion con responsabilidad para cambiar elformato del texto
class ReportFormatter:
    def format(self, data):
        fecha_str = data["fecha"].strftime("%Y-%m-%d %H:%M:%S")
        return f"REPORTE: ventas={data['ventas']} fecha={fecha_str}"


#funcion con responsabilidad para mostrar la informacion
class ConsoleOutput:
    def write(self, text):
        print(text)

#clase que orquesta el servicio uniendo todos los componentes
class ReportService:
    def __init__(self, data_source, formatter, outputs):
        self.data_source = data_source
        self.formatter = formatter
        self.outputs = outputs  # lista de salidas

    def run(self):
        data = self.data_source.get_data()
        text = self.formatter.format(data)
        for output in self.outputs:
            output.write(text)


if __name__ == "__main__":
    data_source = DataSource()
    formatter = ReportFormatter()
    outputs = [FileOutput(), ConsoleOutput()]
    service = ReportService(data_source, formatter, outputs)
    service.run()
