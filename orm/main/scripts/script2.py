
from main.models import Empresa, Cuenta, Agencia, Inspector, Cotizacion
from json import JSONDecodeError, loads, dumps

def deserializar_referencias(cuenta: Cuenta) -> list:

    try:
        return loads(cuenta.referencias or "[]")
    except JSONDecodeError:
        return []

def serializar_referencias(referencias: list) -> str:

    return dumps(referencias, ensure_ascii=False)

def crearSantander():
    tgs = Empresa.objects.get(id = 1)
    santander = Cuenta(empresa = tgs, key = 'CF', nombre = 'SANTANDER')
    santander.save()

    
def corregirAgencias():
    tgs = Empresa.objects.get(id = 1)
    caf = Cuenta.objects.get(key = 'CSF')
    cs =Cuenta.objects.get(key = 'CF')
    agencias = Agencia.objects.filter(cuenta = caf)   
    print(agencias)
    for agencia in agencias:
        agencia.cuenta = cs
        agencia.save()

def corregirAgencias2():
    tgs = Empresa.objects.get(id = 1)
    cs =Cuenta.objects.get(key = 'CF')
    cs.key = "CSF"
    cs.referencias = ""
    cs.save()

def run():
    mkaqp2= Agencia.objects.get(id =37)
    refe = serializar_referencias(["AREQUIPA 1","AREQUIPA1", "MAKRO AREQUIPA 1"])
    mkaqp1= Agencia(nombre = "MAKRO AREQUIPA 1", key = "MAKRO AREQUIPA 1", ciudad = mkaqp2.ciudad, cuenta = mkaqp2.cuenta, empresa = mkaqp2.empresa, referencias = refe)
    mkaqp1.save()
    