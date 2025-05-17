
from main.models import Empresa, Cuenta, Agencia, Inspector, Cotizacion
from json import JSONDecodeError, loads, dumps

def deserializar_referencias(cuenta: Cuenta) -> list:

    try:
        return loads(cuenta.referencias or "[]")
    except JSONDecodeError:
        return []

def serializar_referencias(referencias: list) -> str:

    return dumps(referencias, ensure_ascii=False)

def run():
    insp = Inspector(nombre = "Marcos Rogelio Cañari Chavaria", correo = "mcanaric@tgestiona.com.pe", nombreClave = "Marcos", empresa = Empresa.objects.get(id = 1))
    insp.save()