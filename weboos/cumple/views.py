from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import cx_Oracle


#Para cuando hay SID
#dns = cx_Oracle.makedsn(host='10.80.123.15', port= '1521', sid='SID') 
#Para cuando hay service_NAME
def Consulta(modo, valor):
    results = [{'ID': '','NOMBRE_FUNCIONARIO': '', 'NOMBRE_CORTO': '', 'MES': '', 'DIA': '', 'CORREO': ''}]
    intento = 'fail'
    try:           
        connection_str = f"erbetancouca/TELEFONICA123@//ptmscan.nh.inet:1521/ORCLDB_SVC" 
        connection = cx_Oracle.connect(connection_str)    
        cursor = connection.cursor()
        if modo == 'total':     
                print(valor)
                sqlQuery = "select * from dsautom1.cumpleanos_test ORDER BY MES, DIA"
                print(sqlQuery)
                cursor.execute(sqlQuery)    
                column_names = [desc[0] for desc in cursor.description] # Obtiene los nombres de las columnas del cursor
                results = [dict(zip(column_names, row)) for row in cursor.fetchall()]# Recupera los datos y combínalos en una lista de diccionarios
                intento = 'ok'
            
        elif modo =='Consultar':
            try:            
                sqlQuery = "select * from dsautom1.cumpleanos_test where ID = '"+ valor[0] +"'"
                print(sqlQuery)
                cursor.execute(sqlQuery)    
                column_names = [desc[0] for desc in cursor.description] # Obtiene los nombres de las columnas del cursor
                results = [dict(zip(column_names, row)) for row in cursor.fetchall()]
                intento = 'ok'
            except cx_Oracle.Error as error:
                print(error)
                results = results
                intento = 'fail'
            
        elif modo =='Modificar':
            try:           
                sqlQuery = "UPDATE dsautom1.cumpleanos_test SET NOMBRE_CORTO = '"+valor[1]+"',MES = '"+valor[2]+"', DIA = '"+valor[3]+"' WHERE ID = '"+valor[0]+"'"
                print(sqlQuery)
                cursor.execute(sqlQuery)
                connection.commit()
                results = results
                intento = 'ok'
            except cx_Oracle.Error as error:
                print(error)
                results = results
                intento = 'fail'
        cursor.close()
        connection.close()
    except cx_Oracle.Error as error:
        print(error)
        results = results
        intento = 'fail'
    return results, intento

@login_required
def cumple(request):
    datosdonsulta, intento = Consulta('total',['total'])
    if intento == 'ok':
        titulo = 'Tabla Info Cumpleaños Área'
    else:
        titulo = 'Falla en la consulta, sin conexion a DB. Intente nuevamente'
    return render(request, 'cumple.html', {'datoscumple': datosdonsulta, 'titulo': titulo})

@csrf_exempt
@login_required
def capturar_datos(request):
    results = [{'ID': '','NOMBRE_FUNCIONARIO': '', 'NOMBRE_CORTO': '', 'MES': '', 'DIA': '', 'CORREO': ''}]
    titulo = ''
    titulo1 = ''
    mensajeia = ''
    if request.method == 'POST':
        action = request.POST.get('action')
        print(action)   
        id = request.POST.get('id')
        name = request.POST.get('name')
        nameshort = request.POST.get('nameshort')
        mes = request.POST.get('mes')
        dia = request.POST.get('dia')
        email = request.POST.get('email')
        if action == "Consultar":
            print(f"Consultar {id}")
            if id != '' and  esEntero(id):            
                datosdonsulta, intento = Consulta("Consultar",[id])
                if intento =='ok':
                    titulo = 'Info Cumpleaños ' + name
                else:
                    titulo1 = 'Consulta fallida BDOracle'
            else:
                datosdonsulta = results
                titulo1 = "Consulta fallida debe indicar ID"  
        elif action == "Modificar":            
            if nameshort == '':
                print(f"Modificar if {nameshort}")
                datosdonsulta, intento = Consulta("Consultar",[id])
                if intento =='ok':
                    titulo = 'Info Cumpleaños ' + name
                else:
                    titulo1 = 'Consulta fallida BDOracle'
                titulo1 = 'indique NOMBRE_CORTO'

            elif esEntero(mes) and esEntero(dia):
                print(f"Modificar elif1 {nameshort}")
                if 1 > int(mes) or int(mes) > 12:
                    datosdonsulta, intento = Consulta("Consultar",[id])
                    if intento =='ok':
                        titulo = 'Info Cumpleaños ' + name
                    else:
                        titulo1 = 'Consulta fallida BDOracle'
                    titulo1 = 'Mes no válido'
                elif 1 > int(dia) or int(dia) > 31 :
                    datosdonsulta, intento = Consulta("Consultar",[id])
                    if intento =='ok':
                        titulo = 'Info Cumpleaños ' + name
                    else:
                        titulo1 = 'Consulta fallida BDOracle'
                    titulo1 = 'Día no válido'          

                else:
                    print(f"Modificar else {nameshort}") 
                    try: 
                        print(f"Modificar try {nameshort}")
                        if esEntero(mes) and esEntero(dia):
                            try:
                                if int(mes) < 10: mes = f"{int(mes):02d}"
                                if int(dia) < 10: dia = f"{int(dia):02d}"
                                datosdonsulta, intento = Consulta("Modificar",[id,nameshort,mes,dia])
                                #print(f"Modificar try {datosdonsulta}")
                                if intento =='ok':
                                    datosdonsulta, intento = Consulta("Consultar",[id])
                                    titulo = f"Info Cumpleaños {name} modificado correctamente"
                                else:
                                    titulo1 = 'Consulta fallida BDOracle'
                            except ValueError:
                                datosdonsulta = results
                                titulo1 = "Entrada no válida. Debe ingresar un número válido en los campos de mes y dia."
                        else:
                            datosdonsulta = results
                            titulo1 = "Entrada no válida. Debe ingresar un número entero en los campos de mes y dia." 
                    except ValueError:
                        datosdonsulta = results
                        titulo1 = "Entrada no válida. Debe ingresar un número entero en los campos de mes y dia." 
            else:
                datosdonsulta = results
                titulo1 = "Entrada no válida. Debe ingresar un número entero en los campos de mes y dia." 

        elif action == "Reload":
            datosdonsulta, intento = Consulta('total',['total'])
            if intento == 'ok':
                titulo = 'Tabla Info Cumpleaños Área'
            else:
                titulo = 'Falla en la consulta, Intente nuevamente'
        
        elif action == 'mensajeia':
            if nameshort != '' and  esEntero(mes) and esEntero(dia):        
                mensajeia = Mensaje_cumple_IA(nameshort, mes, dia)
                datosdonsulta, intento = Consulta("Consultar",[id])
                if intento =='ok':
                    titulo = 'Info Cumpleaños ' + name
                else:
                    titulo1 = 'Consulta fallida BDOracle'
            else:
                datosdonsulta = results
                titulo1 = "Consulta fallida debe indicar ID" 

        elif action == 'Insertar':
            datosdonsulta, intento = Consulta('Insertar',['Insertar'])
        # Aquí puedes procesar los datos, por ejemplo, guardarlos en la base de datos
        # o realizar alguna lógica adicional
        return render(request, 'cumple.html', {'datoscumple': datosdonsulta,'titulo': titulo,'titulo1': titulo1,'mensajeia': mensajeia})
    else:
        datosdonsulta, intento = Consulta('total',['total'])
        if intento == 'ok':
            titulo = 'Tabla Info Cumpleaños Área'
        else:
            titulo = 'Falla en la consulta, sin conexion a DB. Intente nuevamente'
        return render(request, 'cumple.html', {'datoscumple': datosdonsulta,'titulo': titulo,'titulo1': titulo1})

    #['ID', 'NOMBRE_FUNCIONARIO', 'NOMBRE_CORTO', 'MES', 'DIA', 'CORREO', 'SENDER_NAME', 'SENDER_ADDRES', 'ESTADO']
    #'''[{'ID': 1, 
    #  'NOMBRE_FUNCIONARIO': 'Adriana Lucia Narvaez Morales', 
    #  'NOMBRE_CORTO': 'Adriana', 
    #  'MES': '08', 
    #  'DIA': '11', 
    #  'CORREO': 'adriana.narvaez@telefonica.com', 
    #  'SENDER_NAME': 'Ing. Conmutacion y OSS', 
    #  'SENDER_ADDRES': 'pentaho@telefonica.com.co', 
    #  'ESTADO': 1}]'''

    #return render(request, 'cumple.html') 
    #return render(request, 'asistenteAI.html',{'form':contact_form , 'poema':poema}) 

def esEntero(cadena):
    try:
        numero = int(cadena)
        return True
    except ValueError:
        print(f"Error: '{cadena}' no es un número entero válido.")
        return False
    
def Mensaje_cumple_IA(nombre, mes, dia ):
    import os 
    import openai
    from openai import OpenAI
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider


    comportamiento = f'Genera un mensaje de cumpleaños muy especial y novedoso de 50 palabras para una persona que se llama {nombre} nacio el mes {mes} y e dia {dia} aprovecha un evento especial que haya ocurrido ese mismo mes y dia en la histora para generar tu mensaje.'
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        client = OpenAI()
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
            "content":  "eres Especialista en mensajes autenticos de cumpleaños."
            },
            {"role": "user",
            "content": comportamiento
            }
        ]
        )
        return (response.choices[0].message.content)

    except Exception as error:
        print(error)
        return (error)
