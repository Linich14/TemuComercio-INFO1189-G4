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


############################################

############################################

############################################


# Despues (SRP)
class ReportData: 
    def __init__(self, data: dict = None):
        if data is None:
            data = {"ventas": 1200, "fecha": str(datetime.now())}
        self.data = data

    def get_data(self):
        return self.data

class ReportFormatter:
    def __init__(self, report_data: ReportData):
        self.report_data = report_data

    def format_report(self):
        data = self.report_data.get_data()
        return f"REPORTE: ventas={data['ventas']} fecha={data['fecha']}"

class ReportManager:
    def __init__(self):
        self.report_data = ReportData()
        self.report_formatter = ReportFormatter(self.report_data)

    def run_report(self):
        report = self.report_formatter.format_report()
        print(report)

if __name__ == "__main__":
    ReportManager().run_report()