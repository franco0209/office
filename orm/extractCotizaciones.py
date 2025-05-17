import openpyxl

cliente=""
    
def getPPTO(sheet, celda='J13'):
    codigoCotizacion = sheet[celda].value
    return codigoCotizacion

def getNOMBREINSPECTOR(sheet, celda='D18'):
    inspector = sheet[celda].value
    inspector = inspector.replace('Sr. ', '').replace('Sra. ', '')
    return inspector

def getDESCRIPCIÓN(sheet, celda='D19'):
    nombreServicio = sheet[celda].value
    return nombreServicio

###################################################################
###################################################################

def separateWord(word):
    first=word.split()[0]
    rest = " ".join(word.split()[1:])
    return [first,rest]

def getFirstTryClient(sheet, celda='D17'):
    firstClient = sheet[celda].value
    if '-' in firstClient:
        before_dash, after_dash = firstClient.split('-', 1)
        return [before_dash, after_dash]
    else:
        return separateWord(firstClient)
    
def getCLIENTE(sheet):
    global cliente
    
    cuentas={
        "sb":"scotiabank",
        "sbp":"scotiabank",
        "csf":"crediscotia financiera",
        "pv":"plaza vea",
        "bf":"banco falabella",
        "agencias":"agencias scotiabank",
        "outlet":"outlet arauco",
        "ib":"interbank",
        "ibk":"interbank",
        "entel":"entel",
        "efe":"efe",
    }
    
    [cliente,cuentaParcial]=getFirstTryClient(sheet)
    [cuentaParcial,agencia]=separateWord(cuentaParcial)
    try:
        cuentaParcial=(cuentas[cuentaParcial.lower()])
    except:
        agencia=cuentaParcial
        cuentaParcial=cliente
    return [cliente.upper(),cuentaParcial.upper(),agencia.upper()]   
    
    
###################################################################
###################################################################


def getCOSTO(sheet, celdaPRECIO='I', celdaCANTIDAD='H',inicio=25,fin=49):
    total=0
    for row in range(inicio, fin):
        precio = sheet[f'{celdaPRECIO}{row}'].value
        if precio is not None:
            if isinstance(precio, str):
                precio = precio.replace('S/', '').strip()
            try:
                cantidad = sheet[f'{celdaCANTIDAD}{row}'].value
                if cantidad is not None:
                    try:
                        print(precio)
                        print(cantidad)
                        total+=float(precio)*float(cantidad)
                        print(total)
                    except ValueError:
                        continue
            except ValueError:
                continue
    print(f"final: {total}")
    return total

def getESTADO(sheet,estado="NUEVO"):
    return estado

def getCODIGO(sheet,codigo="SIN OT"):
    global cliente
    print(cliente.lower)
    if 'tgestiona' in cliente.lower():
        codigo="SIN TICKET"
    return codigo

def getZONA(sheet,zona="AREQUIPA"):
    return zona


def getALLDATA(sheet):
    [cliente,cuenta,agencia]= getCLIENTE(sheet=sheet)
    data = {
        "NOMBRE_INSPECTOR": getNOMBREINSPECTOR(sheet=sheet),
        "PPTO": getPPTO(sheet=sheet),
        "COSTO": getCOSTO(sheet=sheet),
        "CLIENTE": cliente,
        "CUENTA": cuenta,
        "ESTADO": getESTADO(sheet=sheet),
        "CODIGO DEL SERVICIO": getCODIGO(sheet=sheet),
        "ZONA": "AREQUIPA",
        "AGENCIA/SEDE": agencia,
        "DESCRIPCIÓN DEL SERVICIO": getDESCRIPCIÓN(sheet=sheet),
    }
    return data


if __name__ == "__main__":
    print(separateWord("sassa"))