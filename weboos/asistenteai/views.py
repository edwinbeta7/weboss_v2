from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from openai import OpenAI
import zipfile
import os, re, math
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader
from docx import Document
import tiktoken

### Configuracion Variables globales ChatGPTOpenAI
# Cargar las variables de entorno desde el archivo .env
#load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
# Create your views here.
def prueba(request):
    #codigo
    "Hola"
    return JsonResponse({'respuesta':""})
    #return render(request, 'home.html')

@csrf_exempt
def asistenteai(request):
    #contact_form=ContactForm()
    filename = ""
    if request.method == 'POST':
        #contact_form = ContactForm(data=request.POST) 
        action = request.POST.get('action')
        filenameget = request.POST.get('rutafile')
        pregunta = request.POST.get('pregunta')
        print(action)
        print(filenameget)
        if action == 'Seleccionar':
            filetypes = (('pdf files', '*.pdf'),("Word files", "*.docx"),('All files', '*.*'))
            root = tk.Tk()
            # Abre cuandro de dialogo para seleccionar archivo pdf-file dialog            
            loaded=True
            filename = tk.filedialog.askopenfilename(title='Seleccione el archivo .pdf para analizar', filetypes=filetypes)
            root.destroy()
            root.mainloop()
            print(filename)
            return render(request, 'asistenteAI.html',{'textruta':filename, 'len':len(filename)}) 
        elif action == 'Analizar':
            ruta_val, ext = validacion_ruta_ingresada(str(filenameget), 'tx')
            if ruta_val=='ok':
                if ext == '.pdf' or ext == ".docx":
                    res = convierte_to_txt(str(filenameget),ext, 1 )
                    resultado = res[0]
                    rutafull_txt = res[1]
                    if resultado[:3]=="***":
                        return render(request, 'asistenteAI.html',{'textruta':filenameget, 'len':len(filenameget), 'resumen':resultado})
                    else:
                        ValTokens = num_tokens_from_string(resultado)
                        if ValTokens < 16000:
                            resultadoia = genera_archivo_txt_IA(resultado, rutafull_txt, ext)
                            return render(request, 'asistenteAI.html',{'textruta':filenameget, 'len':len(filenameget), 'resumen':resultadoia})   
                        else:
                            resultado_n, textocompleto = particiona_txt(ValTokens, resultado, rutafull_txt, ext )
                            #nombre_arch_sinext = Path(ruta_arch).stem
                            resultado = f"Tokens Excedidos: El documento tiene {str(ValTokens)} Tokens, el máximo permitido es de 16000, se dividio en {len(resultado_n)} archivos\n {textocompleto}"
                            return render(request, 'asistenteAI.html',{'textruta':filenameget, 'len':len(filenameget), 'resumen':resultado}) 

                elif ext == 'im':
                    #resultado = convierte_to_txt(ruta_val,ext )
                    return render(request, 'asistenteAI.html',{'textruta':filenameget, 'len':len(filenameget), 'resumen':'resultado'}) 
            return render(request, 'asistenteAI.html',{'textruta':filenameget,'len':len(filenameget),'resumen':ruta_val}) 
        elif action == 'Preguntar':
            ruta_val, ext = validacion_ruta_ingresada(str(filenameget), 'tx')           
            if ruta_val == 'ok':
                res = convierte_to_txt(str(filenameget),ext, 1 )
                resultado = res[0] 
                if pregunta == '':
                    return render(request, 'asistenteAI.html',{'textruta':filenameget,'len':len(filenameget),'resumen':resultado,'pregunta':pregunta, 'respuesta':'Indique su pregunta.'})
                else: 
                    ruta_arch_txt = os.path.dirname(filenameget)
                    nombre_arch_sinext = Path(filenameget).stem
                    ruta_val_txt = nombre_arch_sinext+'.txt'                
                    rutafull_txt = ruta_arch_txt + '\\' + ruta_val_txt
                    respuestaOAI = Pregunta_texto_IA(rutafull_txt, pregunta)
                    guardar_preguntas_txt(pregunta, respuestaOAI, rutafull_txt)
                    return render(request, 'asistenteAI.html',{'textruta':filenameget,'len':len(filenameget),'resumen':resultado,'pregunta':pregunta, 'respuesta':respuestaOAI}) 
            else:
                return render(request, 'asistenteAI.html',{'textruta':filenameget,'len':len(filenameget),'resumen':ruta_val,'pregunta':pregunta,'respuesta':ruta_val}) 
    return render(request, 'asistenteAI.html',{'textruta':''})

## Verifiacion de que la ruta del archivo exista y sea formato pdf
def validacion_ruta_ingresada(ruta_usu, tipo):
    resultado = ""
    ext=''
    ruta_arch = ruta_usu.strip('"')     
    if  ruta_arch == "":
        resultado = "Error en la ruta, No se ha seleccionado el documento, vuelva a intentarlo."
    else:
        ruta_ing_normal = os.path.abspath(ruta_arch)
        if os.path.exists(ruta_ing_normal):
            extension_ing_usu = os.path.splitext(ruta_ing_normal) 
            if  str(extension_ing_usu[1]) == ".pdf" or str(extension_ing_usu[1]) == ".docx":
                resultado = 'ok'
                ext= str(extension_ing_usu[1])
            else:
                resultado ="El formato del archivo debe ser extension <.pdf> o <.docx>"        
        else:
            resultado = "El archivo no existe"
    return resultado, ext

## Estraccion datos tecnologia OCR conversion de archivo pdf a txt guardado de archivo txt
def convierte_to_txt(ruta_arch, extension, n):
    resultado = ''
    ruta_arch_txt = os.path.dirname(ruta_arch)
    nombre_arch_sinext = Path(ruta_arch).stem
    match extension:
            case ".pdf" :
                nombre_arch_txt = nombre_arch_sinext+'.txt'
                rutafull_txt = ruta_arch_txt + '\\' + nombre_arch_txt  
            case ".docx":
                nombre_arch_txt = nombre_arch_sinext+'.txt'
                rutafull_txt = ruta_arch_txt + '\\' + nombre_arch_txt 
            case "im":
                # Carpeta donde se guardarán las imágenes
                output_folder = os.path.dirname(os.path.abspath(__file__))
                # Nombre del archivo de salida
                rutafull_txt = os.path.join(output_folder, f"{os.path.splitext(ruta_arch)[0]}.txt")
                          
    if os.path.exists (rutafull_txt):
        if extension == ".pdf" or extension == ".docx" or "im" :
            mensj1 = "***El archivo ya fue analizado***\n"         
            ##   Lee el archivo TXT y extrae el resumen del documento.
            file = open(rutafull_txt, encoding="utf8")
            for linea in file:
                s = re.search('Resumen del documento(.*)',linea)
                if s: break
            resultado = mensj1+s.group(0), rutafull_txt
        else: resultado = ''
    else:        
        textopaginas = ""
        match extension:
            case ".pdf" :
                print('lectura documento pdf')
                reader = PdfReader(ruta_arch)
                number_of_pages = len(reader.pages)
                for page in range(number_of_pages):
                    pages = reader.pages[page]
                    textopagina = pages.extract_text()
                    textopaginas = textopaginas + re.sub("\n", "", textopagina) + "\n" 
                resultado= textopaginas, rutafull_txt
            case ".docx":
                print('lectura documento word')
                docx = zipfile.ZipFile(ruta_arch)
                content = docx.read('word/document.xml').decode('utf-8')
                textopaginas = re.sub('<(.|\n)*?>','',content)
                resultado= textopaginas, rutafull_txt

            case "im": 
                textopagina = ''
                # Ruta a Tesseract-OCR si no está en PATH (por ejemplo, en Windows)
                #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                # Carpeta donde se guardarán las imágenes
                #output_folder = os.path.dirname(os.path.abspath(__file__))
                # Nombre del archivo de salida
                #rutafull_txt = os.path.join(output_folder, f"{os.path.splitext(ruta_arch)[0]}.txt")
                # Abrir el documento PDF
                #pdf_document = fitz.open(ruta_arch)
                #for page_num in range(pdf_document.page_count):
                        # Obtener la página
                        #page = pdf_document.load_page(page_num)        
                        # Convertir la página a una imagen de pixmap
                        #pix = page.get_pixmap()        
                        # Crear una imagen a partir del pixmap
                        #img = Image.open(io.BytesIO(pix.tobytes()))
                        # Usar pytesseract para extraer texto
                        #text = pytesseract.image_to_string(img)
                        #textopaginas = textopaginas + text+'\n' 
                        #textopaginas = textopaginas + re.sub("\n", "", text) + "\n"  
                # Guardar el texto extraído en un archivo .txt
                #with open(textopaginas, 'w', encoding='utf-8') as f: 
                    # Recorrer cada página del documento 
                        #f.write(text+'\n')
        
    return resultado

## valida la cantidad de tokens que se van a enviar a la IA NO PUEDE SER MAYOR DE 16000    
def num_tokens_from_string(textoDocumento) -> int:
    """Returns the number of tokens in a text string."""
    ##encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0125")
    num_tokens = len(encoding.encode(str(textoDocumento)))
    return num_tokens

# divide el texto en varios archivos dependiendo la cantidad de tokens cuando se exceden los 16000 tokens.
def particiona_txt(ValTokens, resultado, ruta_arch, ext):    
    n = math.ceil(ValTokens/15000)
    long = len(resultado)
    largo=math.ceil(long/n)
    resultado_n=[]    
    ruta_arch_txt = os.path.dirname(ruta_arch)
    nombre_arch_sinext = Path(ruta_arch).stem
    textocompleto = ''
    for i in range(n):
        ini_car = i*largo
        fin_car = ini_car + largo 
        nombre_arch_txt = nombre_arch_sinext + str(i+1) +'.txt'
        rutafull_txt = ruta_arch_txt + '\\' + nombre_arch_txt
        resultado_i = resultado[ini_car:fin_car]
        resultadoia_n = genera_archivo_txt_IA(resultado_i, rutafull_txt, ext)
        f = open(ruta_arch,'a')
        f.write("********** Resumen del documento: ")
        f.write(str(resultadoia_n.encode("ascii", "replace")))
        f.close()
        resultado_n.append(resultadoia_n)
        textocompleto = f"{textocompleto} {resultadoia_n}\n"
    return resultado_n, textocompleto

# Generar archivo txt con respuesta de la IA
def genera_archivo_txt_IA(resultado, rutafull_txt, ext):
    if ext == '.pdf' or ext == '.docx':
        f = open(rutafull_txt,'a')
        f.write(str(resultado.encode("ascii", "replace")))
        f.close()
        mensj1 = (f"{rutafull_txt} \nLa IA generó el siguiente resumen del documento: \n")
        resultado1 = Resumen_texto_IA(rutafull_txt)
        ## Guardar resumen al final del archivo de texto
        archi1=open(rutafull_txt,"a")
        archi1.write("********** Resumen del documento: ")
        archi1.write(str(resultado1.encode("ascii", "replace")))
        archi1.close()
        resultado = mensj1+resultado1

    else:
        resultado = ""    
    return resultado

## Guardar un archivo txt con llamado nombrearchivos_preguntas con el listado de las preguntas que se le hacen al documento pdf.
def guardar_preguntas_txt(pregunta,respuesta,nArchivotxt):
    ruta_arch_txt = os.path.dirname(nArchivotxt)
    nombre_arch_siext = Path(nArchivotxt).stem
    nombre_arch_txt = nombre_arch_siext+'_preguntas.txt'
    rutafull_txt = ruta_arch_txt + '\\' + nombre_arch_txt
    if os.path.exists (rutafull_txt):
        Archivo_pre_txt = open(rutafull_txt, "a")
        Archivo_pre_txt.write("\n"+"\n"+"<P> "+pregunta+"\n"+"<R> "+respuesta)        
        Archivo_pre_txt.close()
    else:
        Archivo_pre_txt = open(rutafull_txt, "w")
        Archivo_pre_txt.write("<P> "+pregunta+"\n"+"<R> "+respuesta)        
        Archivo_pre_txt.close()
    return

## Realizar peticion a OPENAI para saber de que se trata el archivo
def Resumen_texto_IA(ruta_arch_txt):
    comportamiento = ''
    rta=''
    with open(ruta_arch_txt, 'r', encoding='utf-8') as text_file:
        prompt = text_file.read()
        comportamiento = 'Eres un experto en analizar textos de todo tipo, por favor analiza, resume y dame una respuesta de maximo 200 palabras del siguiente texto: ' + f'{prompt}'
    
    try:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", 
            "content": comportamiento
            },
            {"role": "user", 
            "content": "De que se trata este texto?, por favor resumelo en máximo 300 palabras"
            }
        ],
        temperature=1
        )
        rta= (str(completion.usage.prompt_tokens) + "/" + str(completion.usage.completion_tokens) +' Tokens' +  " <> " +  completion.choices[0].message.content)
    except:
        rta = 'Falla en consultar la IA'

    '''client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version="2024-05-01-preview",
    )
    completion = client.chat.completions.create(
    model=deployment_name,
    messages= [
    {
      "role": "user",
      "content": comportamiento
    }],
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
    )'''
   # print(completion.to_json())

    return rta
    #return (str(num_tokens_from_string(prompt)) + "/" + str(num_tokens_from_string(completion.to_json())) +' Tokens' +  " <> " + completion.to_json())

## Realizar peticion a OPENAI de la pregunta de usuario
def Pregunta_texto_IA(ruta_arch_txt, pregunta_texto):
    comportamiento = ''
    with open(ruta_arch_txt, 'r', encoding='utf-8') as text_file:
        prompt = text_file.read()
        comportamiento = 'Eres un experto en analizar a profundidad textos de todo tipo, por favor analiza el siguiente texto y contesta la pregunta, puedes apoyarte tambien en internet' + prompt
    
    try:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", 
            "content": comportamiento
            },
            {"role": "user", 
            "content": pregunta_texto
            }
        ]
        )
        rta = (completion.choices[0].message.content)
    except:
        rta = 'Falla en consultar la IA'
    return rta
