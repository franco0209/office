import win32com.client
import openpyxl
import os
from extractCotizaciones import getALLDATA

def generateEmail(data, data2, nameInforme):
    print(data)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    firma_path = os.path.join(script_dir, "firma.png")
    
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    
    attachment = mail.Attachments.Add(firma_path)
    attachment_cid = "firma123"
    attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", attachment_cid)
    
    recipients = {
        "gerald": "galea@tgestiona.com.pe",
        "julio": "galea@tgestiona.com.pe",
        "renzo": "rtorresmo@sodimac.com.pe",
        "juan": "jolguinoc@tgestiona.com.pe",
        "hector": "hvasquezc@tgestiona.com.pe",
        "isabel": "iriverav@tgestiona.com.pe",
        "gonzalo": "jhuallpa@national.com.pe",
        "jonathan": "jastete@tottus.com.pe",
        "jonathan2": "jespejo@national.com.pe",
        "jose": "jgarciah@tgestiona.com.pe",
        "josé": "jgarciah@tgestiona.com.pe",
        "alfonso": "supervisor.sur@national.com.pe",
        "gustavo": "gcentenod@tgestiona.com.pe",
    }
    
    mujeres=['isabel']
    
    name_Inspector=((data["NOMBRE_INSPECTOR"]).split()[0]).lower()
    saludo="Estimad"
    
    capital_name=name_Inspector.capitalize()
    
    if name_Inspector in mujeres:
        saludo=saludo+f"a {capital_name}"
    else:
        saludo=saludo+f"o Sr. {capital_name}"    
    
    try:
        mail.To = recipients[name_Inspector]
    except Exception as e:
        print(e)
        
    mail.CC="<josesotom@electrototalsecurity.com>; 'Analista Operaciones Electrototal' <analista.operaciones@electrototalsecurity.com>; <asistente.administrativo@electrototalsecurity.com>; <asistente.operaciones@electrototalsecurity.com>"
    mail.Subject = f"COTIZACIÓN {data['PPTO']} || {data['DESCRIPCIÓN DEL SERVICIO']} || {data['CUENTA']} {data['AGENCIA/SEDE']}"
    namespace = outlook.GetNamespace("MAPI")
    for account in namespace.Accounts:
        print(account.DisplayName)
    for account in outlook.Session.Accounts:
        if account.DisplayName == "cotizaciones@electrototalsecurity.com":
            mail._oleobj_.Invoke(*(64209, 0, 8, 0, account))
            break

    estadoCorreo=data2[0]
    estadoCorreoString=''
    if estadoCorreo==1:
        estadoCorreoString = 'actualizada '
    elif estadoCorreo ==2:
        estadoCorreoString = 'y los entregables '
    elif estadoCorreo ==3:
        estadoCorreoString = 'actualizada y los entregables '
    
    
    saludo2 = f"Se envía nuestra cotización {estadoCorreoString}en atención del siguiente servicio, para que pueda brindarnos la aprobación formal por correo:"
    datacostobruta=data["COSTO"]
    data["COSTO"] = f"{data['COSTO']:.2f} Sin IGV"
    filtered_data = {key: value for key, value in data.items() if key != "NOMBRE_INSPECTOR"}
    table = """<table border='1' style='border-collapse: collapse; font-family: Calibri; color: #2F5597; font-size:9pt;'>
                <tr style='background-color: #2F5597; font-family: Arial; color: white; font-size: 10pt; font-weight: normal;'>
                    """ + "".join(f"<th style='text-align: center; padding: 4px;'>{key}</th>" for key in filtered_data.keys()) + """
                </tr>"""

    table += "<tr>" + "".join(f"<td style='text-align: center; padding: 4px; vertical-align: middle;'>{val}</td>" for val in filtered_data.values()) + "</tr>"      
    table += "</table>"
    
    ticket_info=""
    
    print(data["ESTADO"])
    print(data["CLIENTE"].lower())
    if(data["ESTADO"]=='NUEVO'): 
        envio_ticket=' la OT'
        complement_ticket=""
        if("tgestiona" in data["CLIENTE"].lower()):
            envio_ticket='l tícket'
            if(datacostobruta)<(700/1.18):
                complement_ticket="(caso contrario indicar si el pago es por planilla recurrente)"
                
        ticket_info=f"Para proceder con el inicio de los trabajos se requiere del envío de{envio_ticket}, aprobación del servicio por correo y la orden de compra{complement_ticket}."
    
    firma = f"""<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 width=695 style='width:521.2pt;background:white;border-collapse:collapse;mso-yfti-tbllook:1184;mso-padding-alt:0cm 0cm 0cm 0cm'>
    <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes;height:73.1pt'>
        <td width=288 valign=top style='width:216.3pt;padding:0cm 5.4pt 0cm 5.4pt;height:73.1pt'>
            <p class=MsoNormal align=right style='text-align:right'>
                <span style='color:#1F497D;'> 
                    <img src='cid:{attachment_cid}' width='274' height='97' />
                </span>
            </p>
        </td>
        <td width=407 valign=top style='width:304.9pt;padding:0cm 5.4pt 0cm 5.4pt;height:73.1pt'>
            <table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 align=left width=392 style='width:294.1pt;border-collapse:collapse;mso-yfti-tbllook:1184;'>
                <tr style='mso-yfti-irow:0;height:11.8pt'>
                    <td width=392 valign=top style='width:294.1pt;padding:0cm 0cm 0cm 0cm;height:11.8pt'></td>
                </tr>
                <tr style='mso-yfti-irow:1;height:10.95pt'>
                    <td width=392 valign=top style='width:294.1pt;padding:0cm 0cm 0cm 0cm;height:10.95pt'>
                        <p class=MsoNormal><b><span style='font-family:"Arial",sans-serif;color:#6699FF;'>José Luis Soto Marin</span></b></p>
                    </td>
                </tr>
                <tr style='mso-yfti-irow:2;height:6.55pt'>
                    <td width=392 valign=top style='width:294.1pt;padding:0cm 0cm 0cm 0cm;height:6.55pt'>
                        <p class=MsoNormal><span lang=ES style='font-family:"Arial",sans-serif;color:#6699FF;'>Jefe de Operaciones</span></p>
                    </td>
                </tr>
                <tr style='mso-yfti-irow:3;height:6.55pt'>
                    <td width=392 valign=top style='width:294.1pt;padding:0cm 0cm 0cm 0cm;height:6.55pt'>
                        <p class=MsoNormal style='margin-bottom: 5px;'><span lang=ES style='font-family:"Arial",sans-serif;color:#6699FF;'>999 999 944</span></p>
                    </td>
                </tr>
                <tr style='mso-yfti-irow:4;height:6.55pt'>
                    <td width=392 valign=top style='width:294.1pt;padding:0cm 0cm 0cm 0cm;height:6.55pt'>
                        <p class=MsoNormal style='margin-bottom: 5px;'>
                            <a href="mailto:josesotom@electrototalsecurity.com"><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:blue;'>josesotom@electrototalsecurity.com</span></a>
                        </p>
                    </td>
                </tr>
                <tr style='mso-yfti-irow:5;height:6.55pt'>
                    <td width=392 valign=top style='width:294.1pt;padding:0cm 0cm 0cm 0cm;height:6.55pt'>
                        <p class=MsoNormal style='margin-bottom: 5px;'>
                            <a href="mailto:electrototals@gmail.com"><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:blue;'>electrototals@gmail.com</span></a>
                        </p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    </table>"""
    
    mail.HTMLBody = f"""
    <html>
        <body style='font-family: Calibri; color: #2F5597; font-style: italic; font-size: 12pt;'>
            <p>{saludo}</p> 
            <p>{saludo2}</p> 
            {table}
            <p>{ticket_info}</p> 
            <p>Quedamos atentos a sus comentarios.</p>
            <p>Saludos cordiales.</p>
            {firma}
        </body>
    </html>
    """
    try:
        coti = os.path.join(script_dir, f"{nameInforme}.pdf")
        if os.path.exists(coti):
            mail.Attachments.Add(coti)
    except:
        print("NO PDF")
    

    mail.Display()

def identifyACTUALIZACIÓN(ppto):
    if '_' in ppto:
        return 1
    return 0
def identifyENTREGABLES(name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    entregables_path = os.path.join(script_dir, f"{name}.pdf")
    if os.path.exists(entregables_path):
        return 2
    else:
        return 0

if __name__ == "__main__":
    name=input("Ingresar nombre de la cotización:")
    nameXLSX=f'{name}.xlsx' 
    wb = openpyxl.load_workbook(nameXLSX,data_only=True)
    sheet = wb.active
    data=getALLDATA(sheet)
    data2=[identifyACTUALIZACIÓN(ppto=data["PPTO"])+identifyENTREGABLES(name=name)]
    generateEmail(data,data2,name)