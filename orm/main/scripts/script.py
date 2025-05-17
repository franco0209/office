import time
from main.models import Empresa, Cuenta, Agencia, Inspector
from json import JSONDecodeError, loads, dumps

def deserializar_referencias(cuenta: Cuenta) -> list:

    try:
        return loads(cuenta.referencias or "[]")
    except JSONDecodeError:
        return []

def serializar_referencias(referencias: list) -> str:

    return dumps(referencias, ensure_ascii=False)

def searchEmpresa(ppto):
    pptoFilter = ppto.split()[0]
    empresa = Empresa.objects.filter(key = pptoFilter).first()
    return empresa

def searchAccountByName(addressee, cuentas):
    account = None
    namesClient = cuentas.values_list('nombre', flat=True)
    for name in namesClient:
        if name in addressee:
            account = cuentas.filter(nombre = name).first()
            return account
    return account

def searchAccountByKey(addresseeFilter, cuentas):
    account = None
    keysClient = cuentas.values_list('key', flat=True)
    for key in keysClient:
        if key in addresseeFilter:
            account = cuentas.get(key = key)
            return account
    return account

def searchAccountByReferences(addresseeFilter, cuentas):
    account = None
    for cuenta in cuentas:
        referencias = deserializar_referencias(cuenta)
        for referencia in referencias:
            if referencia in addresseeFilter:
                account = cuentas.get(nombre = cuenta.nombre)
                return account
    return account

def searchCuenta(addressee, client):
    cuentas = Cuenta.objects.filter(empresa = client)
    cuenta = None
    cuenta = searchAccountByName(addressee, cuentas)
    if cuenta is None:
        addresseeFilter = addressee.split()
        cuenta = searchAccountByKey(addresseeFilter, cuentas)
        if cuenta is None:
            cuenta = searchAccountByReferences(addresseeFilter, cuentas)
    return cuenta

def searchAgencia(addressee, cuenta):
    agencias = Agencia.objects.filter(cuenta = cuenta)
    agencia = None
    agencia = searchAccountByName(addressee, agencias)
    if agencia is None:
        addresseeFilter = addressee.split()
        agencia = searchAccountByKey(addresseeFilter, agencias)
        if agencia is None:
            agencia = searchAccountByReferences(addresseeFilter, agencias)
    return agencia

def searchInspectorByName(filterAddressee, inspectores):
    if isinstance(filterAddressee, str):
        search_terms = [filterAddressee.strip().lower()]
    else:
        search_terms = [term.strip().lower() for term in filterAddressee]
    
    names = inspectores.values_list('nombre', flat=True)
    normalized_names = {name.lower().strip(): name for name in names}
    
    matching_names = []
    for term in search_terms:
        if term in normalized_names:
            matching_names.append(normalized_names[term])
    
    if matching_names:
        return list(inspectores.filter(nombre__in=matching_names))
    else:
        for term in search_terms:
            for name in normalized_names.keys():
                if name in term:
                    matching_names.append(normalized_names[name])
    
    if matching_names:
        return list(inspectores.filter(nombre__in=matching_names))
    
    return []

def searchInspectorByKey(filterAddressee, inspectores):
    if isinstance(filterAddressee, str):
        search_terms = [filterAddressee.strip().lower()]
    else:
        search_terms = [term.strip().lower() for term in filterAddressee]
    
    names = inspectores.values_list('nombreClave', flat=True)
    normalized_names = {name.lower().strip(): name for name in names}
    
    matching_names = []
    for term in search_terms:
        if term in normalized_names:
            matching_names.append(normalized_names[term])
    
    if matching_names:
        return list(inspectores.filter(nombreClave__in=matching_names))
    else:
        for term in search_terms:
            for name in normalized_names.keys():
                if name in term:
                    matching_names.append(normalized_names[name])
    if matching_names:
        return list(inspectores.filter(nombreClave__in=matching_names))
    return []


def searchInspector(addressee, empresa):
    inspectores = Inspector.objects.filter(empresa=empresa)
    
    if isinstance(addressee, str) and '-' in addressee:
        parts = [part.strip() for part in addressee.split('-') if part.strip()]
        return searchInspectorByName(parts, inspectores)
    
    if isinstance(addressee, str) and '/' in addressee:
        parts = [part.strip() for part in addressee.split('/') if part.strip()]
        return searchInspectorByName(parts, inspectores)
    
    inspectors = searchInspectorByName(addressee, inspectores)

    if inspectors == []:
        inspectors = searchInspectorByKey(addressee, inspectores)
    return inspectors

def run():
    start_time_total = time.perf_counter_ns()
    
    start_empresa = time.perf_counter_ns()
    ppto = "SOD 0026"
    addressee = "SODIMAC AREQUIPA 1 - PORONGOCHE"
    inspectoresdir= "Sr. Renzo Torres"
    
    ppto = ppto.upper()
    addressee = addressee.upper()
    
    
    client = searchEmpresa(ppto)
    empresa_time = time.perf_counter_ns() - start_empresa
    
    print(f"Empresa encontrada: {client} | Tiempo: {empresa_time/1e6:.2f} ms ({empresa_time} ns)")
    
    start_cuenta = time.perf_counter_ns()
    cuenta = searchCuenta(addressee, client)
    cuenta_time = time.perf_counter_ns() - start_cuenta
    
    print(f"Cuenta encontrada: {cuenta} | Tiempo: {cuenta_time/1e6:.2f} ms ({cuenta_time} ns)")
    
    agencia = searchAgencia(addressee, cuenta)
    print(f"Agencia encontrada: {agencia}")
    inspectores = searchInspector(inspectoresdir, client)
    print(f"Inspectores encontrados: {inspectores}")
    total_time = time.perf_counter_ns() - start_time_total
    
    print(f"\nTiempo total: {total_time/1e6:.2f} ms ({total_time} ns)")
    
