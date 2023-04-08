# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 01:03:21 2022

@author: BENJAMIN MIGUEL
"""

import sqlite3                                          # Para trabajar con la base de datos
from ast import Break, Return                           # Para salir de un bucle
from datetime import *                                  # Para trabajar con fechas
from tkinter import *                                   # Para crear la interfaz gráfica
from tkinter.ttk import Combobox                        # Para crear los combobox
from reportlab.lib.pagesizes import A4,landscape        # 210mm x 297mm   # Para crear el PDF
from reportlab.pdfgen import canvas                     # Para crear el PDF
from reportlab.lib.units import mm                      # Para crear el PDF
from reportlab.pdfbase import pdfmetrics                # Para crear el PDF
from reportlab.pdfbase.ttfonts import TTFont            # Para crear el PDF
import shutil                                           # Para copiar archivos
import os                                               # Para borrar archivos
import time                                             # Para trabajar con el tiempo
import copy                                             # Para crear copias de variables
import keyboard                                         # Para detectar pulsaciones de teclas
#  ----------------------------------- Raiz -----------------------------------

raiz = Tk()                                             # Crea la ventana raiz
raiz.title("CN Control")                                # Le da un título a la ventana
raiz.iconbitmap("image/icono.ico")                      # Le da un icono a la ventana
raiz.config(bg="#b7b493")                               # Le da un color de fondo a la ventana
raiz.config(bd=10)                                      # Le da un borde a la ventana
raiz.config(relief="groove")                            # Le da un tipo de borde a la ventana
alto = raiz.winfo_screenheight()                        # Obtiene el alto de la pantalla
ancho = raiz.winfo_screenwidth()                        # Obtiene el ancho de la pantalla
raiz.geometry(f"{ancho}x{alto}")                        # Le da el tamaño de la pantalla a la ventana
raiz.resizable(0, 0)                                    # Evita que se pueda cambiar el tamaño de la ventana
raiz.state("zoomed")                                    # Ajusta la ventana a la pantalla

logo = PhotoImage(file="image/logo.png")                # Carga laimagen del logo
logo = logo.subsample(8, 8)                             # Lo colocamos en raiz utilizando la transparencia
Label(raiz, image=logo, bg="#b7b493").place(x=30, y=20) # Lo colocamos en raiz utilizando la transparencia
        
raiz.bind("<Control-r>", lambda event: menuRegistrosIntroducir("Yes"))  # Si en cualquier momento se pulsan las teclas CTRL + R se va al menu de registro
raiz.bind("<Control-R>", lambda event: menuRegistrosIntroducir("Yes"))
raiz.bind("<Control-c>", lambda event: copia())                         # Si en cualquier momento se pulsa las teclas CTRL + C intenta copiar al portapapeles
raiz.bind("<Control-C>", lambda event: copia())
raiz.bind("<Control-v>", lambda event: paste())                         # Si en cualquier momento se pulsan las teclas CTRL + V intenta copiar lo del portapapeles
raiz.bind("<Control-V>", lambda event: paste())
raiz.bind("<Control-e>", lambda event: paste())                         # Si en cualquier momento se pulsan las teclas CTRL + V se va al menu de ventas
raiz.bind("<Control-E>", lambda event: paste())
raiz.bind("<Control-i>", lambda event: menuIncidenciasIntroducir("Yes"))# Si en cualquier momento se pulsan las teclas CTRL + I se va al menu de incidencias
raiz.bind("<Control-I>", lambda event: menuIncidenciasIntroducir("Yes")) 
raiz.bind("<Control-o>", lambda event: menuIncidenciasConsultar("Yes")) # Si en cualquier momento se pulsan las teclas CTRL + O se va al menu de consultar incidencias
raiz.bind("<Control-O>", lambda event: menuIncidenciasConsultar("Yes"))
raiz.bind("<Control-u>", lambda event: cambioUsuario1())                # Si en cualquier momento se pulsan las teclas CTRL + U se va al menu de cambio de usuario
raiz.bind("<Control-U>", lambda event: cambioUsuario1())
raiz.bind("<Control-n>", lambda event: LimpiaElegibles())               # Si en cualquier momento se pulsan las teclas CTRL + N se limpian las celdas de texto
raiz.bind("<Control-N>", lambda event: LimpiaElegibles())
raiz.bind("<Control-l>", lambda event: BotonPrimeroL())                 # Si en cualquier momento se pulsan las teclas CTRL + L se pone el cursor en el primer boton de la lista
raiz.bind("<Control-L>", lambda event: BotonPrimeroL())
raiz.bind("<Control-m>", lambda event: BotonPrimeroM())                 # Si en cualquier momento se pulsan las teclas CTRL + M se pone el cursor en el primer boton del menu
raiz.bind("<Control-M>", lambda event: BotonPrimeroM())
raiz.bind("<Control-plus>", lambda event: TamanyoMas())                 # Si en cualquier momento se pulsan las teclas CTRL + + se aumenta el tamaño de la letra
raiz.bind("<Control-minus>", lambda event: TamanyoMenos())              # Si en cualquier momento se pulsan las teclas CTRL + - se disminuye el tamaño de la letra
raiz.bind("<Control-Return>", lambda event: BotonValidarForzado())      # Si en cualquier momento se pulsan las teclas CTRL + INTRO se fuerza el pulsado del botón VALIDAR
raiz.bind("<Control-p>", lambda event: BotonImprimirForzado())          # Si en cualquier momento se pulsan las teclas CTRL + P se fuerza la impresión de PDF
raiz.bind("<Control-P>", lambda event: BotonImprimirForzado())
raiz.bind("<Control-Up>", lambda event: BotonSubirForzado())            # Si en cualquier momento se pulsan las teclas CTRL + CURSOR ARRIBA se fuerza el pulsado del botón SUBIR
raiz.bind("<Control-Down>", lambda event: BotonBajarForzado())          # Si en cualquier momento se pulsan las teclas CTRL + CURSOR ABAJO se fuerza el pulsado del botón BAJAR
raiz.bind("<Control-Left>", lambda event: BotonRegresarForzado())       # Si en cualquier momento se pulsan las teclas CTRL + CURSOR IZQUIERDA se fuerza el pulsado del botón REGRESAR
raiz.bind("<End>", lambda event: Saliendo())                            # Si en cualquier momento se pulsan las teclas FIN se fuerza el pulsado del botón SALIR
raiz.bind("<Control-d>", lambda event: regresaSinNada())                # Si aquí se pulsan las teclas CTRL + D no pasa nada
raiz.bind("<Control-D>", lambda event: regresaSinNada())
#  ---------------------- Definiendo variables necesarias ---------------------
# Variables sobre ventanas
global ventanaTabla,frameTabla
# Variables de control de usuario
global  DatosUsuario, usuarioReal, usuarioNivel                               
DatosUsuario, usuarioReal, usuarioNivel = (), "No s'ha identificat", "0"    
# Variables de control de menús
global avisoint, EstamosEnIncidencias, EstamosEnRegistros, EstamosEnProforma, EstamosEnBloqueos, EstamosEnProductos, EstamosEnClientes, EstamosEnUsuarios, EstamosEnIntroducir,PrimeraVez                                                                      
avisoint, EstamosEnIncidencias, EstamosEnRegistros, EstamosEnProforma, EstamosEnBloqueos, EstamosEnProductos, EstamosEnClientes, EstamosEnUsuarios, EstamosEnIntroducir,PrimeraVez = True, False, False, False, False, False, False, False, False,True              
# Variable sobre el tamaño de la letra
global TamanyoLetra                 
TamanyoLetra = 0                    
# Variables de control de la base de datos
global origenes, idiomas, horas, fuentes, descripciones, tiposPago, estados, usoUsuarios, productos, productosR, productosS                                                                                                                          
origenes, idiomas, horas, fuentes, descripciones, tiposPago, estados, usoUsuarios, productos, productosR, productosS = "","","","","","","","","","",""                                                                                             
# Variables de control del manejo de los datos de los cuestionarioa
global vr1,vr2,vr3,vr4,vr5,vr6,vr7,vr8,vr9,vr10,vr11,vr12,vr13,vr14                                                                                                                                                                                 
vr1,vr2,vr3,vr4,vr5,vr6,vr7,vr8,vr9,vr10,vr11,vr12,vr13,vr14 = "","","","","","",False,"","","","","","",False                                                                                                                                      
# Variables de control de la fecha    
global fecha, diaGlobal, diaGlobaltk, mesGlobal, mesGlobaltk, anyoGlobal, anyoGlobaltk, diaFecha, mesFecha, anyoFecha                                                                                                                               

fecha = datetime.now()              # Obtenemos la fecha actual
diaGlobal = str(fecha.day)          # Obtenemos el día actual
diaGlobaltk = StringVar()           # Creamos una variable de tipo StringVar para poder usarla en Tkinter
diaGlobaltk.set(diaGlobal)          # Asignamos el valor de la variable diaGlobal a la variable diaGlobaltk 
mesGlobal = str(fecha.month)        # Obtenemos el mes actual
mesGlobaltk = StringVar()           # Creamos una variable de tipo StringVar para poder usarla en Tkinter
mesGlobaltk.set(mesGlobal)          # Asignamos el valor de la variable mesGlobal a la variable mesGlobaltk
anyoGlobal = str(fecha.year)        # Obtenemos el año actual
anyoGlobaltk = StringVar()          # Creamos una variable de tipo StringVar para poder usarla en Tkinter
anyoGlobaltk.set(anyoGlobal)        # Asignamos el valor de la variable anyoGlobal a la variable anyoGlobaltk

stringBusqueda = ""                 # Definimos la variable que vamos a usar para escribir la búsqueda en un combobox

global puntero                      # Definimos las variables que vamos a usar en el sector 3
puntero = 0                         # Definimos el valor del puntero para cuando los listados som más largos que el espacio en pantalla
# ------------------------------------- Ventanas extras -----------------------------------
def ventanaAviso            (texto,color,pausa):                                    # Función que crea la ventana de aviso
    global aviso
    aviso = Tk()                         # Creamos la ventana
    aviso.title(" ")                     # Damos titulo a la ventana
    aviso.geometry("500x250+10+10")      # Damos tamaño a la ventana
    aviso.configure(bg=color)            # Damos color de fondo a la ventana
    aviso.iconbitmap("image/icono.ico")  # Damos icono a la ventana
    aviso.deiconify()                    # Mostramos la ventana
    aviso.config(bd=10)                  # Le da un grosor de borde
    aviso.config(relief="groove")        # Le da un tipo de borde
    avisolabel1=Label(aviso,text="",bg = color)    # Creamos un label vacío
    avisolabel1.pack()                    # Coloca el label en la ventana
    avisolabel2=Label(aviso,text="",bg = color)    # Creamos un label vacío
    avisolabel2.pack()                    # Coloca el label en la ventana
    avisolabel3=Label(aviso,text="",bg = color)    # Creamos un label vacío
    avisolabel3.pack()                    # Coloca el label en la ventana
    avisolabel4=Label(aviso,text="",bg = color)    # Creamos un label vacío
    avisolabel4.pack()                    # Coloca el label en la ventana
    avisolabel5=Label(aviso,text="",bg = color)    # Creamos un label vacío
    avisolabel5.pack()                    # Coloca el label en la ventana
    avisolabel6 = Label(aviso, text = texto,
                       bg = color, fg = "white",
                       font = ("Helvetica", 13))   
    avisolabel6.pack()                    # Coloca el label en la ventana
    aviso.overrideredirect(True)         # Quitamos el marco de la ventana
    aviso.update()                       # Actualiza la ventana       
    time.sleep(pausa)                    # X segundos de pausa
    aviso.destroy()                      # Destruye la ventana 
def ventanaSeleccion        (texto,color,destinoSi):                                # Función que crea la ventana de selección
    global seleccion                                            # Función que crea la ventana de selección
    seleccion = Tk()                                            # Creamos la ventana
    seleccion.title(" ")                                        # Damos titulo a la ventana
    seleccion.geometry("500x250+10+10")                         # Damos tamaño a la ventana
    seleccion.configure(bg=color)                               # Damos color de fondo a la ventana
    seleccion.iconbitmap("image/icono.ico")                     # Damos icono a la ventana
    seleccion.deiconify()                                       # Mostramos la ventana
    seleccion.config(bd=10)                                     # Le da un grosor de borde
    seleccion.config(relief="groove")                           # Le da un tipo de borde
    eti1 = Label(seleccion,text = " ",bg = color)               # Creamos un label vacío
    eti1.pack()                                                 # Coloca el label en la ventana
    eti2 = Label(seleccion,text = " ",bg = color)               # Creamos un label vacío
    eti2.pack()                                                 # Coloca el label en la ventana
    eti3 = Label(seleccion,text = " ",bg = color)               # Creamos un label vacío
    eti3.pack()                                                 # Coloca el label en la ventana
    eti4 = Label(seleccion,text = " ",bg = color)               # Creamos un label vacío
    eti4.pack()                                                 # Coloca el label en la ventana
    aviso = Label(seleccion,text = (texto),
                  anchor = "center",
                  background = color, font = ("Helvetica", 13))     # Creamos un label con el texto
    aviso.pack()                                                # Coloca el label en la ventana
    no_btn = Button(seleccion, text="NO", command=del_no)       # Botón NO
    no_btn.pack()                                               # Coloca el botón en la ventana
    yes_btn = Button(seleccion, text="SI", command=destinoSi)   # Botón SI
    yes_btn.pack()                                              # Coloca el botón en la ventana
    no_btn.focus()                                              # Pone el foco en el botón NO
    seleccion.overrideredirect(True)                            # Quitamos el marco de la ventana
    seleccion.update()                                          # Actualiza la ventana      
    seleccion.mainloop()                                        # Bucle de la ventana
def ventanaTablas           (titulo,tuplaDeFrames):                                 # Función que crea la ventana de tablas
    # globalizamos la ventana
    global ventanaTabla,frameTabla                      
    ventanaTabla = Tk()                         # Creamos la ventana
    ventanaTabla.title(titulo)                  # Le da un titulo a la ventana
    ventanaTabla.configure(bg='green')          # Le da un color de fondo a la ventana
    ventanaTabla.iconbitmap("image/icono.ico")  # Le da un icono a la ventana
    ventanaTabla.geometry("+1+1")             # Le da una posicion a la ventana
    ventanaTabla.config(bd=10)                  # Le da un grosor de borde
    ventanaTabla.config(relief="groove")        # Le da un tipo de borde
    frameTabla = Frame(ventanaTabla)         # Creamos un frame dentro de la ventana
    frames(frameTabla,tuplaDeFrames[0],tuplaDeFrames[1],tuplaDeFrames[2],tuplaDeFrames[3],tuplaDeFrames[4],tuplaDeFrames[5])  # Creamos un frame dentro del frameTabla
    # Si en cualquier momento se pulsan las teclas CTRL + CURSOR IZQUIERDA se fuerza el pulsado del botón REGRESAR
    ventanaTabla.bind("<Control-Left>", lambda event: BotonRegresarForzado())
    # Si en cualquier momento se pulsan las teclas CTRL + P se fuerza la impresión de PDF
    ventanaTabla.bind("<Control-p>", lambda event: BotonImprimirForzado())
    ventanaTabla.bind("<Control-P>", lambda event: BotonImprimirForzado())
    # Importancia en la raiz
    ventanaTabla.deiconify()    # Desiconifica la raiz
    ventanaTabla.iconify() # Iconifica la ventanaTabla
# ---------------------- Funciones sobre errores en los questionarios ---------------------      
def cotejaFecha             (muralla,dia,dialabel,mes,meslabel,anyo,anyolabel):     # Función que comprueba si la fecha introducida es correcta  
    
    if dia.isdigit() == False:      # Si el dia no es un entero
        muralla = True
        LR23.config(text = "Dia no vàlid")
        dialabel.focus()
        return muralla,dia,mes,anyo
    if mes.isdigit() == False:      # Si el mes no es un entero
        muralla = True
        LR23.config(text = "Mes no vàlid")
        meslabel.focus()
        return muralla,dia,mes,anyo
    if anyo.isdigit() == False:     # Si el año no es un entero
        muralla = True
        LR23.config(text = "Any no vàlid")
        anyolabel.focus()
        return muralla,dia,mes,anyo    
    if len(dia) == 1:               # Si el día tiene un solo dígito le añadimos un 0 delante
        dia = "0" + dia    
    if len(mes) == 1:               # Si el mes tiene un solo dígito le añadimos un 0 delante
        mes = "0" + mes
    if len(anyo) == 2:              # Si el año tiene dos dígitos le añadimos un 20 delante
        anyo = "20" + anyo
    if anyo == "" or len(anyo) > 4: # Si el año no tiene 4 dígitos o está vacío        
        LR23.config(text = "Any inexistent")
        anyolabel.focus()
        muralla = True       
    if len(anyo) != 4:              # Si el año no tiene 4 dígitos           
        LR23.config(text = "Any no vàlid")
        anyolabel.focus()
        muralla = True      
    if mes == "":                   # Si el mes está vacío       
        LR23.config(text = "Mes inexistent")
        meslabel.focus()
        muralla = True
    # Si el mes es mayor que 12 o menor que 1
    if int(mes) > 12 or int(mes) < 1 or len(mes) != 2:      
        LR23.config(text = "Mes no vàlid")
        meslabel.focus()
        muralla = True
    if dia == "":                   # Si el día está vacío      
        LR23.config(text = "Dia inexistent")
        dialabel.focus()
        muralla = True
    if int(dia) > 31 or int(dia) < 1:# Si el día es mayor que 31 o menor que 1       
        LR23.config(text = "Dia no vàlid")
        dialabel.focus()
        muralla = True
    return muralla,dia,mes,anyo     # Devolvemos el valor de la variable muralla y la fecha
def cotejaFechaBlock        (muralla,fecha,fechalabel):                             # Función que comprueba si la fecha introducida es correcta
    
    if fecha == "": return muralla,fecha                        # Si la fecha está vacía devolvemos el valor de la variable muralla y la fecha
    if fecha.count("/") != 2:                                   # Si fecha no contiene dos veces "/"
        LR23.config(text = "Format de data incorrecte")
        fechalabel.focus()
        muralla = True
        return muralla,fecha
    if len(fecha[0:fecha.find("/")]) > 2:                       # Si antes de la primera "/" hay más de dos dígitos
        LR23.config(text = "Dia incorrecte")
        fechalabel.focus()
        muralla = True
        return muralla,fecha
    if len(fecha[fecha.find("/")+1:fecha.rfind("/")]) > 2:      # Si entre la primera "/" y la segunda "/" hay más de dos dígitos
        LR23.config(text = "Mes incorrecte")
        fechalabel.focus()
        muralla = True
        return muralla,fecha
    # Si después de la segunda "/" hay más de cuatro dígitos o hay 3 digitos o no hay nada
    if len(fecha[fecha.rfind("/")+1:]) > 4 or len(fecha[fecha.rfind("/")+1:]) == 3 or len(fecha[fecha.rfind("/")+1:]) <= 1:
        LR23.config(text = "Any incorrecte")
        fechalabel.focus()
        muralla = True
        return muralla,fecha
    fecha1 = fecha.replace("/","")                              # Quitamos las "/" de la fecha y comprobamos que sea un número
    if fecha1.isdigit() == False:                               # Si no es un número
        LR23.config(text = "Format de data incorrecte")
        fechalabel.focus()
        muralla = True
        return muralla,fecha
    # Si el día es mayor que 31 o menor que 1
    if int(fecha[0:fecha.find("/")]) > 31 or int(fecha[0:fecha.find("/")]) < 1:
        LR23.config(text = "Dia incorrecte")
        fechalabel.focus()
        muralla = True
        return muralla,fecha
    # Si el mes es mayor que 12 o menor que 1
    if int(fecha[fecha.find("/")+1:fecha.rfind("/")]) > 12 or int(fecha[fecha.find("/")+1:fecha.rfind("/")]) < 1:
        LR23.config(text = "Mes incorrecte")
        fechalabel.focus()
        muralla = True
        return muralla,fecha
    if len(fecha[0:fecha.find("/")]) == 1:                      # Si el dia es un solo dígitos le añadimos un 0 delante
        fecha = "0" + fecha
    if len(fecha[fecha.find("/")+1:fecha.rfind("/")]) == 1:     # Si el mes es un solo dígitos le añadimos un 0 delante
        fecha = fecha[0:fecha.find("/")+1] + "0" + fecha[fecha.find("/")+1:]
    if len(fecha[fecha.rfind("/")+1:]) == 2:                    # Si el año es dos dígitos le añadimos un 20 delante
        fecha = fecha[0:fecha.rfind("/")+1] + "20" + fecha[fecha.rfind("/")+1:]
    return muralla,fecha                                        # Devolvemos el valor de la variable muralla y la fecha
def cotejaFechaEmptyOk      (muralla,dia,dialabel,mes,meslabel,anyo,anyolabel):     # Función que comprueba si la fecha introducida es correcta
    
    if len(dia) == 1:                       # Si el día tiene un solo dígito le añadimos un 0 delante
        dia = "0" + dia
    if len(mes) == 1:                       # Si el mes tiene un solo dígito le añadimos un 0 delante
        mes = "0" + mes
    if len(anyo) == 2:                      # Si el año tiene dos dígitos le añadimos un 20 delante
        anyo = "20" + anyo
    if len(anyo) != 4 and anyo != "":       # Si el año no tiene 4 dígitos y no está vacío          
        LR23.config(text = "Any no vàlid")
        anyolabel.focus()
        muralla = True
    try:                                    # Si el año no es un número
        if (int(mes) > 12 or int(mes) < 1 or len(mes) != 2) and mes != "":            
            LR23.config(text = "Mes no vàlid")
            meslabel.focus()
            muralla = True
    except:                                 # Si el añp sí es un número
        pass   
    try:                                    # Si el día no es un número
        if int(dia) > 31 or int(dia) < 1 and dia != "":
                
            LR23.config(text = "Dia no vàlid")
            dialabel.focus()
            muralla = True
    except:                                 # Si el día sí es un número
        pass    
    return muralla,dia,mes,anyo             # Devolvemos el valor de la variable muralla y la fecha
def cotejaVacio             (muralla,campo,label):                                  # Función que comprueba si el campo está vacío
    
    if campo == "":                                                                 # Si el campo está vacío
        LR23.config(text = "Registre buit")
        label.focus()
        muralla = True
    return muralla                                                                  # Devolvemos el valor de la variable muralla
def cotejaVacioCond1        (muralla,campo1,label,campo2,valor):                    # Función que comprueba si el campo está vacío condicionalmente
    if campo1 == "" and campo2 != valor:                                            # Si el campo está vacío y el campo2 no es igual al valor
        LR23.config(text = "Manca data")
        label.focus()
        muralla = True
    return muralla                                                                  # Devolvemos el valor de la variable muralla
def cotejaCondicional       (campo1,valor1,campo2,valor2):                          # Función que comprueba si el campo es condicional
    if campo2 == valor2:                                                            # Si el campo2 es igual al valor2
        campo1 = valor1
    return campo1                                                                   # Devolvemos el valor de la variable campo1
def cotejaFechaBloqueada    (muralla,dia,hora,label):                               # Función que comprueba si la fecha está bloqueada
       
    conn = sqlite3.connect('databases/basesDeDatosIncidencias.db')                  # Abre la base de datos bd_incidencias
    c = conn.cursor()                                                               # Crea un cursor para la base de datos
    c.execute("SELECT * FROM bd_bloqueos")                                          # Crea una lista con todos los datos de bd_bloqueos
    casos = c.fetchall()                                                            # Guarda los datos en la variable casos
    for row in casos:                                                               # Revisa todos los datos de c por si coinciden con v2
        horasConcretas = []
        activo = False
        for i in horas:
            if i == row[1]:
                activo = True
            if i == row[2]:
                activo = False
            if  activo == True:
                # Añadimos i a la lista de horas concretas
                horasConcretas.append(i)
            
        # Si el dia es igual a la fecha de bloqueo y la hora está entre las horas de la fecha de bloqueo
        if dia == row[0] and hora in horasConcretas:
            # Avisamos de la anomalía y regresamos
            LR23.config(text = "Data bloquejada")
            label.focus()
            muralla = True
            # Cerramos la base de datos
            conn.close()
            return muralla
    conn.close()                                                                    # Cerramos la base de datos
    return muralla                                                                  # Devolvemos el valor de la variable muralla
def cotejaDatosCliente      (cliente,telefono,mail,contacto):                       # Función que comprueba si los datos del cliente son correctos

    base_datos_clientes = sqlite3.connect('databases/basesDeDatosClientes.db')      # Abre la base de datos de clientes
    cursor1 = base_datos_clientes.cursor()                                          # Crea el cursor
    cursor1.execute("SELECT * FROM bd_Clientes WHERE NOM ='"+cliente+"'")           # Busca el cliente 
    clientes = cursor1.fetchall()                                                   # Crea una lista con los datos del cliente
    largo = len(clientes)                                                           # Si cursor1 tiene una sóla linea
    if largo == 1:                                                                  # Si el cliente existe
        if telefono == "":                                                          # Si el telefono está vacío le damos el valor del cliente
            telefono = clientes[0][4]
        if mail == "":                                                              # Si el mail está vacío le damos el valor del cliente
            mail = clientes[0][5]
        if contacto == "":                                                          # Si el contacto está vacío le damos el valor del cliente   
            contacto = clientes[0][7]
    return telefono,mail,contacto                                                   # Devolvemos los datos del cliente
def cotejaDatoCoincidente   (muralla,retorno,mensaje,base,
                             lista,busqueda,label,texto,pausa,id,color):            # Función que comprueba si el campo coincide con alguno dentro de la misama base de datos
    conn = sqlite3.connect(base)                                                    # Abrimos la base de datos de incidencias
    miCursor = conn.cursor()                                                        # Creamos el cursor
    miCursor.execute(busqueda)                                                      # Crea una lista con los datos FECHA y HORA
    casos = miCursor.fetchall()                                                     # Guarda los datos en la variable casos
    cant_casos = len(casos)                                                         # Cuenta cuantos casos hay con la misma fecha y hora
    for caso in casos:                                                              # Busca en casos un caso con el mismo ID que v1
        if caso[-1] == id:
            cant_casos -= 1
    if cant_casos > 0 and mensaje == True:                                          # Si hay más de un caso con la misma fecha y hora
        ventanaAviso(texto,color,pausa)                                             # Avisamos de la anomalía
    if cant_casos > 0 and retorno == True:                                          # Si hay más de un caso con la misma fecha y hora
        muralla = True              
    if label != "":                                                                 # Si la label no está vacía                              
        label.focus()
    return muralla                                                                  # Devolvemos el valor de la variable muralla                               
def cotejaIgualdad          (muralla,campo1,campo2,label):                          # Función que comprueba si el campo1 es igual al campo2
    if campo1 != campo2:                                                            # Si el campo1 es diferente al campo2
        LR23.config(text = "Les claus no coincideixen")                             # Avisamos de la anomalía
        label.focus()                                                               # Ponemos el foco en la label   
        muralla = True                                                              # Ponemos la variable muralla en True
    return muralla                                                                  # Devolvemos el valor de la variable muralla
def cotejaEsNumero          (muralla,campo,label):                                  # Función que comprueba si el campo es un número
    if not campo.isdigit():                                                         # Si campo no es un número
        LR23.config(text = "El camp ha de ser numèric")                             # Avisamos de la anomalía
        label.focus()                                                               # Ponemos el foco en la label
        muralla = True                                                              # Ponemos la variable muralla en True
    return muralla                                                                  # Devolvemos el valor de la variable muralla
def cotejaCaracteres        (muralla,campo,label,*caracteres):                      # Función que comprueba si el campo contiene según qué caracteres
    for caracter in caracteres:                                                     # Para cada caracter en caracteres  
        if caracter in campo:                                                       # Si el caracter está en el campo
            LR23.config(text = "El camp no pot contenir el caracter "+caracter)     # Avisamos de la anomalía
            label.focus()                                                           # Ponemos el foco en la label
            muralla = True                                                          # Ponemos la variable muralla en True
            return muralla                                                          # Devolvemos el valor de la variable muralla
        return muralla                                                              # Devolvemos el valor de la variable muralla
# ------------------------------ Funciones copuy/paste y seguridad ----------------------
def copia                   ():                                                     # Función que copia el contenido de una label o entry al portapapeles
    if raiz.focus_get() == None:    return      # Si no está en ninguna label o entry, no hace nada
    else:                                       # Si está en alguna label o entry, hace lo siguiente
        foco = raiz.focus_get()                 # Descubre en qué label o entry está el foco

        try:                                    # intenta hacer lo siguiente   
            texto = foco.get()                  # Obtiene el contenido de la label o entry
            clipboard.copy(texto)               # Copia el contenido de la label o entry al portapapeles
        except:                                 # Si no puede hacer lo anterior... 
            pass                                # No hace nada
def paste                   ():                                                     # Función que pega el contenido del portapapeles dentro de una label o entry
    if raiz.focus_get() == None:    return      # Si no está en ninguna label o entry, no hace nada                       
    else:                                       # Si está en alguna label o entry, hace lo siguiente
        foco = raiz.focus_get()                 # Descubre en qué label o entry está el foco
        try:                                    # intenta hacer lo siguiente
            foco.insert(INSERT, clipboard_get())# Pega el contenido del portapapeles dentro de la label o entry
        except:                                 # Si no puede hacer lo anterior...
            pass                                # No hace nada
def CopiaSeguridadGlobal    ():
    
    # Ventana de aviso
    ventanaAviso("Fent còpia de seguretat...", "blue", 1)
    fecha = datetime.now()                      # Obtenemos la fecha actual
    # Crea en la carpeta Security una carpeta con nombre fecha y hora actual
    os.mkdir("Security/" + str(anyoGlobal) + "-" + str(mesGlobal) + "-" + str(diaGlobal) + " " + str(fecha.hour) + "-" + str(fecha.minute) + "-" + str(fecha.second))
    # Copia la carpeta databases dentro de esta carpeta
    shutil.copytree("databases", "Security/" + str(anyoGlobal) + "-" + str(mesGlobal) + "-" + str(diaGlobal) + " " + str(fecha.hour) + "-" + str(fecha.minute) + "-" + str(fecha.second) + "/databases")
    # Copia la carpeta files dentro de esta carpeta
    shutil.copytree("files", "Security/" + str(anyoGlobal) + "-" + str(mesGlobal) + "-" + str(diaGlobal) + " " + str(fecha.hour) + "-" + str(fecha.minute) + "-" + str(fecha.second) + "/files")
    
def Saliendo                ():                                                     # Función que se ejecuta al salir de la aplicación  
    
    CopiaSeguridadGlobal()                      # Hacemos una copia de seguridad antes de salir
    raiz.destroy()                              # Cerramos tkinter

def pulsaTeclaCombobox      (event):                                                # Función que se ejecuta al pulsar una tecla en un combobox
    
    global stringBusqueda                       # Creamos global la variable de lo escrito
    lugar = raiz.focus_get()                    # Obtenemos el foco
    letter = event.keysym                        # Obtener la tecla presionada
    if  letter in ["Control_L", "Control_R", "Shift_L", "Shift_R", "Alt_L", "Alt_R"]:
        return                                  # Si es una tecla de control, no hacer nada 
    letter = event.char                         # Obtener la tecla presionada
    # Si la tecla pulsada es espacio o vocal con tilde o letra o número...
    if  event.char.isalpha() or event.char.isdigit() or event.char == " " or event.char in "`,´,',À,È,Ì,Ò,Ù,Á,É,Í,Ú,Ó":        
        stringBusqueda += letter                # Añadir la letra a la cadena de búsqueda
        values = lugar.cget('values')           # Obtener las opciones del combobox
        for value in values:                    # Buscar la primera opción que comience con la cadena de búsqueda
                try:
                    # stringBusqueda, todas en minúsculas
                    stringBusqueda = stringBusqueda.lower()
                except:
                    pass
                # Si la opción comienza con la cadena de búsqueda...
                if value.startswith(stringBusqueda):                   
                    lugar.set(value)            # Seleccionar la opción encontrada y salir del bucle
                    break                       # Salir del bucle
                else:
                    try:
                        # stringbusqueda la primera en mayúsculas
                        stringBusqueda = stringBusqueda[0].upper() + stringBusqueda[1:]
                    except:
                        pass
                    # Si la opción comienza con la cadena de búsqueda...
                    if value.startswith(stringBusqueda):                   
                        lugar.set(value)            # Seleccionar la opción encontrada y salir del bucle
                        break                       # Salir del bucle
                    else:
                        try:
                            # StringBusqueda todo en mayúsculas
                            stringBusqueda = stringBusqueda.upper()
                        except:
                            pass
                        if value.startswith(stringBusqueda):                   
                            lugar.set(value)        # Seleccionar la opción encontrada y salir del bucle
                            break                   # Salir del bucle                                          
    else:                                       # Si no...
        stringBusqueda = ""                     # Vaciar la cadena de búsqueda

def cambiaPasaEncima        (boton, colorEncima, colorFuera):                       # Función que cambia el color del botón cuando el ratón pasa por encima 
    boton.bind("<Enter>", func=lambda e: boton.config(background=colorEncima))
    boton.bind("<Leave>", func=lambda e: boton.config(background=colorFuera)) 
def creaBoton               (boton,frame,texto,comando,fila,columna,colfondo,colletras,altura,ancho,colPasa):
    
    boton = Button(frame, text=texto, command=comando)
    boton.grid(row=fila, column=columna)
    boton.config(bg=colfondo,fg=colletras,  height = altura, width = ancho)
    boton.grid(padx=10, pady=10)
    cambiaPasaEncima(boton,colPasa,colfondo)
def creaLabel               (etiqueta,frame,texto,fila,columna,filaexp,colexp,separax,colfondo,colletra,posicion,tamanyo,tipo):
    
    etiqueta = Label(frame,text=texto,textvariable=texto)
    etiqueta.grid(row=fila, column=columna,rowspan=filaexp,columnspan=colexp)
    etiqueta.config(padx = separax,bg=colfondo,fg=colletra, anchor=posicion, font=("Helvetica", tamanyo, tipo))
    etiqueta.grid(padx=10, pady=10)
def creaEntry               (entrada,frame,textoreferencia,justificacion,fila,columna,colfondo,colletra,ancho,tamanyo):
    
    entrada = Entry(frame,textvariable=textoreferencia,justify = justificacion)
    entrada.grid(row=fila, column=columna)
    entrada.config(bg=colfondo,fg=colletra,  width = ancho, font=("Helvetica", tamanyo))
def ConfiguraColumnas       (frame,cantCol,*valores):
    
    for i in range(cantCol):
        e = valores[i]
        frame.columnconfigure(i,weight = e)     
def ConfiguraFilas          (frame,cantFil,*valores):
    
    for i in range(cantFil):
        e = valores[i]
        frame.rowconfigure(i,weight = e)    
def TamanyoMenos            ():
    
    global TamanyoLetra
    if  TamanyoLetra == 0:
        
        return
    
    TamanyoLetra -= 1  
    RepintaTodoTextoTamanyo()  
def TamanyoMas              ():
    global TamanyoLetra
    if  TamanyoLetra == 15:
        
        return
    
    TamanyoLetra += 1 
    RepintaTodoTextoTamanyo()
def RepintaTodoTextoTamanyo ():
    
    global TamanyoLetra
    tamanyoFont = TamanyoLetra + 15
    textMenu.config(font=("Helvetica", tamanyoFont,"bold"))
    for i in range (1,12):
        globals()["BM" + str(i)].config(font=("Helvetica", tamanyoFont))
    
    tamanyoFont = TamanyoLetra + 10
    for i in range (1,24):
        globals()["LR" + str(i)].config(font=("Helvetica", tamanyoFont))
        globals()['LRR%s' % (i) + '1'].config(font=("Helvetica", tamanyoFont))
        globals()['LRR%s' % (i) + '2'].config(font=("Helvetica", tamanyoFont))
    
    LRR1.config(font=("Helvetica", tamanyoFont))
    LRR5.config(font=("Helvetica", tamanyoFont))
    LRR6.config(font=("Helvetica", tamanyoFont))
    LRR73.config(font=("Helvetica", tamanyoFont))
    LRR213.config(font=("Helvetica", tamanyoFont))
# ------------------------ Funciones sobre las notas----------------------
def bindNotasEvento         (text_widget):
    # Enlazar el evento <FocusIn>
    text_widget.bind("<FocusIn>", lambda event: notasAmpliacion())
    # Enlazar el evento <FocusOut>
    text_widget.bind("<FocusOut>",  lambda event: notasAmpliacion())
def notasAmpliacion         ():
    
    # Si la label LRR213 tiene el foco...
    if frameRellena.focus_get() == LRR213:
        # aMPLIAMOS EL ANCHO DE LRR213
        LRR213.config(width=100)
    else:
        LRR213.config(width=30)
# ------------------------ Funciones sobre la fecha---------------------- 
def DaColorAFecha           (color):
    
    frameFecha.config(bg = color)               # Cambia el color de la label frameFecha
    textFecha.config(bg = color)                # Cambia el color de la label textFecha 
    textBarra1.config(bg = color)               # Cambia el color de la label textBarra1    
    textBarra2.config(bg = color)               # Cambia el color de la label textBarra2
    textSpace.config(bg = color)                # Cambia el color de la label textSpace
def MiraFecha               (uno):
    global PrimeraVez
    # Comprueba si diafecha, mesfecha y anyofecha contienen las fechas del dia de hoy
    if diaFecha.get() == diaGlobal and mesFecha.get() == mesGlobal and anyoFecha.get() == anyoGlobal:
        DaColorAFecha("#b7b493")                                # Cambia el color de la label frameFecha a verde
        PrimeraVez = True                                       # Pone PrimeraVez a True
    else:                                                       # Si no es el dia de hoy
        if frameFecha.cget("bg") != "red":                      # mira si el color de la label frameFecha es rojo
            DaColorAFecha("red")                                # Si no es rojo, lo pone rojo
        else:                                                   # Si es rojo
            DaColorAFecha("yellow")                             # lo pone amarillo
        if uno == True or PrimeraVez == True:                   # Si uno es True o PrimeraVez es True
            frameRellena.after(1000, MiraFecha, True)           # Vuelve a ejecutar la funcion MiraFecha pasado 1 segundo
            PrimeraVez = False                                  # Pone PrimeraVez a False
def FechaActualIncrustada   ():
    
    # Introducimos el valor de la fecha actual en los campos de fecha
    LRR12.insert(0,diaGlobal)
    LRR22.insert(0,mesGlobal)
    LRR32.insert(0,anyoGlobal)
    
    # Colocamos el foco en la siguiente label
    LRR41.focus()
def FechaActualIncrustadaInc():
    
    # Introducimos el valor de la fecha actual en los campos de fecha
    LimpiaElegibles()
    LRR22.insert(0,diaGlobal)
    LRR32.insert(0,mesGlobal)
    LRR42.insert(0,anyoGlobal)
def FechaActualIncrustadaPax():
    
    # Introducimos el valor de la fecha actual en los campos de fecha
    LimpiaElegibles()
    LRR12.insert(0,anyoGlobal)
    LRR22.insert(0,mesGlobal)
def FechaActualIncrustadaGru():
    
    # Introducimos el valor de la fecha actual en los campos de fecha
    LimpiaElegibles()
    LRR12.insert(0,"1")
    LRR22.insert(0,mesGlobal)
    LRR32.insert(0,anyoGlobal)
    LRR42.insert(0,"31")
    LRR52.insert(0,mesGlobal)
    LRR62.insert(0,anyoGlobal)
# ------------------------ Funciones sobre botones----------------------
def ActivaBotonPyFocus      (valor,lineaQ):
    valor.focus()
        
    raiz.bind("<Control-q>", lambda event:  lineaQ())                
    raiz.bind("<Control-Q>", lambda event: lineaQ())        
def BotonPrimeroM           ():
    # Colocamos el foco en la primera label de FrameMenu
    BM1.focus()
def BotonPrimeroL           ():
    # Colocamos el foco en la primera label de FrameRellena
    VIEW0001.focus()             
def BotonPrimeroQ11         ():
    # Colocamos el foco en la primera label de FrameRellena
    LRR11.focus()             
def BotonPrimeroQ12         ():
    # Colocamos el foco en la primera label de FrameRellena
    LRR12.focus()             
def BotonPrimeroQ21         ():
    # Colocamos el foco en la primera label de FrameRellena
    LRR21.focus()             
def BotonPrimeroQ22         ():
    # Colocamos el foco en la primera label de FrameRellena
    LRR22.focus()             
def BotonPrimeroQNada       ():
    # Si pulsamos la tecla Q  no hace nada
    raiz.bind("<Control-q>", lambda event: regresaSinNada())
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())
# ------------------------ Funciones de limpieza y listas----------------------    
def LimpiaElegibles         ():
    
    for i in range(1,24):
    
        globals()['LRR%s' % (i) + '1'].config(state = "readandwrite")
        globals()['LRR%s' % (i) + '1'].delete(first=0,last="end")
        globals()['LRR%s' % (i) + '1'].config(state = "readonly")
        
        globals()['LRR%s' % (i) + '2'].delete(first=0,last="end")
        globals()['LRR%s' % (i) + '2'].config(state = "normal",show="")      

    LRR1.config(text ="")
    LRR5.config(text ="")
    LRR6.config(text ="")
    LRR73.delete(1.0,END)
    LRR213.delete(1.0,END)
def LimpiaLabelsRellena     ():

    for i in range(1,24):
            
        globals()['LR%s' % (i)].config(text = "")
        globals()['LRR%s' % (i) + '1'].grid_forget()
        globals()['LRR%s' % (i) + '2'].grid_forget()
    
    LRR1.grid_forget() 
    LRR5.grid_forget()  
    LRR6.grid_forget()  
    LRR73.grid_forget()  
    LRR213.grid_forget()
    
    LimpiaElegibles()
    borra_datos()
    BB4.config(fg="#27779d", bg="#27779d",command = regresaSinNada)
    BB5.config(fg="#27779d", bg="#27779d", command = regresaSinNada)
    BB6.config(fg="#27779d", bg="#27779d", command = regresaSinNada)
    BB7.config(fg="#27779d", bg="#27779d", command = regresaSinNada)
    
    cambiaPasaEncima(BB4,"grey","#27779d")        
    cambiaPasaEncima(BB5,"grey","#27779d")        
    cambiaPasaEncima(BB6,"grey","#27779d")        
    cambiaPasaEncima(BB7,"grey","#27779d")        
def salirInicio             ():
        
        CopiaSeguridadGlobal()
        # Cierra tkinter
        raiz.destroy()  
def abreLasListas           ():
    
    # --- origenes ---
    global origenes
    origenes = ""
    lista = open("files/ORIGENS.DAT")
    for i in lista:        
        separa = i.split(",")        
        origenes = origenes + separa[0] + ','
    
    origenes = origenes[:-2]
    origenes = list(map(str,origenes.split(',')))
    
    lista.close() 
    
    # --- horas ---
    global horas
    horas = ""
    
    lista = open("files/HORARIS.DAT")
    for i in lista:        
        separa = i.split(",")        
        horas = horas + separa[0] + ','
    
    horas = horas[:-2]
    horas = list(map(str,horas.split('\n,')))
    
    lista.close() 

    # --- idiomas ---
    global idiomas
    idiomas = ""
    
    lista = open("files/IDIOMES.DAT")
    for i in lista:        
        separa = i.split(",")        
        idiomas = idiomas + separa[0] + ','
    
    idiomas = idiomas[:-2]
    idiomas = list(map(str,idiomas.split('\n,')))
    
    lista.close()
        
    # --- descripciones ---
    global descripciones
    descripciones = ""
    
    lista = open("files/DESCRIPCIONS.DAT")
    for i in lista:        
        separa = i.split("\n")        
        descripciones = descripciones + separa[0] + ','
    
    descripciones = descripciones[:-2]
    descripciones = list(map(str,descripciones.split(',')))
    
    lista.close()  
    
    # --- estados ---
    global estados
    estados = ""
    
    lista = open("files/ESTATS.DAT")
    for i in lista:        
        separa = i.split("\n")        
        estados = estados + separa[0] + ','
    
    estados = estados[:-2]
    estados = list(map(str,estados.split(',')))
    
    lista.close()  
    
    # --- fuentes ---
    global fuentes
    fuentes = ""
    
    lista = open("files/FONTS.DAT")
    for i in lista:        
        separa = i.split("\n")        
        fuentes = fuentes + separa[0] + ','
    
    fuentes = fuentes[:-2]
    fuentes = list(map(str,fuentes.split(',')))
    
    lista.close()  
                
    # --- formas de pago ---
    global tiposPago
    tiposPago = ""
    
    lista = open("files/MODES PAGAMENT.DAT")
    for i in lista:        
        separa = i.split("\n")        
        tiposPago = tiposPago + separa[0] + ','
    
    tiposPago = tiposPago[:-1]
    tiposPago = list(map(str,tiposPago.split(',')))
    
    lista.close() 
    
    # --- Productos ---
    global productos
    
    try:
        cursor = sqlite3.connect('databases/basesDeDatosDatos.db').cursor()
        cursor.execute("SELECT NOM FROM bd_productos")
        datos = cursor.fetchall()
        # Crea una lista llamada productos que contiene los nombres de todos los clientes
        productos = []
        for i in datos:
            productos.append(i[0])
            
        # Ordena la lista  
        productos.sort()
        cursor.close()    

    except:
        pass
    # --- Productos registrables---
    global productosR
    
    try:
        cursor = sqlite3.connect('databases/basesDeDatosDatos.db').cursor()
        cursor.execute("SELECT NOM FROM bd_productos WHERE REGISTRABLE = 'Registre'")
        datos = cursor.fetchall()
        # Crea una lista llamada productosR que contiene los nombres de todos los clientes
        productosR = []
        for i in datos:
            productosR.append(i[0])
            
        # Ordena la lista  
        productosR.sort()
        cursor.close()    

    except:
        pass
    # --- Productos stockables---
    global productosS
    
    try:
        cursor = sqlite3.connect('databases/basesDeDatosDatos.db').cursor()
        cursor.execute("SELECT NOM FROM bd_productos WHERE REGISTRABLE = 'Stock'")
        datos = cursor.fetchall()
        # Crea una lista llamada productosS que contiene los nombres de todos los clientes
        productosS = []
        for i in datos:
            productosS.append(i[0])
            
        # Ordena la lista  
        productosS.sort()
        cursor.close()    

    except:
        pass
    # --- Clientes ---  
    global clientes
    
    try:
    
        cursor = sqlite3.connect('databases/basesDeDatosClientes.db').cursor()
        cursor.execute("SELECT NOM FROM bd_clientes")
        datos = cursor.fetchall()
        # Crea una lista llamada clientes que contiene los nombres de todos los clientes
        clientes = []
        for i in datos:
            clientes.append(i[0])
            
        # Ordena la lista        
        clientes.sort()
            
        cursor.close()  
    
    except:
        pass  
      
def cargaUsuario            ():

    # Si no existe ningún usuario, ejecuta la introducción de uno.
    # Crea la base de datos o conecta con ella
    base_datos_datos = sqlite3.connect('databases/basesDeDatosDatos.db')
        
    # Crea el cursor
    cursor = base_datos_datos.cursor()
    
    # Coge el valor del ultimo oid
    cursor.execute("SELECT *, oid FROM bd_usuarios")
    
    try:
        datos = cursor.fetchall()
        dato = datos[-1]
        idAdecuado = dato[7]
        variable_circunstancial = True
    except:
        
        raiz.deiconify()
        menuDatosUsuarioIntroducir()
        textMenu.config(text = "PRIMER USUARI") 
        menusBotones("Tancar",salirInicio)
        variable_circunstancial = False
    
    if variable_circunstancial == False:
        return
        
    raiz.iconify()
    raiz.attributes("-toolwindow", 1)                       # desactivar el botón de maximizar en la barra de título

    rUsuario = Tk()                                         # Crea la ventana para identificar el usuario
    rUsuario.title("Identificació d'usuari")                # Le pone un título
    rUsuario.iconbitmap("image/icono.ico")                  # Le pone un icono
    rUsuario.config(bg="#b7b493")                           # Le da un color de fondo
    rUsuario.config(bd=10)                                  # Le da un grosor de borde
    rUsuario.config(relief="groove")                        # Le da un tipo de borde
    rUsuario.config(width = 300, heigh = 300)               # Le da un tamaño
    rUsuario.deiconify()                                    # La muestra 
    rUsuario.overrideredirect(True)                         # Desactiva la barra de título 
    
    # Si en cualquier momento se pulsan las teclas CTRL + ESC se fuerza el pulsado del botón SALIR 
    rUsuario.bind("<End>", lambda event: salir())   
    # Si en cualquier momento se pulsan las teclas CTRL + INTRO se fuerza el pulsado del botón VALIDAR
    rUsuario.bind("<Control-Return>", lambda event: regreso())

    # --- Usuarios ---  
    global usoUsuarios
    global usuariosO
    usoUsuarios = ""
    
    cursor = sqlite3.connect('databases/basesDeDatosDatos.db').cursor()
    cursor.execute("SELECT NOM FROM bd_usuarios")
    datos = cursor.fetchall()
        
    datos = str(datos)
    separa = datos.split("',), ('")
    separa = str(separa).replace("[('","")
    separa = str(separa).replace("',)]","")
    usoUsuarios = separa
    usoUsuarios = str(usoUsuarios).replace(" '","")
    usoUsuarios = str(usoUsuarios).replace("'","")
    usoUsuarios = str(usoUsuarios).replace(' "',"")
    usoUsuarios = str(usoUsuarios).replace('"',"")
    usoUsuarios = str(usoUsuarios).replace('[',"")
    usoUsuarios = str(usoUsuarios).replace(']',"")
    
    usoUsuarios = list(map(str,usoUsuarios.split(',')))
    usoUsuarios.sort()
    usuariosO = usoUsuarios
    cursor.close()   
    
    def salir():
    
        rUsuario.destroy()
        raiz.destroy()  
              
    def regreso():
        
        global usuarioNivel
        global usuarioReal
        usuarioFinal = CBUsuario.get()
        claveFinal = EClave.get()
        
        if usuarioFinal == "":
            
            LMensaje.config(text = "No s'ha definit cap usuari")
            CBUsuario.focus()
            return
        
        elif claveFinal == "":
            
            LMensaje.config(text = "No s'ha definit cap clau")
            EClave.focus()
            return
        
        else:

            cursor = sqlite3.connect('databases/basesDeDatosDatos.db').cursor()
            cursor.execute("SELECT CLAVE FROM bd_usuarios WHERE (NOM = '" + usuarioFinal+"')")
            datos = cursor.fetchall()
            datos = str(datos).replace("[('","")
            datos = str(datos).replace("',)]","")
            
            if datos == claveFinal:
                
                usuarioReal = usuarioFinal
                cursor.execute("SELECT NIVEL FROM bd_usuarios WHERE (NOM = '" + usuarioFinal+"')")
                datos = cursor.fetchall()
                datos = str(datos).replace("[('","")
                datos = str(datos).replace("',)]","")
                usuarioNivel = datos
                
                cursor.execute("SELECT * FROM bd_usuarios WHERE (NOM = '" + usuarioFinal+"')")
                datos = cursor.fetchall()
                DatosUsuario = datos
                
                rUsuario.destroy()                                      # Destruye la ventana de usuario
                
                raiz.attributes("-toolwindow", 0)                       # Activar el botón de maximizar en la barra de título
                raiz.deiconify()                                        # Para que la ventana se muestre
                nomUsuario.config(text = usuarioReal)                   # Muestra el nombre del usuario en la barra de estado       
                MenuInicial()                                           # Llama a la función que crea el menú inicial
                return(DatosUsuario)                                    # Devuelve los datos del usuario
            
        LMensaje.config(text = "Clau incorrecte")                       # Muestra el mensaje de error 
        EClave.delete(0, END)                                           # Limpia el campo de la clave
        EClave.focus()                                                  # Pone el foco en el campo de la clave            

        return                                                          # Sale de la función
        

    # Botones
    LUsuario = Label(rUsuario,text="Usuari:")
    LUsuario.grid(row=0, column=0,rowspan=1,columnspan=1)
    LUsuario.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor = E, font=("Helvetica", 15,"bold"),width = 15)
    CBUsuario = Combobox(rUsuario,state="readonly")
    CBUsuario.grid(rowspan=1,columnspan=1)
    CBUsuario.config(font=("Helvetica", 15),width = 15)
    CBUsuario.grid(row=0, column=1) 
    CBUsuario['values'] = (usuariosO) 
    CBUsuario.focus()
    
    LClave = Label(rUsuario,text="Clau d'accés:")
    LClave.grid(row=1, column=0,rowspan=1,columnspan=1)
    LClave.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor = E, font=("Helvetica", 15,"bold"),width = 15)
    EClave = Entry(rUsuario,show="*")
    EClave.grid(row=1,column=1,rowspan=1,columnspan=1)
    EClave.config(font=("Helvetica", 15),width = 15)
    
    BValidaUsuario = Button(rUsuario, text="Valida", command=regreso, font=(10))
    BValidaUsuario.grid(row=2, column=0,columnspan=2)
    BValidaUsuario.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 5)
    BValidaUsuario.grid(pady = 2)
    cambiaPasaEncima(BValidaUsuario,"green","#27779d")
    
    BSalir = Button(rUsuario, text="Sortir", command=salir, font=(10))
    BSalir.grid(row=3, column=0,columnspan=2)
    BSalir.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 5)
    BSalir.grid(pady = 2)
    cambiaPasaEncima(BSalir,"green","#27779d")
    
    LMensaje = Label(rUsuario,text="")
    LMensaje.grid(row=4, column=0,rowspan=1,columnspan=2)
    LMensaje.config(padx = 5,bg="#b7b493",fg="red", font=("Helvetica", 18,"bold"),width = 30)

    rUsuario.mainloop()
def regresaSinNada          ():
    
    return 
def regresaSinNada1         (val):
    
    return 
def cambioUsuario           ():
    if  nomUsuario.cget("text") == "":

        return
    global DatosUsuario
    DatosUsuario = ()
    usuarioReal = ""
    nomUsuario.config(text = usuarioReal)
    CopiaSeguridadGlobal()           
    cargaUsuario()

def BotonValidarForzado     ():
    
    BB4.invoke()
def BotonImprimirForzado    ():
    
    BB7.invoke()
def BotonSubirForzado       ():
    BB4.focus()
    BB5.invoke()
def BotonBajarForzado       ():

    BB4.focus()    
    BB6.invoke()     
def BotonRegresarForzado    ():
    
    BM11.invoke()        

def Boton4activado          (Destino,subdestino):
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10, command = lambda: Destino(subdestino))
    cambiaPasaEncima(BB4,"green","#27779d")
def Boton4activado2         (Destino):
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10, command = Destino)
    cambiaPasaEncima(BB4,"green","#27779d")      
def Boton5activado          (Destino,subdestino):
    
    BB5.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 5, command = lambda: Destino(subdestino))
    cambiaPasaEncima(BB5,"green","#27779d") 
def Boton6activado          (Destino):
    
    BB6.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 5, command = Destino)
    cambiaPasaEncima(BB6,"green","#27779d")
def Boton7activado          (Destino):
    
    BB7.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10, command = Destino)
    cambiaPasaEncima(BB7,"green","#27779d")              
        
def crea_espacios_info      (frame,a,b):
                 
    for dato in range(a):
        
        for data in range(b):
            num = "0" + str(dato) + "0" + str(data)
            listalistados = ["0001","0002","0003","0004","0005","0006","0007","0008","0009","00010","00011","00012","00013","00014","00015","00016","00017","00018","00019","00020","00021"]
            if dato == 0 and data != 0:

                globals()['VIEW%s' % num] = Button(frame, text="",bg="#b7b493", fg="#293337",width = 10, height = 1)
                globals()['VIEW%s' % num].grid(row=data+1,column=dato)
                if data>1: 
                    globals()['VIEW%s' % num].bind("<Up>", lambda event, data=data: globals()['VIEW%s' % (listalistados[data-2])].focus_set())
                if data<21:
                    globals()['VIEW%s' % num].bind("<Down>", lambda event, data=data: globals()['VIEW%s' % (listalistados[data])].focus_set())                      
            else:
        
                globals()['VIEW%s' % num] = Label(frame, text="",bg="#b7b493", fg="#293337",width = 10, height = 1)
                globals()['VIEW%s' % num].grid(row=data+1,column=dato)
                # jUSTIFICA A LA IZQUIERDA
                globals()['VIEW%s' % num].config(anchor = W)
            
    columna = 0
    for dato in range (a):
        
        num = "0" + str(columna) + "00"
        globals()['VIEW%s' % num].config(text = "                    ",bg = "#5d5b45",fg = "#FFFFFF")
        columna += 1  
    ConfiguraColumnas(frameLista,1,1,1,1,1,1,1,1,1,1)  
def destruye_espacios_info  (a,b):
                 
    for dato in range(a):
        
        for data in range(b):
            
            num = "0" + str(dato) + "0" + str(data)
        
            globals()['VIEW%s' % num].destroy()
def ajusta_espacios_info    (a,b,*ancho):
                 
    for dato in range(a):
        
        for data in range(b):
            
            num = "0" + str(dato) + "0" + str(data)
        
            globals()['VIEW%s' % num].config(width = ancho[dato])

def borra_datos             ():
                  
    for dato in range(10):
        
        for data in range(22):
            
            num = "0" + str(dato) + "0" + str(data)
            
            globals()['VIEW%s' % num].config(text = "                              ")            
def menusBotones            (texto11="",enlace11=regresaSinNada,
                             texto1="",enlace1=regresaSinNada,
                             texto2="",enlace2=regresaSinNada,
                             texto3="",enlace3=regresaSinNada,
                             texto4="",enlace4=regresaSinNada,
                             texto5="",enlace5=regresaSinNada,
                             texto6="",enlace6=regresaSinNada,
                             texto7="",enlace7=regresaSinNada,
                             texto8="",enlace8=regresaSinNada,
                             texto9="",enlace9=regresaSinNada,
                             texto10="",enlace10=regresaSinNada,
                             texto12="",enlace12=regresaSinNada,
                             texto0="",enlace0=regresaSinNada
                             ):
    
    botones = [
        {'texto': texto1, 'enlace': enlace1},
        {'texto': texto2, 'enlace': enlace2},
        {'texto': texto3, 'enlace': enlace3},   
        {'texto': texto4, 'enlace': enlace4},    
        {'texto': texto5, 'enlace': enlace5},    
        {'texto': texto6, 'enlace': enlace6},    
        {'texto': texto7, 'enlace': enlace7},    
        {'texto': texto8, 'enlace': enlace8},    
        {'texto': texto9, 'enlace': enlace9},    
        {'texto': texto10, 'enlace': enlace10},
        {'texto': texto11, 'enlace': enlace11},
        {'texto': texto12, 'enlace': enlace12}
        ]

    for i, boton in enumerate(botones):
        texto = boton['texto']
        enlace = boton['enlace']
        if texto == "":
            globals()['BM%s' % (i+1)].config(text = " ",bg = "#b7b493",command = regresaSinNada,relief='flat')
            cambiaPasaEncima(globals()['BM%s' % (i+1)],"#b7b493","#b7b493")
            # Cambia el color del botón cuando está enfocado
            globals()['BM%s' % (i+1)].bind("<FocusIn>", lambda event, i=i: globals()['BM%s' % (i+1)].config(bg="#b7b493"))
            # Devuelve el color original si el botón no está enfocado
            globals()['BM%s' % (i+1)].bind("<FocusOut>", lambda event, i=i: globals()['BM%s' % (i+1)].config(bg="#b7b493"))
            globals()['BM%s' % (i+1)].config(takefocus = False)
        else:
            globals()['BM%s' % (i+1)].config(text = texto,bg = "#27779d",command = enlace,relief='groove')
            cambiaPasaEncima(globals()['BM%s' % (i+1)],"green","#27779d")
            # Cambia el color del botón cuando está enfocado
            globals()['BM%s' % (i+1)].bind("<FocusIn>", lambda event, i=i: globals()['BM%s' % (i+1)].config(bg="#87779d"))
            # Devuelve el color original si el botón no está enfocado
            globals()['BM%s' % (i+1)].bind("<FocusOut>", lambda event, i=i: globals()['BM%s' % (i+1)].config(bg="#27779d"))
            globals()['BM%s' % (i+1)].config(takefocus = True)
        BM0.config(text = " ",bg = "#b7b493",command = regresaSinNada,relief='flat')
        cambiaPasaEncima(BM0,"#b7b493","#b7b493")

def OpcionesQuestionario    (*opciones):
    
    linea = 0
    # Revisamos todas las opciones
    for opcion in opciones:
        opcion[1].config(text = opcion[2])
        opcion[3].grid(row=linea,column=1)
        
        if opcion[0] == "1":    
            opcion[3].config(text = opcion[4])
        
        elif opcion[0] == "X1":
            opcion[3]['values'] = opcion[4]
            try:
                if opcion[5] != False and opcion[7] != False:
                    opcion[3].bind('<Key>', opcion[5])
            except:
                pass
            try:
                opcion[3].config(state = opcion[6])
            except:
                pass
        
        linea += 1
def query_todos             (archivo,seleccion,column,variableTrue,*datosAlQuery):
    

    global EstamosEnRegistros,EstamosEnIncidencias,EstamosEnProforma,EstamosEnBloqueos,EstamosEnProduto,EstamosEnClientes,EstamosEnProductos,EstamosEnClientes,EstamosEnUsuarios, EstamosEnIntroducir 
    
   # Creamos la base de datos o conectamos con una
    base_datos = sqlite3.connect(archivo)
    busqueda = seleccion
    columnas = column
    global puntero
    if EstamosEnIntroducir == True:
        puntero = 0
    globals()[variableTrue] = True
    query(base_datos,busqueda,columnas,*datosAlQuery)    
def prequery_todos          (funcion):
    global puntero
    if puntero <= 0:
        puntero = 0
        funcion()
        return
    else:
        puntero -= 42
        funcion()
def query_todos_busca0      (funcion):
    
    global puntero
    puntero = 0
    funcion()
def Le_Bd_Se_todos          (base_datos):
    LimpiaElegibles     ()                                              # Limpia los campos de texto
    base_datos.commit   ()	                                            # Asegura los cambios
    base_datos.close    ()	                                            # Cierra la conexión
    seleccion.destroy   ()                                              # Destruye la ventana de aviso
                   
def query_registros_busca   ():
    
    global EstamosEnRegistros
    
    # Rescata valores
    v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11 = LRR12.get(),LRR22.get(),LRR32.get(),LRR12.get()+"/"+LRR22.get()+"/"+LRR32.get(),LRR41.get(),LRR51.get(),LRR61.get(),LRR71.get(),LRR81.get(),LRR91.get(),LRR101.get()
    
    # Coteja fallos
    muralla = False
    muralla,v1,v2,v3 = cotejaFechaEmptyOk(muralla,v1,LRR12,v2,LRR22,v3,LRR32)
    if muralla == True: 
        LR23.config(fg = "red")         # Pintamos de rojo el campo LR23
        return 
       
    # Salva datos       
    # Creamos la base de datos o conectamos con una
    query_todos('databases/basesDeDatosRegistros.db',
                "SELECT *, oid FROM bd_registros WHERE ((FECHA LIKE '" + v3 + "/%' or '" + v3 + "' = '') AND (FECHA LIKE '%/" + v2 + "/%' or '" + v2 + "' = '') AND (FECHA LIKE '%/" + v1 + "' or '" + v1 + "' = '') AND (USUARIO = '" + v11 + "' or '" + v11 + "' = '') AND (DESCRIPCION = '" + v5 + "' or '" + v5 + "' = '') AND (ORIGEN = '" + v6 + "' or '" + v6 + "' = '') AND (HORA >= '" + v7 + "' or '" + v7 + "' = '')  AND (HORA <= '" + v8 + "' or '" + v8 + "' = '')  AND (PRODUCTO = '" + v9 + "' or '" + v9 + "' = '')   AND (FUENTE = '" + v10 + "' or '" + v10 + "' = '')) ORDER BY FECHA",
                8,
                "EstamosEnRegistros",
                "ID","","DATA","DESCRIPCIÓ","ORIGEN","HORA","PRODUCTE","FONT","")
def registroCorrigeUno      ():

    global val1,val2,diaGlobal,mesGlobal,anyoGlobal
    val1,val2,diaGlobal,mesGlobal,AnyoGlobal = LRR12.get(),usuarioReal,diaGlobaltk.get(),mesGlobaltk.get(),anyoGlobaltk.get()

    if  val1 == "":
        return
                       
    LimpiaElegibles                                                     # Limpia las cajas
    base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')	# Crea una base de datos o se conecta a una
    c = base_datos.cursor()	                                            # Crea cursor   
    c.execute("SELECT * FROM bd_registros WHERE oid = " + val1)	        # Query the database
    records = c.fetchall()                                              # Devuelve una lista de tuplas   
    menuRegistrosIntroducir()                                           # Llama a la función que crea la ventana de introducir registros
      
    global descripcion,origen,hora,producto,fuente,notas,val6           # Creando las variables globales

    # Loop para volcar los resultados
    for record in records:
        notillas = record[7]
        notillas = notillas.rstrip()
              
        LRR1.config(text = val1)
        LRR21.config(state = "readandwrite")
        LRR21.insert(0,record[2])
        LRR21.config(state = "readonly")
        LRR31.config(state = "readandwrite")
        LRR31.insert(0,record[3])
        LRR41.config(state = "readandwrite")
        LRR41.insert(0,record[4])
        LRR41.config(state = "readonly")
        LRR51.config(state = "readandwrite")
        LRR51.insert(0,record[5])
        LRR51.config(state = "readonly")
        LRR61.config(state = "readandwrite")
        LRR61.insert(0,record[6])
        LRR61.config(state = "readonly")
        LRR73.config(state = NORMAL)
        LRR73.insert(1.0,notillas+" - "+usuarioReal+" fa canvis el "+diaGlobal+"/"+mesGlobal+"/"+anyoGlobal+": ")
        nomUsuario.config(text = record[0])
        val6 =record[1]
        val7 = []
        for t in val6.split("/"):
            val7.append(t)
        anyoGlobaltk.set(val7[0])
        mesGlobaltk.set(val7[1])
        diaGlobaltk.set(val7[2])
        diaFecha.config(text = diaGlobaltk)
        mesFecha.config(text = mesGlobaltk)
        anyoFecha.config(text = anyoGlobaltk)
        MiraFecha(anyoFecha)
        
    LRR21.focus()                                                       # Centramos el cursor
    Boton4activado2(RegistroSalvaCorreccion)                            # Activa el botón de guardar
def RegistroSalvaCorreccion ():
    
    global origenes,usuarioReal,diaGlobal,mesGlobal,anyoGlobal
    
    # Rescata valores
    v1,v2,v3,v4,v5,v6,v7,v8,v9 = LRR21.get(),LRR31.get(),LRR41.get(),LRR51.get(),LRR61.get(),LRR73.get(1.0,END),anyoGlobaltk.get(),mesGlobaltk.get(),diaGlobaltk.get()
                        
    # Coteja fallos
    muralla = False
    muralla = cotejaVacio(muralla,v5,LRR61)
    muralla = cotejaVacio(muralla,v4,LRR51)
    muralla = cotejaVacio(muralla,v3,LRR41)
    muralla = cotejaVacio(muralla,v2,LRR31)
    muralla = cotejaVacio(muralla,v1,LRR21)
    muralla,v9,v8,v7 = cotejaFecha(muralla,v9,diaFecha,v8,mesFecha,v7,anyoFecha)
    if muralla == True: 
        LR23.config(fg = "red")         # Pintamos de rojo el campo LR23
        return        
    base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')      # Crea una base de datos o abre la existente 
    c = base_datos.cursor()                                                 # Conecta el cursor

    c.execute("""UPDATE bd_registros SET
              USUARIO = :usuario,
              FECHA = :fecha,
              DESCRIPCION = :descripcion,
              ORIGEN = :origen,
              HORA = :hora,
              PRODUCTO = :producto,
              FUENTE = :fuente,
              NOTAS = :notas
                            
              WHERE oid = :val1""",
              {
              'usuario': nomUsuario.cget("text"),
              'fecha': v7 + "/" + v8 + "/" + v9,
              'descripcion': LRR21.get(),
              'origen': LRR31.get(),
              'hora': LRR41.get(),
              'producto': LRR51.get(),
              'fuente': LRR61.get(),
              'notas': LRR73.get(1.0,END),
              'val1': val1
                  })
    
    base_datos.commit()                 #Asegura los cambios
    base_datos.close()  	            # Cierra la conexión 
    nomUsuario.config(text = val2)      # Vuelve a pintar usuario y fecha

    anyoGlobaltk.set(anyoGlobal)        # Recupera en las variables tk los datos de fecha salvados en diaGlobal, mesGlobal y anyoGlobal
    mesGlobaltk.set(mesGlobal)
    diaGlobaltk.set(diaGlobal)
    diaFecha.config(text = diaGlobaltk) # Los vuelca a los labels
    mesFecha.config(text = mesGlobaltk)
    anyoFecha.config(text = anyoGlobaltk)
    MiraFecha(anyoFecha)
    menuRegistroCorregir()	            # Vuelve hacia atrás
def registroBorraUno        ():

    # Creamos la base de datos o conectamos con una
    base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
    busqueda = "SELECT *, oid FROM bd_registros WHERE (oid = '" + LRR12.get() + "')"
    columnas = 8
    global puntero
    query(base_datos,busqueda,columnas,"ID","","DATA","DESCRIPCIÓ","ORIGEN","HORA","PRODUCTE","FONT","")
    
    val1 = LRR12.get()          # Recoge el valor del id
    if val1 == "":  return      # si no ha puesto ningún id, no hará nada

    # Ventana de aviso
    ventanaSeleccion("Aixó esborrarà el registre amb id "+ val1 +", si existeix.","red",del_register_yes)
def del_register_yes        ():

    base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')  # Creamos base de datos o conectamos a una 
    c = base_datos.cursor()	                                            # Creamos el cursor
    c.execute("DELETE from bd_registros WHERE oid = " + LRR12.get())	# Borra el registro
    Le_Bd_Se_todos(base_datos)                                          # Acciones comunes
    # Borramos los datos del listado de registros
    query_todos('databases/basesDeDatosRegistros.db',
                "SELECT *, oid FROM bd_registros ORDER BY oid DESC",
                8,
                "EstamosEnRegistros",
                "ID","","DATA","DESCRIPCIÓ","ORIGEN","HORA","PRODUCTE","FONT","")
    LRR12.focus()                                                       # Foco

def query_incidencias_busca ():
    
    global EstamosEnIncidencias
    v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14 = LRR11.get(),LRR22.get(),LRR32.get(),LRR42.get(),LRR51.get(),LRR61.get(),LRR71.get(),LRR82.get(),LRR92.get(),LRR102.get(),LRR112.get(),LRR121.get(),LRR131.get(),LRR142.get()
    
    muralla = False
    muralla,v2,v3,v4 = cotejaFechaEmptyOk(muralla,v2,LRR22,v3,LRR32,v4,LRR42)
    muralla,v8,v9,v10 = cotejaFechaEmptyOk(muralla,v8,LRR82,v9,LRR92,v10,LRR102)
    if muralla == True:
        LR23.config(fg = "red")         # Pintamos de rojo el campo LR23
        return
    # Creamos la base de datos o conectamos con una
    query_todos('databases/basesDeDatosIncidencias.db',
                "SELECT *, oid FROM bd_incidencias WHERE ((CLIENTE = '" + v1 + "' or '" + v1 + "' = '') AND (FECHA LIKE '" + v2 + "/%' or '" + v2 + "' = '') AND (FECHA LIKE '%/" + v3 + "/%' or '" + v3 + "' = '') AND (FECHA LIKE '%/" + v4 + "' or '" + v4 + "' = '') AND (PRODUCTO = '" + v5 + "' or '" + v5 + "' = '') AND (IDIOMA = '" + v6 + "' or '" + v6 + "' = '') AND (AGENDADO = '" + v7 + "' or '" + v7 + "' = '') AND (FECHA_REV LIKE '" + v8 + "/%' or '" + v8 + "' = '') AND (FECHA_REV LIKE '%/" + v9 + "/%' or '" + v9 + "' = '')  AND (FECHA_REV LIKE '%/" + v10 + "' or '" + v10 + "' = '') AND (ESTADO = '" + v12 + "' or '" + v12 + "' = '') AND (NOTAS = '" + v11 + "' or '" + v11 + "' = '') AND (PAGAT = '" + v13 + "' OR '" + v13 + "' = '') AND (MAIL_EXTRA = '" + v14 + "' OR '" + v14 + "' = '')) ORDER BY FECHA, HORA",
                8,
                "EstamosEnIncidencias",
                "ID","DATA","HORA","PAX","PRODUCTE","IDIOMA","ESTAT","CLIENT","PAGAT")
def incidenciasCorrigeUno   ():

    global val1, val2, diaGlobal, mesGlobal, anyoGlobal, usuarioNivel
    val1,val2,diaGlobal,mesGlobal,anyoGlobal = LRR12.get(),usuarioReal,diaGlobaltk.get(),mesGlobaltk.get(),anyoGlobaltk.get()

    if  val1 == "":        return                                           # Si no hay nada en el campo ID, no hacemos nada
                       
    LimpiaElegibles                                                         # Limpia las cajas
    base_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')	# Crea una base de datos o se conecta a una
    c = base_datos.cursor()	                                                # Crea cursor
    c.execute("SELECT * FROM bd_incidencias WHERE oid = " + val1)	        # Query the database
    records = c.fetchall()                                                  # Obtenemos los resultados del query
    menuIncidenciasIntroducir()                                             # Llamamos a la función que crea la ventana de introducción de datos
      
    # Creando las variables globales
    global  fecha,hora,pax1,pax2,producto,idioma,tel_extra,estado,usuario,fecha_cre,cliente,mail_extra,precio1,tipo1,precio2,tipo2,agendado,fecha_rev,pagat,notas,factura,val6
      
    # Loop para volcar los resultados    
    for record in records:
        notillas = record[20]
        notillas = notillas.rstrip()
              
        LRR1.config(text = val1)
        LRR22.insert(0,record[0])
        LRR31.config(state = "readandwrite")
        LRR31.insert(0,record[10])
        LRR42.insert(0,record[6])
        LRR52.insert(0,record[11])
        LRR61.config(state = "readandwrite")
        LRR61.insert(0,record[1])
        LRR61.config(state = "readonly")
        LRR72.insert(0,record[2])
        LRR82.insert(0,record[12])
        LRR92.insert(0,record[13])
        LRR102.insert(0,record[3])
        LRR112.insert(0,record[14])
        LRR122.insert(0,record[15])
        LRR131.config(state = "readandwrite")
        LRR131.insert(0,record[4])
        LRR131.config(state = "readonly")
        LRR141.config(state = "readandwrite")
        LRR141.insert(0,record[5])
        LRR141.config(state = "readonly")
        LRR152.insert(0,record[21])
        LRR161.config(state = "readandwrite")
        LRR161.insert(0,record[16])
        LRR161.config(state = "readonly")
        LRR172.insert(0,record[17])
        LRR181.config(state = "readandwrite")
        LRR181.insert(0,record[18])
        LRR181.config(state = "readonly")        
        LRR192.insert(0,record[19])
        LRR201.config(state = "readandwrite")
        LRR201.insert(0,record[7])
        LRR201.config(state = "readonly")                
        LRR213.config(state = NORMAL)
        LRR213.insert(1.0,notillas+"\n"+usuarioReal+" fa canvis el "+diaGlobal+"/"+mesGlobal+"/"+anyoGlobal+": ")

        nomUsuario.config(text = record[8])
        val6 =record[9]
        val7 = []
        for t in val6.split("/"):
            val7.append(t)
        anyoGlobaltk.set(val7[0])
        mesGlobaltk.set(val7[1])
        diaGlobaltk.set(val7[2])
        diaFecha.config(text = diaGlobaltk)
        mesFecha.config(text = mesGlobaltk)
        anyoFecha.config(text = anyoGlobaltk)
        MiraFecha(anyoFecha)

    # Centramos el cursor
    LRR21.focus()    
    if int(usuarioNivel) >=3:
        LRR22.configure(state = "readonly")
        LRR31.config(state = "disabled")
        LRR42.config(state = "readonly")
        LRR52.config(state = "readonly")
        LRR61.config(state = "disabled")
        LRR72.config(state = "readonly")
        LRR82.config(state = "readonly")
        LRR92.config(state = "readonly")
        LRR102.config(state = "readonly")
        LRR112.config(state = "readonly")
        LRR122.config(state = "readonly")
        LRR131.config(state = "disabled")
        LRR141.config(state = "disabled")
        LRR152.config(state = "readonly")
        LRR161.config(state = "disabled")
        LRR172.config(state = "readonly")
        LRR181.config(state = "disabled")
        LRR192.config(state = "readonly")
        LRR201.focus()
            
    Boton4activado2(IncidenciasSalvaCorrecc)
def IncidenciasSalvaCorrecc ():
    
    global origenes,usuarioReal,diaGlobal,mesGlobal,anyoGlobal                  # Variables globales
    
    # Rescata valores
    v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22 = LR1.cget("text"),LRR22.get(),LRR31.get(),LRR42.get(),LRR52.get(),LRR61.get(),LRR72.get(),LRR82.get(),LRR92.get(),LRR102.get(),LRR112.get(),LRR122.get(),LRR131.get(),LRR141.get(),LRR152.get(),LRR161.get(),LRR172.get(),LRR181.get(),LRR213.get(1.0,END),LRR201.get(),LRR192.get(),anyoGlobaltk.get()+"/"+mesGlobaltk.get()+"/"+diaGlobaltk.get()

    muralla = False
    muralla     = cotejaVacio(muralla,v20,LRR201)                               # Comprueba que el campo no esté vacío
    muralla,v17 = cotejaFechaBlock(muralla,v17,LRR172)                          # Comprueba que la fecha no esté bloqueada
    muralla,v2  = cotejaFechaBlock(muralla,v2,LRR22)                            # Comprueba que la fecha no esté bloqueada
    v2          = cotejaCondicional(v2,"Per definir",v20,"Pendent gaudir")      # Si el campo v20 es "Pendent gaudir" el campo v2 es "Per definir"
    muralla     = cotejaVacioCond1(muralla,v2,LRR22,v20,"Pendent gaudir")       # Si el campo v20 no es "Pendent gaudir" el campo v2 no puede estar vacío
    muralla     = cotejaFechaBloqueada(muralla,v2,v6,LRR22)                     # Comprueba que la fecha no esté bloqueada
    v4,v5,v15   = cotejaDatosCliente(v3,v4,v5,v15)                              # Comprueba si hay que aprovechar datos del cliente
    # Comprueba que no exista una incidencia con los mismos datos
    if muralla == False:
        muralla     = cotejaDatoCoincidente(muralla,False,True,
                                            'databases/basesDeDatosIncidencias.db',
                                            'bd_incidencias',
                                            "SELECT *,oid FROM bd_incidencias WHERE ((FECHA = '" + v2 + "') AND (HORA = '" + v6+ "'))","",
                                            "¡¡ATENCIÓ!! Ja existeix una altra incidència amb aquesta data i hora",3,v1,"red")          
                                                
    base_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')            # Crea una base de datos o abre la existente
    c = base_datos.cursor()                                                         # Conecta el cursor
    c.execute("""UPDATE bd_incidencias SET
            FECHA           = :fecha,
            HORA            = :hora,
            PAX1            = :pax1,
            PAX2            = :pax2,
            PRODUCTO        = :producto,
            IDIOMA          = :idioma,
            TEL_EXTRA       = :tel_extra,
            ESTADO          = :estado,
            USUARIO         = :usuario,
            FECHA_CREA      = :fecha_crea,
            CLIENTE         = :cliente,
            MAIL_EXTRA      = :mail_extra,
            PRECIO1         = :precio1,
            TIPO1           = :tipo1,
            PRECIO2         = :precio2,
            TIPO2           = :tipo2,
            CONTACTO        = :contacto,
            AGENDADO        = :agendado,
            FECHA_REV       = :fecha_rev,
            PAGAT           = :pagat,
            NOTAS           = :notas,
            FACTURA         = :factura
                            
            WHERE oid = :val1""",
              {
                'fecha':    v2,
                'hora':     v6,
                'pax1':     v7,
                'pax2':     v10,
                'producto': v13,
                'idioma':   v14,
                'tel_extra': v4,
                'estado':   v20,
                'usuario':  nomUsuario.cget("text"),
                'fecha_crea': v22,
                'cliente':  v3,
                'mail_extra': v5,
                'precio1':  v8,
                'tipo1' :   v9,
                'precio2':  v11,
                'tipo2':    v12,
                'contacto': v15,
                'agendado': v16,
                'fecha_rev': v17,
                'pagat':    v18,
                'notas' :   v21,
                'factura':  v19,
                'val1':     val1
                  })
    
    base_datos.commit()                                                             #Asegura los cambios
    base_datos.close()  	                                                        # Cierra la conexión
    nomUsuario.config(text = val2)                                                  # Vuelve a pintar usuario y fecha
    anyoGlobaltk.set(anyoGlobal)                                                    # Recupera en las variables tk los datos de fecha salvados en diaGlobal, mesGlobal y anyoGlobal
    mesGlobaltk.set(mesGlobal)
    diaGlobaltk.set(diaGlobal)
    diaFecha.config(text = diaGlobaltk)                                             # Los vuelca a los labels
    mesFecha.config(text = mesGlobaltk)
    anyoFecha.config(text = anyoGlobaltk)
    MiraFecha(anyoFecha)
    menuIncidenciasCorregir()	                                                    # Vuelve hacia atrás
def incidenciasBorraUno     ():

    # Creamos la base de datos o conectamos con una
    base_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')
    busqueda = "SELECT *, oid FROM bd_incidencias WHERE (oid = '" + LRR12.get() + "')"
    columnas = 8
    global puntero
    query(base_datos,busqueda,columnas,"ID","DATA","HORA","PAX","PRODUCTE","IDIOMA","ESTAT","CLIENT","PAGAT")
    
    val1 = LRR12.get()

    # si no ha puesto ningún id, no hará nada
    if val1 == "":  return
    
    # Ventana de aviso
    ventanaSeleccion("Aixó esborrarà la incidència amb id "+ val1 +", si existeix.","red",del_incidence_yes)
def del_incidence_yes       ():

    base_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')# Creamos base de datos o conectamos a una    
    c = base_datos.cursor()	                                            # Creamos el cursor
    c.execute("DELETE from bd_incidencias WHERE oid = " + LRR12.get())	# Borra el registro
    LimpiaElegibles()                                                   # Limpia las cajas
    base_datos.commit()	                                                # Asegura los cambios
    base_datos.close()	                                                # Cierra la conexión 
    seleccion.destroy()                                                 # Cierra la ventana de aviso
    Le_Bd_Se_todos(base_datos)                                          # Acciones comunes
    # Borramos los datos del listado de registros
    query_todos('databases/basesDeDatosIncidencias.db',
                "SELECT *, oid FROM bd_incidencias ORDER BY oid DESC",
                8,
                "EstamosEnIncidencias",
                "ID","DATA","HORA","PAX","PRODUCTE","IDIOMA","ESTAT","CLIENT","PAGAT")         
    LRR12.focus()                                                       # Foco

def ProformaProduceUno      ():
    
    global VieneDeIncGrups                                              # Variable global que indica si viene de incidencias o de grupos
    VieneDeIncGrups = LRR12.get()                                       # Recupera el id de la incidencia o grupo
    global val1                                                         # Variable global que recupera el id de la incidencia o grupo
    val1 = LRR12.get()                                                  # Recupera el id de la incidencia o grupo
    if  val1 == "": return                                              # Si no ha puesto ningún id, no hará nada               
    LimpiaElegibles                                                     # Limpia las cajas   
    base_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')# Crea una base de datos o se conecta a una
    c = base_datos.cursor()	                                            # Crea cursor
    c.execute("SELECT * FROM bd_incidencias WHERE oid = " + val1)	    # Query the database
    records = c.fetchall()                                              # Recupera los resultados
    base_datos.close()                                                  # Cerramos incidencias
    menuIncidenciasFacturaProformaIntroducirCrear()                     # Vuelve hacia atrás
    # Creando las variables globales
    global  fecha,fechaPro,NumPro,Cliente,Cant1,concept1,Precio1,Cant2,Concept2,Precio2,Iva,TipoIva,IncluidoIva,IdIncidencia     
    # Loop para volcar los resultados    
    for record in records:
             
        LRR1.config(text = val1)
        LRR31.config(state = "readandwrite")
        LRR31.insert(0,record[10])
        LRR42.insert(0,record[0])
        LRR52.insert(0,record[2])
        LRR62.insert(0,record[13])
        LRR72.insert(0,record[12])
        LRR82.insert(0,record[3])
        LRR92.insert(0,record[15])
        LRR102.insert(0,record[14])    
    LRR22.focus()                                                       # Centramos el cursor 
def ProformaClonaUno        ():                         
        
    global VieneDeIncGrups                                              # Variable global que indica si viene de incidencias o de grupos
    VieneDeIncGrups = LRR12.get()                                       # Recupera el id de la incidencia o grupo
    global val1                                                         # Variable global que recupera el id de la incidencia o grupo
    val1 = LRR12.get()                                                  # Recupera el id de la incidencia o grupo
    if  val1 == "": return                                              # Si no ha puesto ningún id, no hará nada               
    LimpiaElegibles                                                     # Limpia las cajas
    base_datos = sqlite3.connect('databases/basesDeDatosProforma.db')	# Crea una base de datos o se conecta a una
    c = base_datos.cursor()	                                            # Crea cursor
    c.execute("SELECT * FROM bd_proforma WHERE oid = " + val1)	        # Query the database
    records = c.fetchall()                                              # Recupera los resultados
    base_datos.close()                                                  # Cerramos incidencias
    menuIncidenciasFacturaProformaIntroducirCrear()                     # Vuelve hacia atrás
    # Creando las variables globales
    global  fecha,fechaPro,NumPro,Cliente,Cant1,concept1,Precio1,Cant2,Concept2,Precio2,Iva,TipoIva,IncluidoIva,IdIncidencia   
    # Loop para volcar los resultados    
    for record in records:
             
        LRR1.config(text = val1)
        LRR31.config(state = "readandwrite")
        LRR31.insert(0,record[3])
        LRR42.insert(0,record[0])
        LRR52.insert(0,record[4])
        LRR62.insert(0,record[5])
        LRR72.insert(0,record[6])
        LRR82.insert(0,record[7])
        LRR92.insert(0,record[8])
        LRR102.insert(0,record[9])  
    LRR22.focus()                                                       # Centramos el cursor
def query_proforma_busca    ():
    
    global EstamosEnProforma
    # Canviar esto en base a búsqueda
    v1 = LRR12.get() # PROFORMA
    v2 = LRR21.get() # CLIENT
    v3 = LRR32.get() # DIA
    v4 = LRR42.get() # MES
    v5 = LRR52.get() # ANY
    v6 = LRR62.get() # QUANTITAT
    v7 = LRR72.get() # PREU
    # Si v4 sólo tiene un dígito, le añadimos un 0 delante
    if len(v4) == 1:
        v4 = "0" + v4
    # Si v3 sólo tiene un dígito, le añadimos un 0 delante
    if len(v3) == 1:
        v3 = "0" + v3
    # Si v5 tiene 2 dígitos, le añadimos un 20 delante
    if len(v5) == 2:
        v5 = "20" + v5
        
    # Creamos la base de datos o conectamos con una
    query_todos('databases/basesDeDatosProforma.db',
                "SELECT *, oid FROM bd_Proforma WHERE ((NUM_PRO = '" + v1 + "' or '" + v1 + "' = '') AND (CLIENTE ='" + v2 + "' or '" + v2 + "' = '') AND ((PRECIO_1 = '" + v7 + "' or '" + v7 + "' = '') OR (PRECIO_2 = '" + v7 + "' OR '" + v7 + "' = '')) AND  ((CANT_1 = '" + v6 + "' OR '" + v6 + "' = '') OR (CANT_2 = '" + v6 + "' or '" + v6 + "' = '')) AND (FECHA LIKE '" + v3 + "/%' or '" + v3 + "' = '') AND (FECHA LIKE '%/" + v4 + "/%' or '" + v4 + "' = '') AND (FECHA LIKE '%/" + v5 + "' or '" + v5 + "' = '')) ORDER BY NUM_PRO DESC",
                8,
                "EstamosEnProforma",
                "ID","DATA","","PROFORMA","CLIENT","QUANTITAT","CONCEPTE","PREU","")
def ProformaCorrigeUno      ():
    
    global val1
    val1 = LRR12.get()
    global val2
    val2 = usuarioReal
    global diaGlobal
    diaGlobal = diaGlobaltk.get()
    global mesGlobal
    mesGlobal = mesGlobaltk.get()
    global anyoGlobal
    anyoGlobal = anyoGlobaltk.get()

    if  val1 == "":
        return
                       
    # Limpia las cajas
    LimpiaElegibles
    
	# Crea una base de datos o se conecta a una
    base_datos = sqlite3.connect('databases/basesDeDatosProforma.db')

	# Crea cursor
    c = base_datos.cursor()
    
	# Query the database
    c.execute("SELECT * FROM bd_proforma WHERE oid = " + val1)
    records = c.fetchall()
    
    menuIncidenciasFacturaProformaIntroducirCrear()
      
    # Creando las variables globales
    global  fecha
    global  fechaPro
    global  NumPro
    global  Cliente
    global  Cant1
    global  concept1
    global  Precio1
    global  Cant2
    global  Concept2
    global  Precio2
    global  Iva
    global  TipoIva
    global  IncluidoIva
    global  IdIncidencia
    global  parte    
      
    # Loop para volcar los resultados
    
    for record in records:
              
        LRR1.config(text = val1)
        LRR22.insert(0,record[2])
        LRR31.config(state = "readandwrite")
        LRR31.insert(0,record[3])
        LRR42.insert(0,record[0])
        LRR52.insert(0,record[4])
        LRR62.insert(0,record[5])
        LRR72.insert(0,record[6])
        LRR82.insert(0,record[7])
        LRR92.insert(0,record[8])
        LRR102.insert(0,record[9])
        LRR111.config(state = "readandwrite")
        # Borra el contenido
        LRR111.delete(0,END)
        LRR111.insert(0,record[10])
        LRR111.config(state = "readonly")
        LRR122.insert(0,record[11])
        LRR131.config(state = "readandwrite")
        LRR131.insert(0,record[12])
        LRR131.config(state = "readonly")
        LRR142.delete(0,END)
        try:        
            LRR142.insert(0,record[14])
        except:
            pass
        val6 =record[0]
        val7 = []
        for t in val6.split("/"):
            val7.append(t)
        diaGlobaltk.set(val7[0])
        mesGlobaltk.set(val7[1])
        anyoGlobaltk.set(val7[2])
        diaFecha.config(text = diaGlobaltk)
        mesFecha.config(text = mesGlobaltk)
        anyoFecha.config(text = anyoGlobaltk)
        MiraFecha(anyoFecha)
    
    # Si en cualquier momento se pulsan las teclas CTRL + P se fuerza la impresión de PDF
    raiz.bind("<Control-p>", lambda event: BotonImprimirForzado())
    raiz.bind("<Control-P>", lambda event: BotonImprimirForzado())     
    Boton7activado(PDFProforma)    

    # Centramos el cursor
    LRR22.focus()

    Boton4activado2(ProformaSalvaCorrecc)
def ProformaSalvaCorrecc    ():
    
    global origenes
    global usuarioReal
    global diaGlobal
    global mesGlobal
    global anyoGlobal
    

    # Rescata los valores de los campos
    v1 = LRR1.cget("text")
    v2 = LRR22.get()
    v3 = LRR31.get()
    v4 = LRR42.get()
    v5 = LRR52.get()
    v6 = LRR62.get()
    v7 = LRR72.get()
    v8 = LRR82.get()
    v9 = LRR92.get()
    v10 = LRR102.get()
    v11 = LRR111.get()
    v12 = LRR122.get()
    v13 = LRR131.get()
    # Guardamos en v14 el valor de ID de incedències/grups si existe
    v14 = VieneDeIncGrups
    v15 = LRR142.get()
            
    # Coteja errores
    # Miramos si v2 está vacío
    if v2 == "":
        LR23.config(text = "Falta proforma")
        LRR22.focus()
        return
    
    # Miramos si v2 existe como NUM_PRO
    # Abrimos la tabla de proformas
    conn = sqlite3.connect('databases/basesDeDatosProforma.db')
    c = conn.cursor()
    # Bucle revisando todas las proformas
    for row in c.execute('SELECT *, oid FROM bd_Proforma'):
        # Si el NUM_PRO coincide con v2 y el ID no coincide con v1
            
        if row[2] == v2 and row[-1] != int(v1):

            
            # Cerramos la tabla
            conn.close()
            # Mostramos el error
            LR23.config(text = "Proforma duplicat")
            # Ponemos el foco en NUM_PRO
            LRR22.focus()
            return
    
    # Si en v2 hay el símbolo "/" avisamos que no es válido
    if "/" in v2:
        LR23.config(text = "No es pot posar '/' al nom de proforma")
        LRR22.focus()
        return   
    # Miramos si ha puesto un cliente
    if v3 == "":
        LR23.config(text = "Falta Client")
        LRR31.focus()
        return
        
    # Miramos si el cliente existe
    # Abrimos la tabla de clientes
    conn = sqlite3.connect('databases/basesDeDatosProforma.db')
    c = conn.cursor()
    # Bucle revisando todos los clientes
    exist = False
    for row in c.execute('SELECT * FROM bd_Proforma'):
        # Si el ID coincide con v3
        if row[3] == v3:
            # Cerramos la tabla
            conn.close()
            # Ponemos la variable exist en True
            exist = True
            # Salimos del bucle
            break
    if exist == False:
        LR23.config(text = "Client inexistent")
        LRR31.focus()
        return  
        
    # Miramos que la fecha esté bien escrita
    try:
        # Si el principio de v4 es 1 dígito y "/"
        if v4[1] == "/":
            #Añadimos un 0 delante
            v4 = "0" + v4
        # Si el principio de v4 no es 2 dígitos y "/"
        if v4[0:2].isdigit() == False:
            LR23.config(text = "Dia incorrecte")
            LRR42.focus()
            return

        # Si la posición 4 es "/"
        if v4[4] == "/":
            # Añadimos un 0 entre la posición 2 y 3
            v4 = v4[0:3] + "0" + v4[3:]
        # Si v4 no contiene "/" dos digitos y "/"
        if v4[3:5].isdigit() == False:
            LR23.config(text = "Mes incorrecte")
            LRR42.focus()
            return

        # Si el largo de la cadena v4 es inferior a 10 caracteres
        if len(v4) <= 9:
            # Añadimos 20 entre las posiciones 5 y 6
            v4 = v4[0:6] + "20" + v4[6:] 
        # Si v4 no acaba en 4 dígitos
        if v4[6:10].isdigit() == False:
            LR23.config(text = "Any incorrecte")
            LRR42.focus()
            return
        # Si el largo es superior a 10 caracteres
        if len(v4) > 10:
            LR23.config(text = "DOta incorrecte")
            LRR42.focus()
            return
    except:
            LR23.config(text = "Data incorrecte")
            LRR42.focus() 
            return 

    # Si v5 no es un número y no está en blanco
    if v5 != "" and v5.isdigit() == False:
        LR23.config(text = "Quantitat incorrecte")
        LRR52.focus()
        return
        
    # Si v7 no es un número y no está en blanco
    if v7 != "" and v7.isdigit() == False:
        LR23.config(text = "Preu incorrecte")
        LRR72.focus()
        return
        
    # Si v8 no es un número y no está en blanco
    if v8 != "" and v8.isdigit() == False:
        LR23.config(text = "Quantitat incorrecte")
        LRR82.focus()
        return
        
    # Si v10 no es un número y no está en blanco
    if v10 != "" and v10.isdigit() == False:
        LR23.config(text = "Preu incorrecte")
        LRR102.focus()
        return
        
    # Si v11 está vacío
    if v11 == "":
        LR23.config(text = "hi ha IVA?")
        LRR111.focus()
        return
        
    # Si v11 es sí y v12 está vacío
    if  v11 == "Si" and v12 == "":
        LR23.config(text = "% d'IVA?")
        LRR122.focus()
        return
        
    # Si v11 es sí y v12 no es un número
    if  v11 == "Si" and v12.isdigit() == False:
        LR23.config(text = "L'IVA ha de ser número")
        LRR122.focus()
        return
        
    # Si v11 es sí y v13 está vacío
    if  v11 == "Si" and v13 == "":
        LR23.config(text = "No sabem si l'IVA està inclòs")
        LRR131.focus()
        return
                    
    # Salva datos
    # Crea la base de datos o conecta con ella
    baseData = sqlite3.connect('databases/basesDeDatosProforma.db')
          
    # Crea el cursor
    c = baseData.cursor()   
    # A partir de aquí se ha de revisar entero
    c.execute("""UPDATE bd_proforma SET
            FECHA_PRO          = :fechaPro,
            NUM_PRO            = :numPro,
            CLIENTE            = :cliente,
            CANT_1             = :cant1,
            CONCEPT_1          = :concept1,
            PRECIO_1           = :precio1,
            CANT_2             = :cant2,
            CONCEPT_2          = :concept2,
            PRECIO_2           = :precio2,
            IVA                = :iva,
            TIPO_IVA           = :tipoIva,
            INCLUIDO_IVA       = :incluidoIva,
            PARTE              = :parte  

            WHERE oid = :val1""",
              {
                'fechaPro': v4,
                'numPro': v2,
                'cliente': v3,
                'cant1': v5,
                'concept1': v6,
                'precio1': v7,
                'cant2': v8,
                'concept2': v9,
                'precio2': v10,
                'iva': v11,
                'tipoIva': v12,
                'incluidoIva': v13,
                'parte': v15,
                'val1': val1
                  })
    
    #Asegura los cambios
    baseData.commit()

	# Cierra la conexión 
    baseData.close()  

    # Vuelve a pintar usuario y fecha
    nomUsuario.config(text = val2)
    
    # Recupera en las variables tk los datos de fecha salvados en diaGlobal, mesGlobal y anyoGlobal
    anyoGlobaltk.set(anyoGlobal)
    mesGlobaltk.set(mesGlobal)
    diaGlobaltk.set(diaGlobal)
    # Los vuelca a los labels
    diaFecha.config(text = diaGlobaltk)
    mesFecha.config(text = mesGlobaltk)
    anyoFecha.config(text = anyoGlobaltk)
    MiraFecha(anyoFecha)
	# Vuelve hacia atrás
    menuIncidenciasFacturaProformaCorregir()
def ProformaBorraUno        ():
    # Creamos la base de datos o conectamos con una
    base_datos = sqlite3.connect('databases/basesDeDatosProforma.db')
    busqueda = "SELECT *, oid FROM bd_proforma WHERE (oid = '" + LRR12.get() + "')"
    columnas = 8
    global puntero
    query(base_datos,busqueda,columnas,"ID","DATA","","PROFORMA","CLIENT","QUANTITAT","CONCEPTE","PREU","")
    
    val1 = LRR12.get()

    # si no ha puesto ningún id, no hará nada
    if val1 == "":  return
        
    # Ventana de aviso
    ventanaSeleccion("Aixó esborrarà la proforma amb id "+ val1 +", si existeix.","red",del_proform_yes) 
def del_proform_yes         ():

    base_datos = sqlite3.connect('databases/basesDeDatosProforma.db')   # Creamos base de datos o conectamos a una    
    c = base_datos.cursor()	                                            # Creamos el cursor
    c.execute("DELETE from bd_proforma WHERE oid = " + LRR12.get())	    # Borra el registro
    Le_Bd_Se_todos(base_datos)                                          # Acciones comunes
    # Borramos los datos del listado de registros
    query_todos('databases/basesDeDatosProforma.db',
                "SELECT *, oid FROM bd_proforma ORDER BY NUM_PRO",
                8,
                "EstamosEnProformas",
                "ID","DATA","","PROFORMA","CLIENT","QUANTITAT","CONCEPTE","PREU","")              
    LRR12.focus()                                                       # Foco

def query_bloqueos          ():
    
        
    global puntero
    if puntero <= 0:
        puntero = 0
        query_bloqueos_busca()
        return
    else:
        puntero -= 42
        query_bloqueos_busca()    
def query_bloqueos_busca    ():
    global EstamosEnBloqueos    
    v2 = LRR12.get()
    # Creamos la base de datos o conectamos con una
    query_todos('databases/basesDeDatosIncidencias.db',
                "SELECT *, oid FROM bd_bloqueos WHERE (FECHA = '" + v2 + "')",
                8,
                "EstamosEnBloqueos",
                "ID","DATA","DESDE","FINS","","","","","")
def bloqueoBorraUno         ():

    global v2
    # Rescata los valores de los campos
    v2 = LRR12.get()
        
    # Coteja errores
    try:
        # Si el principio de v2 es 1 dígito y "/"
        if v2[1] == "/":
            #Añadimos un 0 delante
            v2 = "0" + v2
        # Si el principio de v2 no es 2 dígitos y "/"
        if v2[0:2].isdigit() == False:
            LR23.config(text = "Dia incorrecte")
            LRR22.focus()
            return

        # Si la posición 4 es "/"
        if v2[4] == "/":
            # Añadimos un 0 entre la posición 2 y 3
            v2 = v2[0:3] + "0" + v2[3:]
        # Si v2 no contiene "/" dos digitos y "/"
        if v2[3:5].isdigit() == False:
            LR23.config(text = "Mes incorrecte")
            LRR22.focus()
            return

        # Si el largo de la cadena v2 es inferior a 10 caracteres
        if len(v2) <= 9:
            # Añadimos 20 entre las posiciones 5 y 6
            v2 = v2[0:6] + "20" + v2[6:] 
        # Si v2 no acaba en 4 dígitos
        if v2[6:10].isdigit() == False:
            LR23.config(text = "Any incorrecte")
            LRR22.focus()
            return
        # Si el largo es superior a 10 caracteres
        if len(v2) > 10:
            LR23.config(text = "Data incorrecte")
            LRR22.focus()
            return
    except:
            LR23.config(text = "Data incorrecte")
            LRR22.focus() 
            return

    # Creamos la base de datos o conectamos con una
    base_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')
    busqueda = "SELECT *, oid FROM bd_bloqueos WHERE (FECHA = '" + LRR12.get() + "')"
    columnas = 8
    global puntero
    query(base_datos,busqueda,columnas,"ID","DATA","DESDE","FINS","","","","","")
    
    # Ventana de aviso
    ventanaSeleccion("Aixó esborrarà el bloqueig del"+ v2 +", si existeix.","red",del_block_yes)
def del_block_yes           ():
    
    global v2                                                           # Hace global el valor de v2
    base_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')# Creamos base de datos o conectamos a una
    c = base_datos.cursor()	                                            # Creamos el cursor
    c.execute("DELETE from bd_bloqueos WHERE FECHA = '" + v2 + "'")	    # Borra el registro
    Le_Bd_Se_todos(base_datos)                                          # Acciones comunes
    query_bloqueos()                                                    # Borramos los datos del listado de registros
    LRR12.focus()                                                       # Foco
           
def query_productos_busca   ():
    
    global EstamosEnProductos
    v1,v2,v3,v4 = LRR11.get(),LRR22.get(),LRR32.get(),LRR41.get() 
    # Creamos la base de datos o conectamos con una
    query_todos('databases/basesDeDatosDatos.db',
                "SELECT *, oid FROM bd_productos WHERE ((NOM = '" + v1 + "' or '" + v1 + "' = '') AND (PREU_HABITUAL = '" + v2 + "' or '" + v2 + "' = '') AND (PREU_ACTUAL = '" + v3 + "' or '" + v3 + "' = '') AND (REGISTRABLE = '" + v4 + "' or '" + v4 + "' = '')) ORDER BY NOM",
                4,
                "EstamosEnProductos",
                "ID","NOM","PREU REAL","PREU ACTUAL","TIPUS")
def productoCorrigeUno      ():

    global val1                                 # Hace global el valor de val1
    val1 = LRR12.get()                          # Rescata el valor del campo de texto  
    LimpiaElegibles                             # Limpia las cajas
	# Crea una base de datos o se conecta a una
    base_datos = sqlite3.connect('databases/basesDeDatosDatos.db')
    c = base_datos.cursor()	                    # Crea cursor
	# Query the database
    c.execute("SELECT * FROM bd_productos WHERE oid = " + val1)
    records = c.fetchall()                      # Guarda los resultados en una variable
    MenuDatosProductoIntroducir()               # Llama a la función que crea la ventana de datos
    # Creando las variables globales
    global nombre,precio,precioact,regsto  
    for record in records:                      # Loop para volcar los resultados
        LRR1.config(text = val1)
        LRR22.insert(0,record[0])
        LRR32.insert(0,record[1])
        LRR42.insert(0,record[2])
        LRR51.config(state = "readandwrite")
        LRR51.insert(0,record[3])
        LRR51.config(state = "readonly")    
    LRR22.focus()                               # Centramos el cursor
    Boton4activado2(ProductoSalvaCorreccion)    # Activa el botón de guardar
def ProductoSalvaCorreccion ():

    # Rescata valores
    v1,v2,v3,v4 = LRR22.get(),LRR32.get(),LRR42.get(),LRR51.get()           
    # Coteja fallos
    muralla = False                             # Variable de control
    muralla = cotejaEsNumero(muralla,v3,LRR42)  # Coteja si es número
    muralla = cotejaEsNumero(muralla,v2,LRR32)  # Coteja si es número
    muralla = cotejaVacio(muralla,v4,LRR51)     # Coteja si está vacío
    muralla = cotejaVacio(muralla,v3,LRR42)     # Coteja si está vacío
    muralla = cotejaVacio(muralla,v2,LRR32)     # Coteja si está vacío
    muralla = cotejaVacio(muralla,v1,LRR22)     # Coteja si está vacío
    if muralla == True:                         # Si hay fallos
        LR23.CONFIG(fg = "red")                 # Cambia el color del texto
        return                                  # Si hay fallos, no hace nada    
    # Crea una base de datos o abre la existente
    base_datos = sqlite3.connect('databases/basesDeDatosDatos.db')
    c = base_datos.cursor()                     # Conecta el cursor
    # Actualiza los datos
    c.execute("""UPDATE bd_productos SET
              NOM = :nombre,
              PREU_HABITUAL = :precio,
              PREU_ACTUAL = :precioact,
              REGISTRABLE = :regsto
                            
              WHERE oid = :val1""",
              {
              'nombre': LRR22.get(),
              'precio': LRR32.get(),
              'precioact': LRR42.get(),
              'regsto': LRR51.get(),
              'val1': val1
                  })
    base_datos.commit()                         # Asegura los cambios
    base_datos.close()  	                    # Cierra la conexión 
    abreLasListas()                             # Actualiza las bases de datos
    MenuDatosProductoCorregir()	                # Vuelve hacia atrás
def productoBorraUno        ():
    
    # Creamos la base de datos o conectamos con una
    base_datos = sqlite3.connect('databases/basesDeDatosDatos.db')
    busqueda = "SELECT *, oid FROM bd_productos WHERE (oid = '" + LRR12.get() + "')"
    columnas = 4
    global puntero
    query(base_datos,busqueda,columnas,"ID","NOM","PREU REAL","PREU ACTUAL","TIPUS")

    val1 = LRR12.get()

    # si no ha puesto ningún id, no hará nada
    if val1 == "":
        
        return
    
    # Ventana de aviso
    # Preparamos la ventana Tk donde trabajaremos
    ventanaSeleccion("Aixó esborrarà el producte amb id "+ val1 +", si existeix.","red",del_product_yes)
def del_product_yes         ():

    base_datos = sqlite3.connect('databases/basesDeDatosDatos.db')      # Creamos base de datos o conectamos a una    
    c = base_datos.cursor()	                                            # Creamos el cursor
    c.execute("DELETE from bd_productos WHERE oid = " + LRR12.get())	# Borra el registro
    LimpiaElegibles()                                                   # Limpia las cajas
    base_datos.commit()	                                                # Asegura los cambios
    base_datos.close()	                                                # Cierra la conexión 
    seleccion.destroy()                                                 # Cierra la ventana de aviso
    Le_Bd_Se_todos(base_datos)                                          # Acciones comunes
    # Borramos los datos del listado de registros
    query_todos('databases/basesDeDatosDatos.db',
                "SELECT *, oid FROM bd_productos ORDER BY NOM",
                4,
                "EstamosEnProductos",
                "ID","NOM","PREU REAL","PREU ACTUAL","TIPUS")              
    LRR12.focus()                                                       # Foco

def query_clientes_busca    ():
    
    global EstamosEnClientes                                            # Para saber en qué ventana estamos
    v1,v2,v3,v4 = LRR11.get(),LRR22.get(),LRR32.get(),LRR42.get()       # Rescatamos los valores de las cajas
       
    # Creamos la base de datos o conectamos con una
    query_todos('databases/basesDeDatosClientes.db',
                "SELECT *, oid FROM bd_clientes WHERE ((NOM = '" + v1 + "' or '" + v1 + "' = '') AND (TELEFONO = '" + v2 + "' or '" + v2 + "' = '') AND (MAIL = '" + v3 + "' or '" + v3 + "' = '') AND (NIFCIF = '" + v4 + "' or '" + v4 + "' = '')) ORDER BY NOM",
                7,
                "EstamosEnClientes",
                "ID","NOM","","","CIUTAT/PAIS","TELÈFON","MAIL","NIF/CIF")
def clienteCorrigeUno       ():

    global val1                                                         # Hace global la variable val1
    val1 = LRR12.get()                                                  # Rescatamos el valor de la caja
    LimpiaElegibles                                                     # Limpia las cajas
    base_datos = sqlite3.connect('databases/basesDeDatosClientes.db')	# Crea una base de datos o se conecta a una
    c = base_datos.cursor()	                                            # Crea cursor
    c.execute("SELECT * FROM bd_clientes WHERE oid = " + val1)	        # Query the database
    records = c.fetchall()                                              # Guarda los resultados en una variable
    MenuDatosClienteIntroducir()                                        # Llamamos a la ventana de introducción de datos
    # Creando las variables globales
    global nombre,dir1,dir2,dir3,telefono,mail,nifcif,contacto,telfcontacto
    for record in records:                                              # Loop para volcar los resultados  
        LRR1.config(text = val1)
        LRR22.insert(0,record[0])
        LRR32.insert(0,record[1])
        LRR42.insert(0,record[2])
        LRR52.insert(0,record[3])
        LRR62.insert(0,record[4])
        LRR72.insert(0,record[5])
        LRR82.insert(0,record[6])
        LRR92.insert(0,record[7])
        LRR102.insert(0,record[8])
        LRR112.insert(0,record[9])      
    LRR22.focus()                                                       # Centramos el cursor
    Boton4activado2(ClienteSalvaCorreccion)                             # Activamos el botón de guardar
def ClienteSalvaCorreccion  ():

    v1,v4 = LRR22.get(),LRR62.get()                     # Rescata valores
    # Coteja fallos
    muralla = False                                     # Variable para controlar si hay fallos
    if v4 != "":
        muralla = cotejaEsNumero(muralla,v4,LRR52)      # Coteja si el teléfono es un número             
    muralla = cotejaCaracteres(muralla,v1,LRR22,"'",'"')# Coteja si el nombre tiene caracteres prohibidos
    muralla = cotejaVacio(muralla,v1,LRR22)             # Coteja si el nombre está vacío    
    if muralla == True:                                 # Si hay fallos
        LR23.config(fg = "red")                         # Pone el texto en rojo
        return                                          # Sale de la función        
    # Crea una base de datos o abre la existente
    base_datos = sqlite3.connect('databases/basesDeDatosClientes.db')
    c = base_datos.cursor()                             # Conecta el cursor
    # Actualiza los datos 
    c.execute("""UPDATE bd_clientes SET
              NOM = :nombre,
              DIRECCION1    = :dir1,
              DIRECCION2    = :dir2,
              DIRECCION3    = :dir3,
              TELEFONO      = :telefono,
              MAIL          = :mail,
              NIFCIF        = :nifcif,
              CONTACTO      = :contacto,
              TELFCONTACTO  = :telfcontacto
                            
              WHERE oid     = :val1""",
              {
              'nombre':         LRR22.get(),
              'dir1':           LRR32.get(),
              'dir2':           LRR42.get(),
              'dir3':           LRR52.get(),
              'telefono':       LRR62.get(),
              'mail':           LRR72.get(),
              'nifcif':         LRR82.get(),
              'contacto':       LRR92.get(),
              'telfcontacto':   LRR102.get(),
              'val1':       val1
                  })
    base_datos.commit()                                 # Asegura los cambios
    base_datos.close()	                                # Cierra la conexión 
    abreLasListas()                                     # Actualiza las bases de datos
    MenuDatosClienteCorregir()                          # Vuelve a la ventana de corrección
def clienteBorraUno         ():
    
    # Creamos la base de datos o conectamos con una
    base_datos = sqlite3.connect('databases/basesDeDatosClientes.db')
    # Creamos la consulta
    busqueda = "SELECT *, oid FROM bd_clientes WHERE (oid = '" + LRR12.get() + "')"
    columnas = 7                                        # Número de columnas
    global puntero                                      # Hace global la variable puntero
    # Llama a la función query
    query(base_datos,busqueda,columnas,"ID","NOM","","","CIUTAT/PAIS","TELÈFON","MAIL","NIF/CIF")
    val1 = LRR12.get()                                  # Rescatamos el valor de la caja
    if val1 == "":  return                              # si no ha puesto ningún id, no hará nada
    # Ventana de aviso
    ventanaSeleccion("Aixó esborrarà el client amb id "+ val1 +", si existeix.","red",del_client_yes)
def del_client_yes          ():

    base_datos = sqlite3.connect('databases/basesDeDatosClientes.db')   # Creamos base de datos o conectamos a una    
    c = base_datos.cursor()	                                            # Creamos el cursor
    c.execute("DELETE from bd_clientes WHERE oid = " + LRR12.get())	    # Borra el registro
    LimpiaElegibles()                                                   # Limpia las cajas
    base_datos.commit()	                                                # Asegura los cambios
    base_datos.close()	                                                # Cierra la conexión 
    seleccion.destroy()                                                 # Cierra la ventana de aviso
    Le_Bd_Se_todos(base_datos)                                          # Acciones comunes
    # Borramos los datos del listado de registros
    query_todos('databases/basesDeDatosClientes.db',
                "SELECT *, oid FROM bd_clientes ORDER BY NOM",
                7,
                "EstamosEnClientes",
                "ID","NOM","","","CIUTAT/PAIS","TELÈFON","MAIL","NIF/CIF")             
    LRR12.focus()                                                       # Foco

def query_usuarios_busca    ():

    global EstamosEnUsuarios                       # Variable global para saber en qué ventana estamos
    v1,v2,v3,v4,v5,v6 = LRR11.get(),LRR21.get(),LRR31.get(),LRR41.get(),LRR51.get(),LRR61.get()    
    # Creamos la base de datos o conectamos con una
    query_todos('databases/basesDeDatosDatos.db',
                "SELECT *, oid FROM bd_usuarios WHERE ((NOM = '" + v1 + "' or '" + v1 + "' = '') AND (NIVEL = '" + v2 + "' or '" + v2 + "' = '') AND (INGLES = '" + v3 + "' or '" + v3 + "' = '') AND (CASTELLANO = '" + v4 + "' or '" + v4 + "' = '') AND (CATALAN = '" + v5 + "' or '" + v5 + "' = '') AND (FRANCES = '" + v6 + "' or '" + v6 + "' = '')) ORDER BY NOM",
                8,
                "EstamosEnUsuarios",
                "ID","NOM","CLAU","NIVELL","ANGLÈS","CASTELLÀ"," CATALÀ","FRANCÈS","HORES")
def usuariosCorrigeUno      ():

    global val1                                                     # Variable global para el id del registro a modificar
    val1 = LRR12.get()                                              # Recoge el id del registro a modificar
    LimpiaElegibles                                                 # Limpia las cajas
    base_datos = sqlite3.connect('databases/basesDeDatosDatos.db')	# Crea una base de datos o se conecta a una
    c = base_datos.cursor()	                                        # Crea cursor
    c.execute("SELECT * FROM bd_usuarios WHERE oid = " + val1)	    # Crea la selección
    records = c.fetchall()                                          # Recoge los resultados
    menuDatosUsuarioIntroducir()                                    # Abre la ventana de introducción de datos 
    global nombre, clave, nivel, ingl, cast, cata, fran, horas      # Creando las variables globales
    for record in records:                                          # Loop para volcar los resultados      
        LRR12.insert(0,record[0])                                   # Volcamos los resultados en las cajas
        LRR22.insert(0,record[1])   
        LRR32.insert(0,record[1])
        LRR41.config(state = "readandwrite")
        LRR41.insert(0,record[2])
        LRR41.config(state = "readonly")
        LRR51.config(state = "readandwrite")
        LRR51.insert(0,record[3])
        LRR51.config(state = "readonly")
        LRR61.config(state = "readandwrite")
        LRR61.insert(0,record[4])
        LRR61.config(state = "readonly")
        LRR71.config(state = "readandwrite")
        LRR71.insert(0,record[5])
        LRR71.config(state = "readonly")
        LRR81.config(state = "readandwrite")
        LRR81.insert(0,record[6])
        LRR81.config(state = "readonly")
        LRR92.insert(0,record[7])      
    LRR12.focus()                                                   # Centramos el cursor
    Boton4activado2(UsuarioSalvaCorreccion)
def UsuarioSalvaCorreccion  ():

    # Rescata valores
    v1, v2, v3, v4, v5, v6, v7, v8, v9 = LRR12.get(), LRR22.get(), LRR32.get(), LRR41.get(), LRR51.get(), LRR61.get(), LRR71.get(), LRR81.get(), LRR92.get()
    # Coteja fallos
    muralla = False                                 # Si muralla = True, no se salva
    muralla = cotejaIgualdad(muralla,v2,v3,LRR22)   # Coteja que no sean iguales
    muralla = cotejaEsNumero(muralla,v9,LRR92)      # Coteja que sea numero
    muralla = cotejaVacio(muralla,v1,LRR12)         # Coteja que no esten vacios
    muralla = cotejaVacio(muralla,v2,LRR22)         # Coteja que no esten vacios
    muralla = cotejaVacio(muralla,v3,LRR32)         # Coteja que no esten vacios
    muralla = cotejaVacio(muralla,v4,LRR41)         # Coteja que no esten vacios
    muralla = cotejaVacio(muralla,v5,LRR51)         # Coteja que no esten vacios
    muralla = cotejaVacio(muralla,v6,LRR61)         # Coteja que no esten vacios
    muralla = cotejaVacio(muralla,v7,LRR71)         # Coteja que no esten vacios
    muralla = cotejaVacio(muralla,v8,LRR81)         # Coteja que no esten vacios
    muralla = cotejaVacio(muralla,v9,LRR92)         # Coteja que no esten vacios
    if muralla == True:                             # Si muralla = True, no se salva
        LR23.config(fg = "red")                     # Pintamos de rojo el campo LR23
        return                                      # Salimos de la funcion        
    # Crea una base de datos o abre la existente
    base_datos = sqlite3.connect('databases/basesDeDatosDatos.db')   
    c = base_datos.cursor()                         # Conecta el cursor
    c.execute("""UPDATE bd_usuarios SET
              NOM = :nombre,
              CLAVE = :clave,
              NIVEL = :nivel,
              INGLES = :ingl,
              CASTELLANO = :cast,
              CATALAN = :cata,
              FRANCES = :fran,
              HORASMES = :horas
                            
              WHERE oid = :val1""",
              {
              'nombre': LRR12.get(),
              'clave': LRR22.get(),
              'nivel': LRR41.get(),
              'ingl': LRR51.get(),
              'cast': LRR61.get(),
              'cata': LRR71.get(),
              'fran': LRR81.get(),
              'horas': LRR92.get(),
              'val1': val1
                  })
    
    base_datos.commit()                             # Asegura los cambios
    base_datos.close()  	                        # Cierra la conexión 
    abreLasListas()                                 # Actualiza las bases de datos
    menuDatosUsuarioCorregir()	                    # Vuelve hacia atrás
def usuariosBorraUno        ():

    # Creamos la base de datos o conectamos con una
    base_datos = sqlite3.connect('databases/basesDeDatosDatos.db')
    # Creamos el cursor
    busqueda = "SELECT *, oid FROM bd_usuarios WHERE (oid = '" + LRR12.get() + "')"
    columnas = 8                                                        # Número de columnas
    global puntero                                                      # Variable global
    # Llamamos a la función que crea la tabla
    query(base_datos,busqueda,columnas,
          "ID","NOM","CLAU","NIVELL","ANGLÈS","CASTELLÀ"," CATALÀ","FRANCÈS","HORES")
    val1 = LRR12.get()                                                  # Rescata el valor de la caja
    if val1 == "":  return                                              # si no ha puesto ningún id, no hará nada
    # Ventana de aviso
    ventanaSeleccion("Aixó esborrarà l'usuari amb id "+ val1 +", si existeix.","red",del_user_yes)
def del_user_yes            ():

    base_datos = sqlite3.connect('databases/basesDeDatosDatos.db')      # Creamos base de datos o conectamos a una    
    c = base_datos.cursor()	                                            # Creamos el cursor
    c.execute("DELETE from bd_usuarios WHERE oid = " + LRR12.get())	    # Borra el registro
    Le_Bd_Se_todos(base_datos)                                          # Acciones comunes
    # Borramos los datos del listado de registros
    query_todos('databases/basesDeDatosDatos.db',
                "SELECT *, oid FROM bd_usuarios ORDER BY NOM",
                8,
                "EstamosEnUsuarios",
                "ID","NOM","CLAU","NIVELL","ANGLÈS","CASTELLÀ","CATALÀ","FRANCÈS","HORES")          
    LRR12.focus()                                                       # Foco

def Registros_Todo          (num):

    TEXTO = globals()['VIEW%s' % num].cget("text")
   
    # Hacemos globales las variables que vamos a usar
    global vr1,vr2,vr3,vr4,vr5,vr6,vr7
    # Guardamos los valores del registro
    vr1 = LRR21.get()
    vr2 = LRR31.get()
    vr3 = LRR41.get()
    vr4 = LRR51.get()
    vr5 = LRR61.get()
    vr6 = LRR73.get(1.0,END)
    MiraFecha(anyoFecha)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
    # Ponemos en la label LRR12 el valor VALOR
    LRR12.delete(0,'end')
    LRR12.insert(0,TEXTO)
    LRR22.focus()
    registroCorrigeUno()
    vr7 = True
def Incidencias_Todo        (num):
    
    TEXTO = globals()['VIEW%s' % num].cget("text")

    # Hacemos globales las variables que vamos a usar
    global vr1,vr2,vr3,vr4,vr5,vr6,vr7,vr8,vr9,vr10,vr11,vr12,vr13,vr14
    # Guardamos los valores del registro    
    vr1 = LRR22.get()
    vr2 = LRR32.get()
    vr3 = LRR42.get()
    vr4 = LRR51.get()
    vr5 = LRR61.get()
    vr6 = LRR71.get()
    vr8 = LRR82.get()
    vr9 = LRR92.get()
    vr10 = LRR102.get()
    vr11 = LRR112.get()
    vr12 = LRR121.get()
    vr13 = LRR131.get()
         
    MiraFecha(anyoFecha)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
    # Ponemos en la label LRR12 el valor VALOR
    LRR12.delete(0,'end')
    LRR12.insert(0,TEXTO)
    LRR22.focus()
    incidenciasCorrigeUno()
    vr14 = True
def Proforma_Todo           (num):
    
    TEXTO = globals()['VIEW%s' % num].cget("text")

    MiraFecha(anyoFecha)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
    # Ponemos en la label LRR12 el valor VALOR
    LRR12.delete(0,'end')
    LRR12.insert(0,TEXTO)
    LRR22.focus()
    ProformaCorrigeUno()
def Bloqueos_Todo           (num):
    
    TEXTO = globals()['VIEW%s' % num].cget("text")

    # Buscamos en bd_bloqueos el registro que queremos
    # Creamos la base de datos o conectamos con una
    base_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')
    # Creamos el cursor
    c = base_datos.cursor()
    # Buscamos el registro
    c.execute("SELECT * FROM bd_bloqueos WHERE (oid = '" + TEXTO + "')")
    # Guardamos los datos en una variable
    registros = c.fetchall()
    # TEXTO tiene que valer ahora el valor de la columna 1
    TEXTO = registros[0][0]
    
    MiraFecha(anyoFecha)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
    # Ponemos en la label LRR12 el valor VALOR
    LRR12.delete(0,'end')
    LRR12.insert(0,TEXTO)
    LRR22.focus()
    bloqueoBorraUno()
def Productos_Todo          (num):
    
    TEXTO = globals()['VIEW%s' % num].cget("text")

    MiraFecha(anyoFecha)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
    # Ponemos en la label LRR12 el valor VALOR
    LRR12.delete(0,'end')
    LRR12.insert(0,TEXTO)
    LRR22.focus()
    productoCorrigeUno()
def Clientes_Todo           (num):
    
    TEXTO = globals()['VIEW%s' % num].cget("text")

    MiraFecha(anyoFecha)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
    # Ponemos en la label LRR12 el valor VALOR
    LRR12.delete(0,'end')
    LRR12.insert(0,TEXTO)
    LRR22.focus()
    clienteCorrigeUno()
def Usuarios_Todo           (num):
    
    TEXTO = globals()['VIEW%s' % num].cget("text")

    MiraFecha(anyoFecha)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
    # Ponemos en la label LRR12 el valor VALOR
    LRR12.delete(0,'end')
    LRR12.insert(0,TEXTO)
    LRR22.focus()
    usuariosCorrigeUno()
    
def query                   (seleccion,busc,columnas,*enunciados):
    
    global EstamosEnIncidencias,EstamosEnRegistros,EstamosEnProforma,EstamosEnBloqueos,EstamosEnProductos,EstamosEnClientes,EstamosEnUsuarios

    # Definimos a puntero como global para que se guarde su valor fuera de la función
    global puntero
        
	# Crea el cursor
    cursor = seleccion.cursor()

	# Muestra la base de datos
    cursor.execute(busc)
    datos = cursor.fetchall()
    cant_registros = len(datos)
    LR22.config(text = str(cant_registros) + " registres")
    borra_datos()
    
    columna = 0
    for dato in enunciados:
        
        num = "0" + str(columna) + "00"
        globals()['VIEW%s' % num].config(text = str(dato),bg = "#5d5b45",fg = "#FFFFFF",font=("Helvetica",9,"bold"))
        columna += 1
    columna = 0
    puntero2 = 0
    num_dicc = {}
    # Loop para todos los datos
    for dato in datos:
                   
        # Si el dato que mira es inferior al puntero, no se muestra
        if puntero2 < puntero:

            puntero2 += 1
            continue
        
        num = "000" + str(columna+1)
        globals()['VIEW%s' % num].config(text = str(dato[-1]))
        globals()['VIEW%s' % num].config(command=lambda: regresaSinNada() ) 

        if EstamosEnRegistros == True:
            
            num_dicc['num%s' % num] = num
            func = lambda val: Registros_Todo(val)
            globals()['VIEW%s' % num].config(command=lambda func=func, val=num_dicc['num%s' % num]: func(val))
                                                
        if EstamosEnIncidencias == True:
            
            num_dicc['num%s' % num] = num
            func = lambda val: Incidencias_Todo(val)
            globals()['VIEW%s' % num].config(command=lambda func=func, val=num_dicc['num%s' % num]: func(val))

        if EstamosEnProforma == True:
            
            num_dicc['num%s' % num] = num
            func = lambda val: Proforma_Todo(val)
            globals()['VIEW%s' % num].config(command=lambda func=func, val=num_dicc['num%s' % num]: func(val))
        
        if EstamosEnBloqueos == True:
            
            num_dicc['num%s' % num] = num
            func = lambda val: Bloqueos_Todo(val)
            globals()['VIEW%s' % num].config(command=lambda func=func, val=num_dicc['num%s' % num]: func(val))
            
        if EstamosEnProductos == True:
            
            num_dicc['num%s' % num] = num
            func = lambda val: Productos_Todo(val)
            globals()['VIEW%s' % num].config(command=lambda func=func, val=num_dicc['num%s' % num]: func(val))
            
        if EstamosEnClientes == True:
            
            num_dicc['num%s' % num] = num
            func = lambda val: Clientes_Todo(val)
            globals()['VIEW%s' % num].config(command=lambda func=func, val=num_dicc['num%s' % num]: func(val))
            
        if EstamosEnUsuarios == True:
            
            num_dicc['num%s' % num] = num
            func = lambda val: Usuarios_Todo(val)
            globals()['VIEW%s' % num].config(command=lambda func=func, val=num_dicc['num%s' % num]: func(val)) 
                                                                                       
        for i in range (columnas):
            
            if  enunciados[i+1] == "CLAU":
                num = "0" + str(i+1) + "0" + str(columna+1)
                globals()['VIEW%s' % num].config(text = "********")
            elif enunciados[i+1] == "":
                num = "0" + str(i+1) + "0" + str(columna+1)
            elif EstamosEnIncidencias == True:
                if enunciados[i+1] == "PRODUCTE" or enunciados[i+1] == "IDIOMA":
                    num = "0" + str(i+1) + "0" + str(columna+1)
                    globals()['VIEW%s' % num].config(text = str(dato[i+1]))
                elif enunciados[i+1] == "ESTAT":
                    num = "0" + str(i+1) + "0" + str(columna+1)
                    globals()['VIEW%s' % num].config(text = str(dato[i+2]))
                elif enunciados[i+1] == "CLIENT": 
                    num = "0" + str(i+1) + "0" + str(columna+1)
                    globals()['VIEW%s' % num].config(text = str(dato[i+4]))
                elif enunciados[i+1] == "PAGAT": 
                    num = "0" + str(i+1) + "0" + str(columna+1)
                    globals()['VIEW%s' % num].config(text = str(dato[i+11]))
                else:
                    num = "0" + str(i+1) + "0" + str(columna+1)
                    globals()['VIEW%s' % num].config(text = str(dato[i]))         
            else:
                num = "0" + str(i+1) + "0" + str(columna+1)
                globals()['VIEW%s' % num].config(text = str(dato[i]))
                                
        columna += 1
        
        if columna == 21:
            
            # Situamos el puntero para la siguiente vuelta
            puntero += 21
            break            

	# Asegura los cambios
    seleccion.commit()

	# Cierra la conexión con la base de datos
    seleccion.close()
    
    # Todo es falso
    EstamosEnIncidencias, EstamosEnRegistros, EstamosEnProforma, EstamosEnBloqueos, EstamosEnProductos, EstamosEnClientes, EstamosEnProductos, EstamosEnClientes, EstamosEnUsuarios = False, False, False, False, False, False, False, False, False
    return
def del_no                  ():

    LimpiaElegibles()           # Limpia las labels de elegibles
    seleccion.destroy()         # Destruye la ventana de selección

def PDFTablasPax            ():
    
    # Creamos el nombre del archivo de salida
    Nombre = "pdf/Pax "+ LRR22.get() + " " + LRR12.get() + ".pdf"
    
    # Creamos el documento, DIN A4 y apaisado
    PDF = canvas.Canvas(Nombre, pagesize=landscape(A4))
    
    # Imágenes en el documento
    PDF.drawImage('image/LOGO PARA PDF.bmp',5*mm,5*mm,width=35,height=35)
    PDF.drawImage('image/MARCA PARA PDF.bmp',260*mm,5*mm,width=100,height =14)

    # Tipografía y tamaño
    pdfmetrics.registerFont(TTFont('Boecklins Universe','image/Boecklins Universe.ttf'))
    PDF.setFont('Boecklins Universe',18)
    PDF.setFillColorRGB(0.4,0.1,0.3)
    PDF.drawString(22*mm,200*mm,"Tabla de Pax: "+ LRR22.get() + "/" + LRR12.get() + " - Total: "+globals()['VIEW039032'].cget("text"))
    
    # Espacios
    columna = 0
    
    for columnas in range(9,289,7):
        fila = 32
        alterna = True
        for filas in range(25,190,5):
            
            if filas == 25 or columnas == 9+39*7:
                PDF.setFillColorRGB(0.9,0.9,0.9)
            elif filas == 25+32*5 or columnas == 9:
                PDF.setFillColorRGB(0.4,0.7,0.6)               
            else:
                if alterna == True:
                    PDF.setFillColorRGB(1,1,1)
                    alterna = False
                else:
                    PDF.setFillColorRGB(0.8,0.8,1)
                    alterna = True
            PDF.setStrokeColorRGB(0,0,0)
            PDF.rect(columnas*mm,filas*mm,7*mm,5*mm,fill = True)
            num = "0" + str(columna) + "0" + str(fila)
            valor = globals()['VIEW%s' % num].cget("text")
            if  columnas == 9 and filas > 25 and filas != 25+32*5 or filas == 25+32*5:
                PDF.setFillColorRGB(1,1,1)
            
            else:
                PDF.setFillColorRGB(0,0,0)    
            PDF.setFont('Helvetica',8)
            PDF.drawCentredString(columnas*mm+10,filas*mm+4,valor)
            fila -= 1
        columna += 1     
    # Muestra el PDF
    PDF.showPage()
    
    # Salva el PDF
    PDF.save()
    
    # Salimos de tabla pax
    ventanaTabla.destroy()
    preMenuTablas()
def PDFTablasVGrupos        ():
    # Creamos el nombre del archivo de salida
    Nombre = "pdf/Pax per zones "+ LRR12.get() + " " + LRR22.get() + " " + LRR32.get() + "   " + LRR42.get() + " " + LRR52.get() + " " + LRR62.get() + ".pdf"
    
    # Creamos el documento, DIN A4 y apaisado
    PDF = canvas.Canvas(Nombre, pagesize=landscape(A4))
    
    # Imágenes en el documento
    PDF.drawImage('image/LOGO PARA PDF.bmp',5*mm,5*mm,width=35,height=35)
    PDF.drawImage('image/MARCA PARA PDF.bmp',260*mm,5*mm,width=100,height =14)

    # Tipografía y tamaño
    pdfmetrics.registerFont(TTFont('Boecklins Universe','image/Boecklins Universe.ttf'))
    PDF.setFont('Boecklins Universe',18)
    PDF.setFillColorRGB(0.4,0.1,0.3)
    PDF.drawString(22*mm,200*mm,"Pax per zones: "+ LRR12.get() + "/" + LRR22.get() + "/" + LRR32.get() + " - " + LRR42.get() + "/" + LRR52.get() + "/" + LRR62.get())

    # Espacios
    columna = 0
    
    for columnas in range(90,205,40):
        fila = 34
        alterna = True
        for filas in range(20,195,5):
            
            if filas == 190:
                PDF.setFillColorRGB(0.9,0.9,0.9) 
            elif filas == 70 or filas == 125 or filas == 180 or filas == 185 or columnas == 90 and filas!= 190:
                PDF.setFillColorRGB(0.4,0.7,0.6)               
            else:
                if alterna == True:
                    PDF.setFillColorRGB(1,1,1)
                    alterna = False
                else:
                    PDF.setFillColorRGB(0.8,0.8,1)
                    alterna = True
            PDF.setStrokeColorRGB(0,0,0)
            PDF.rect(columnas*mm,filas*mm,40*mm,5*mm,fill = True)
            num = "0" + str(columna) + "0" + str(fila)
            valor = globals()['VIEW%s' % num].cget("text")
            
            if  columnas == 90 and filas != 190 or filas == 70 or filas == 125 or filas == 180 or filas == 185:
                PDF.setFillColorRGB(1,1,1)
            
            else:
                PDF.setFillColorRGB(0,0,0)    
            
            PDF.setFont('Helvetica',8)
            PDF.drawCentredString(columnas*mm+57,filas*mm+4,str(valor))
            fila -= 1
        columna += 1     
    # Muestra el PDF
    PDF.showPage()
    
    # Salva el PDF
    PDF.save()
    
    # Salimos de tabla pax
    ventanaTabla.destroy()
    preMenuTablas()
def PDFTablasVProvincias    ():
    # Creamos el nombre del archivo de salida
    Nombre = "pdf/Pax per províncies "+ LRR12.get() + " " + LRR22.get() + " " + LRR32.get() + "   " + LRR42.get() + " " + LRR52.get() + " " + LRR62.get() + ".pdf"
    
    # Creamos el documento, DIN A4 y apaisado
    PDF = canvas.Canvas(Nombre, pagesize=landscape(A4))
    
    # Imágenes en el documento
    PDF.drawImage('image/LOGO PARA PDF.bmp',5*mm,5*mm,width=35,height=35)
    PDF.drawImage('image/MARCA PARA PDF.bmp',260*mm,5*mm,width=100,height =14)

    # Tipografía y tamaño
    pdfmetrics.registerFont(TTFont('Boecklins Universe','image/Boecklins Universe.ttf'))
    PDF.setFont('Boecklins Universe',18)
    PDF.setFillColorRGB(0.4,0.1,0.3)
    PDF.drawString(22*mm,200*mm,"Tabla de Pax per províncies: "+ LRR12.get() + "/" + LRR22.get() + "/" + LRR32.get() + " - " + LRR42.get() + "/" + LRR52.get() + "/" + LRR62.get())

    # Espacios
    columna = 0
    
    for columnas in range(70,225,40):
        fila = 4
        alterna = True
        for filas in range(120,145,5):
            
            if filas == 145:
                PDF.setFillColorRGB(0.9,0.9,0.9) 
            elif columnas == 70:
                PDF.setFillColorRGB(0.4,0.7,0.6)               
            else:
                if alterna == True:
                    PDF.setFillColorRGB(1,1,1)
                    alterna = False
                else:
                    PDF.setFillColorRGB(0.8,0.8,1)
                    alterna = True
            PDF.setStrokeColorRGB(0,0,0)
            PDF.rect(columnas*mm,filas*mm,40*mm,5*mm,fill = True)
            num = "0" + str(columna) + "0" + str(fila)
            valor = globals()['VIEW%s' % num].cget("text")
            
            if  columnas == 70 or filas == 145:
                PDF.setFillColorRGB(1,1,1)
            
            else:
                PDF.setFillColorRGB(0,0,0)    
            
            PDF.setFont('Helvetica',8)
            PDF.drawCentredString(columnas*mm+57,filas*mm+4,str(valor))
            fila -= 1
        columna += 1     
    # Muestra el PDF
    PDF.showPage()
    
    # Salva el PDF
    PDF.save()
    
    # Salimos de tabla pax
    ventanaTabla.destroy()
    preMenuTablas()
def PDFTablasVComarcas      ():
# Creamos el nombre del archivo de salida
    Nombre = "pdf/Pax per comarques "+ LRR12.get() + " " + LRR22.get() + " " + LRR32.get() + "   " + LRR42.get() + " " + LRR52.get() + " " + LRR62.get() + ".pdf"
    
    # Creamos el documento, DIN A4 y apaisado
    PDF = canvas.Canvas(Nombre, pagesize=landscape(A4))
    
    # Imágenes en el documento
    PDF.drawImage('image/LOGO PARA PDF.bmp',5*mm,5*mm,width=35,height=35)
    PDF.drawImage('image/MARCA PARA PDF.bmp',260*mm,5*mm,width=100,height =14)

    # Tipografía y tamaño
    pdfmetrics.registerFont(TTFont('Boecklins Universe','image/Boecklins Universe.ttf'))
    PDF.setFont('Boecklins Universe',18)
    PDF.setFillColorRGB(0.4,0.1,0.3)
    PDF.drawString(22*mm,200*mm,"Tabla de Pax per comarques: "+ LRR12.get() + "/" + LRR22.get() + "/" + LRR32.get() + " - " + LRR42.get() + "/" + LRR52.get() + "/" + LRR62.get())

    # Espacios
    columna = 0
    
    for columnas in range(70,190,40):
        fila = 10
        alterna = True
        for filas in range(120,175,5):
            
            if filas == 170:
                PDF.setFillColorRGB(0.9,0.9,0.9) 
            elif columnas == 70:
                PDF.setFillColorRGB(0.4,0.7,0.6)               
            else:
                if alterna == True:
                    PDF.setFillColorRGB(1,1,1)
                    alterna = False
                else:
                    PDF.setFillColorRGB(0.8,0.8,1)
                    alterna = True
            PDF.setStrokeColorRGB(0,0,0)
            PDF.rect(columnas*mm,filas*mm,40*mm,5*mm,fill = True)
            num = "0" + str(columna) + "0" + str(fila)
            valor = globals()['VIEW%s' % num].cget("text")
            
            if  columnas == 70 and filas < 170:
                PDF.setFillColorRGB(1,1,1)
            
            else:
                PDF.setFillColorRGB(0,0,0)    
            
            PDF.setFont('Helvetica',8)
            PDF.drawCentredString(columnas*mm+57,filas*mm+4,str(valor))
            fila -= 1
        columna += 1     
    # Muestra el PDF
    PDF.showPage()
    
    # Salva el PDF
    PDF.save()
    
    # Salimos de tabla pax
    ventanaTabla.destroy()
    preMenuTablas()
def PDFTablasVPerfiles      ():
# Creamos el nombre del archivo de salida
    Nombre = "pdf/Pax per perfils "+ LRR12.get() + " " + LRR22.get() + " " + LRR32.get() + "   " + LRR42.get() + " " + LRR52.get() + " " + LRR62.get() + ".pdf"
    
    # Creamos el documento, DIN A4 y apaisado
    PDF = canvas.Canvas(Nombre, pagesize=landscape(A4))
    
    # Imágenes en el documento
    PDF.drawImage('image/LOGO PARA PDF.bmp',5*mm,5*mm,width=35,height=35)
    PDF.drawImage('image/MARCA PARA PDF.bmp',260*mm,5*mm,width=100,height =14)

    # Tipografía y tamaño
    pdfmetrics.registerFont(TTFont('Boecklins Universe','image/Boecklins Universe.ttf'))
    PDF.setFont('Boecklins Universe',18)
    PDF.setFillColorRGB(0.4,0.1,0.3)
    PDF.drawString(22*mm,200*mm,"Tabla de Pax per perfils: "+ LRR12.get() + "/" + LRR22.get() + "/" + LRR32.get() + " - " + LRR42.get() + "/" + LRR52.get() + "/" + LRR62.get())

    # Espacios
    columna = 0
    
    for columnas in range(70,190,40):
        fila = 10
        alterna = True
        for filas in range(120,175,5):
            
            if filas == 170:
                PDF.setFillColorRGB(0.9,0.9,0.9) 
            elif columnas == 70:
                PDF.setFillColorRGB(0.4,0.7,0.6)               
            else:
                if alterna == True:
                    PDF.setFillColorRGB(1,1,1)
                    alterna = False
                else:
                    PDF.setFillColorRGB(0.8,0.8,1)
                    alterna = True
            PDF.setStrokeColorRGB(0,0,0)
            PDF.rect(columnas*mm,filas*mm,40*mm,5*mm,fill = True)
            num = "0" + str(columna) + "0" + str(fila)
            valor = globals()['VIEW%s' % num].cget("text")
            
            if  columnas == 70 and filas < 170:
                PDF.setFillColorRGB(1,1,1)
            
            else:
                PDF.setFillColorRGB(0,0,0)    
            
            PDF.setFont('Helvetica',8)
            PDF.drawCentredString(columnas*mm+57,filas*mm+4,str(valor))
            fila -= 1
        columna += 1     
    # Muestra el PDF
    PDF.showPage()
    
    # Salva el PDF
    PDF.save()
    
    # Salimos de tabla pax
    ventanaTabla.destroy()
    preMenuTablas()
def PDFTablasVFuentes       ():
# Creamos el nombre del archivo de salida
    Nombre = "pdf/Pax per fonts "+ LRR12.get() + " " + LRR22.get() + " " + LRR32.get() + "   " + LRR42.get() + " " + LRR52.get() + " " + LRR62.get() + ".pdf"
    
    # Creamos el documento, DIN A4 y apaisado
    PDF = canvas.Canvas(Nombre, pagesize=landscape(A4))
    
    # Imágenes en el documento
    PDF.drawImage('image/LOGO PARA PDF.bmp',5*mm,5*mm,width=35,height=35)
    PDF.drawImage('image/MARCA PARA PDF.bmp',260*mm,5*mm,width=100,height =14)

    # Tipografía y tamaño
    pdfmetrics.registerFont(TTFont('Boecklins Universe','image/Boecklins Universe.ttf'))
    PDF.setFont('Boecklins Universe',18)
    PDF.setFillColorRGB(0.4,0.1,0.3)
    PDF.drawString(22*mm,200*mm,"Tabla de Pax per fonts: "+ LRR12.get() + "/" + LRR22.get() + "/" + LRR32.get() + " - " + LRR42.get() + "/" + LRR52.get() + "/" + LRR62.get())

    # Espacios
    columna = 0
    
    for columnas in range(70,190,40):
        fila = 10
        alterna = True
        for filas in range(120,175,5):
            
            if filas == 170:
                PDF.setFillColorRGB(0.9,0.9,0.9) 
            elif columnas == 70:
                PDF.setFillColorRGB(0.4,0.7,0.6)               
            else:
                if alterna == True:
                    PDF.setFillColorRGB(1,1,1)
                    alterna = False
                else:
                    PDF.setFillColorRGB(0.8,0.8,1)
                    alterna = True
            PDF.setStrokeColorRGB(0,0,0)
            PDF.rect(columnas*mm,filas*mm,40*mm,5*mm,fill = True)
            num = "0" + str(columna) + "0" + str(fila)
            valor = globals()['VIEW%s' % num].cget("text")
            
            if  columnas == 70 and filas < 170:
                PDF.setFillColorRGB(1,1,1)
            
            else:
                PDF.setFillColorRGB(0,0,0)    
            
            PDF.setFont('Helvetica',8)
            PDF.drawCentredString(columnas*mm+57,filas*mm+4,str(valor))
            fila -= 1
        columna += 1     
    # Muestra el PDF
    PDF.showPage()
    
    # Salva el PDF
    PDF.save()
    
    # Salimos de tabla pax
    ventanaTabla.destroy()
    preMenuTablas()
def PDFTablasVHoras         ():
# Creamos el nombre del archivo de salida
    Nombre = "pdf/Pax per hores "+ LRR12.get() + " " + LRR22.get() + " " + LRR32.get() + "   " + LRR42.get() + " " + LRR52.get() + " " + LRR62.get() + ".pdf"
    
    # Creamos el documento, DIN A4 y apaisado
    PDF = canvas.Canvas(Nombre, pagesize=landscape(A4))
    
    # Imágenes en el documento
    PDF.drawImage('image/LOGO PARA PDF.bmp',5*mm,5*mm,width=35,height=35)
    PDF.drawImage('image/MARCA PARA PDF.bmp',260*mm,5*mm,width=100,height =14)

    # Tipografía y tamaño
    pdfmetrics.registerFont(TTFont('Boecklins Universe','image/Boecklins Universe.ttf'))
    PDF.setFont('Boecklins Universe',18)
    PDF.setFillColorRGB(0.4,0.1,0.3)
    PDF.drawString(22*mm,200*mm,"Tabla de Pax per hores: "+ LRR12.get() + "/" + LRR22.get() + "/" + LRR32.get() + " - " + LRR42.get() + "/" + LRR52.get() + "/" + LRR62.get())

    # Espacios
    columna = 0
    
    for columnas in range(70,190,40):
        fila = 10
        alterna = True
        for filas in range(120,175,5):
            
            if filas == 170:
                PDF.setFillColorRGB(0.9,0.9,0.9) 
            elif columnas == 70:
                PDF.setFillColorRGB(0.4,0.7,0.6)               
            else:
                if alterna == True:
                    PDF.setFillColorRGB(1,1,1)
                    alterna = False
                else:
                    PDF.setFillColorRGB(0.8,0.8,1)
                    alterna = True
            PDF.setStrokeColorRGB(0,0,0)
            PDF.rect(columnas*mm,filas*mm,40*mm,5*mm,fill = True)
            num = "0" + str(columna) + "0" + str(fila)
            valor = globals()['VIEW%s' % num].cget("text")
            
            if  columnas == 70 and filas < 170:
                PDF.setFillColorRGB(1,1,1)
            
            else:
                PDF.setFillColorRGB(0,0,0)    
            
            PDF.setFont('Helvetica',8)
            PDF.drawCentredString(columnas*mm+57,filas*mm+4,str(valor))
            fila -= 1
        columna += 1     
    # Muestra el PDF
    PDF.showPage()
    
    # Salva el PDF
    PDF.save()
    
    # Salimos de tabla pax
    ventanaTabla.destroy()
    preMenuTablas()
def PDFTablasVDias          ():
# Creamos el nombre del archivo de salida
    Nombre = "pdf/Assitència per dies "+ LRR12.get() + " " + LRR22.get() + " " + LRR32.get() + "   " + LRR42.get() + " " + LRR52.get() + " " + LRR62.get() + ".pdf"
    
    # Creamos el documento, DIN A4 y apaisado
    PDF = canvas.Canvas(Nombre, pagesize=landscape(A4))
    
    # Imágenes en el documento
    PDF.drawImage('image/LOGO PARA PDF.bmp',5*mm,5*mm,width=35,height=35)
    PDF.drawImage('image/MARCA PARA PDF.bmp',260*mm,5*mm,width=100,height =14)

    # Tipografía y tamaño
    pdfmetrics.registerFont(TTFont('Boecklins Universe','image/Boecklins Universe.ttf'))
    PDF.setFont('Boecklins Universe',18)
    PDF.setFillColorRGB(0.4,0.1,0.3)
    PDF.drawString(22*mm,200*mm,"Assitència per dies: "+ LRR12.get() + "/" + LRR22.get() + "/" + LRR32.get() + " - " + LRR42.get() + "/" + LRR52.get() + "/" + LRR62.get())

    # Espacios
    columna = 0
    
    for columnas in range(70,190,40):
        fila = 11
        alterna = True
        for filas in range(115,175,5):
            
            if filas == 170 or filas == 140:
                PDF.setFillColorRGB(0.9,0.9,0.9) 
            elif columnas == 70:
                PDF.setFillColorRGB(0.4,0.7,0.6)               
            else:
                if alterna == True:
                    PDF.setFillColorRGB(1,1,1)
                    alterna = False
                else:
                    PDF.setFillColorRGB(0.8,0.8,1)
                    alterna = True
            PDF.setStrokeColorRGB(0,0,0)
            PDF.rect(columnas*mm,filas*mm,40*mm,5*mm,fill = True)
            num = "0" + str(columna) + "0" + str(fila)
            valor = globals()['VIEW%s' % num].cget("text")
            
            if  columnas == 70 and filas < 170 and filas != 140:
                PDF.setFillColorRGB(1,1,1)
            
            else:
                PDF.setFillColorRGB(0,0,0)    
            
            PDF.setFont('Helvetica',8)
            PDF.drawCentredString(columnas*mm+57,filas*mm+4,str(valor))
            fila -= 1
        columna += 1     
    # Muestra el PDF
    PDF.showPage()
    
    # Salva el PDF
    PDF.save()
    
    # Salimos de tabla pax
    ventanaTabla.destroy()
    preMenuTablas()
def PDFTablasVOrigen        ():
 # Creamos el nombre del archivo de salida
    Nombre = "pdf/Pax per origens "+ LRR12.get() + " " + LRR22.get() + " " + LRR32.get() + "   " + LRR42.get() + " " + LRR52.get() + " " + LRR62.get() + ".pdf"
    
    # Creamos el documento, DIN A4 y apaisado
    PDF = canvas.Canvas(Nombre, pagesize=landscape(A4))
    
    # Imágenes en el documento
    PDF.drawImage('image/LOGO PARA PDF.bmp',5*mm,5*mm,width=35,height=35)
    PDF.drawImage('image/MARCA PARA PDF.bmp',260*mm,5*mm,width=100,height =14)

    # Tipografía y tamaño
    pdfmetrics.registerFont(TTFont('Boecklins Universe','image/Boecklins Universe.ttf'))
    PDF.setFont('Boecklins Universe',18)
    PDF.setFillColorRGB(0.4,0.1,0.3)
    PDF.drawString(22*mm,200*mm,"Tabla de Pax per origens: "+ LRR12.get() + "/" + LRR22.get() + "/" + LRR32.get() + " - " + LRR42.get() + "/" + LRR52.get() + "/" + LRR62.get())

    # Espacios
    columna = 0
    
    for columnas in range(70,190,40):
        fila = 10
        alterna = True
        for filas in range(120,175,5):
            
            if filas == 170:
                PDF.setFillColorRGB(0.9,0.9,0.9) 
            elif columnas == 70:
                PDF.setFillColorRGB(0.4,0.7,0.6)               
            else:
                if alterna == True:
                    PDF.setFillColorRGB(1,1,1)
                    alterna = False
                else:
                    PDF.setFillColorRGB(0.8,0.8,1)
                    alterna = True
            PDF.setStrokeColorRGB(0,0,0)
            PDF.rect(columnas*mm,filas*mm,40*mm,5*mm,fill = True)
            num = "0" + str(columna) + "0" + str(fila)
            valor = globals()['VIEW%s' % num].cget("text")
            
            if  columnas == 70 and filas < 170:
                PDF.setFillColorRGB(1,1,1)
            
            else:
                PDF.setFillColorRGB(0,0,0)    
            
            PDF.setFont('Helvetica',8)
            PDF.drawCentredString(columnas*mm+57,filas*mm+4,str(valor))
            fila -= 1
        columna += 1     
    # Muestra el PDF
    PDF.showPage()
    
    # Salva el PDF
    PDF.save()
    
    # Salimos de tabla pax
    ventanaTabla.destroy()
    preMenuTablas()
def PDFProforma             ():

    # Ventana de aviso
    ventanaAviso("Generant PDF...","blue",1)
    try:
        # Abrimos la base de datos de clientes
        conn = sqlite3.connect('databases/basesDeDatosClientes.db')
        c = conn.cursor()
        # Elige el cliente con el mismo nombre que en la proforma
        c.execute("SELECT * FROM bd_clientes WHERE NOM = ?", (LRR31.get(),))
        # Guarda los datos del cliente en una variable
        datosCliente = c.fetchall()    
        
        # Creamos el nombre del archivo de salida
        Nombre = "pdf/"+LRR22.get()+" - Proforma - "+LRR31.get()+".pdf"
        
        # Creamos el documento, DIN A4 y formato vertical
        PDF = canvas.Canvas(Nombre, pagesize=A4)
        
        # Rectangulo magenta en la parte superior en escala a 255
        PDF.setFillColorRGB(0.6,0.2,0.4)
        PDF.setStrokeColorRGB(0.6,0.2,0.4)
        PDF.rect(35*mm,265*mm,140*mm,7*mm,fill = True)
        
        # Imágenes en el documento
        PDF.drawImage('image/LOGO PARA PDF.bmp',42*mm,235*mm,width=65,height=65)
        PDF.drawImage('image/MARCA PARA PDF.bmp',35*mm,230*mm,width=100,height =14)

        # Cambia texto a blanco
        PDF.setFillColorRGB(1,1,1)
        
        # Escribe sobre el rectangulo "Factura Proforma"
        PDF.setFont('Helvetica',13)
        PDF.drawCentredString(65*mm,267*mm,"Factura Proforma")
        
        # Escribe sobre el rectangulo El número de factura
        PDF.setFont('Helvetica',7)
        PDF.drawCentredString(155*mm,267*mm,LRR22.get())
        
        # Cambiamos el texto a negro
        PDF.setFillColorRGB(0,0,0)
        
        # Bajo MARCA escribimos "direccio@casanavas.cat"
        PDF.setFont('Helvetica',7)
        PDF.drawString(41*mm,227*mm,"info@casanavas.cat")
        
        # Pinta cuadrado negro vacío a la derecha de LOGO
        PDF.setStrokeColorRGB(0,0,0)
        PDF.rect(90*mm,225*mm,85*mm,35*mm,fill = False)
        
        # Escribe dentro del cuadrado  seis lineas de texto justificado a la izquierda
        # Activamos negrita
        PDF.setFont('Helvetica-Bold',8)
        PDF.drawString(92*mm,255*mm,LRR31.get())
        
        # Desactivamos negrita
        PDF.setFont('Helvetica',8)
        PDF.drawString(92*mm,250*mm,datosCliente[0][1])
        PDF.drawString(92*mm,245*mm,"C.P.: "+datosCliente[0][2]+ " "+datosCliente[0][3])
        PDF.drawString(92*mm,240*mm,"nif/cif: "+datosCliente[0][6])
        PDF.drawString(92*mm,235*mm,"Telèfon: "+datosCliente[0][4])
        PDF.drawString(92*mm,230*mm,"Correu electrònic: "+datosCliente[0][5])
        
        # Ponemos color a la letra como el cuadrado
        PDF.setFillColorRGB(0.6,0.2,0.4)
        
        # Debajo del cuadrado negro justificado a la izquierda escribimos "Data de la factura proforma"
        PDF.setFont('Helvetica',9)
        PDF.drawString(92*mm,220*mm,"Data de la factura proforma:")
        
        # Cambiamos el color a negro
        PDF.setFillColorRGB(0,0,0)
        
        # A continuación de "Data de la factura proforma" escribimos la fecha
        PDF.setFont('Helvetica',9)
        PDF.drawString(132*mm,220*mm,str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year))
        
        # Cambiamos el color a gris para pintar cuadrados
        PDF.setFillColorRGB(0.6,0.2,0.4)
        PDF.setStrokeColorRGB(0.8,0.8,1)
        
        # Pinta el rectangulo gris global con sus celdas de colores
        PDF.rect(35*mm,200*mm,140*mm,10*mm,fill = True)
        PDF.rect(35*mm,180*mm,140*mm,10*mm,fill = False)
        PDF.rect(35*mm,170*mm,140*mm,40*mm,fill = False)
        PDF.rect(55*mm,170*mm,120*mm,40*mm,fill = False)
        PDF.rect(125*mm,160*mm,50*mm,50*mm,fill = False)
        PDF.rect(145*mm,160*mm,30*mm,50*mm,fill = False)
        PDF.rect(145*mm,160*mm,30*mm,10*mm,fill = True)
    
        # Color de letra a blanco
        PDF.setFillColorRGB(1,1,1)
        
        # Escribe en las celdas de la primera fila: Quantitat, Descripció, Preu unitari, Import
        PDF.setFont('Helvetica',8) 
        PDF.drawCentredString(45*mm,204*mm,"Quantitat")
        PDF.drawCentredString(90*mm,204*mm,"Descripció")
        PDF.drawCentredString(135*mm,204*mm,"Preu unitari")
        PDF.drawCentredString(159*mm,204*mm,"Import")
        
        # Color de letra a negro
        PDF.setFillColorRGB(0,0,0)
        
        # Tercera columna de la quinta fila escribe: Total
        PDF.setFont('Helvetica',9)
        PDF.drawCentredString(138*mm,164*mm,"Total:")
        # Si lo que hay en la label LRR142 es distinto de  "100"
        if LRR142.get() != "100":
            PDF.setFillColorRGB(0.6,0.2,0.4)
            PDF.rect(115*mm,150*mm,30*mm,10*mm,fill = False)    
            PDF.rect(145*mm,150*mm,30*mm,10*mm,fill = True)
            PDF.drawString(120*mm,154*mm,"A pagar el "+LRR142.get()+"%:")
        
        # Debajo de todo y centrado escribe: "S'ha d'efectuar l'ingrès una setmana abans de l'acte ES97 2100 0010 3202 0238 4644"
        PDF.setFont('Helvetica',7)
        PDF.drawCentredString(105*mm,30*mm,"S'ha d'efectuar l'ingrès una setmana abans de l'acte ES97 2100 0010 3202 0238 4644")
        
        # Primera columna de la segunda fila escribe los 4 datos de toda la fila
        PDF.setFont('Helvetica',8)
        PDF.drawString(43*mm,193*mm,LRR52.get())
        PDF.drawString(60*mm,193*mm,LRR62.get())
        if LRR72.get() != "":
            PDF.drawString(133*mm,193*mm,LRR72.get()+" €")
        PDF.drawString(43*mm,183*mm,LRR82.get())
        PDF.drawString(60*mm,183*mm,LRR92.get())
        if LRR102.get() != "":
            PDF.drawString(133*mm,183*mm,LRR102.get()+" €")
            
        if LRR111.get() == "Si" and LRR131.get() == "Si":
            try:
                valor1 = (float(LRR52.get())*float(LRR72.get()))/((float(LRR122.get())/100)+1)
            except:
                valor1 = 0
            try:
                valor2 = (float(LRR82.get())*float(LRR102.get()))/((float(LRR122.get())/100)+1)
            except:
                valor2 = 0
        else:
            try:
                valor1 = float(LRR52.get())*float(LRR72.get())
            except:
                valor1 = 0
            try:
                valor2 = float(LRR82.get())*float(LRR102.get())
            except:
                valor2 = 0    
        # Redondeamos "valor" a dos decimales
        valor1 = round(valor1,2)
        valor2 = round(valor2,2)  
        
        if valor1 != 0:       
            PDF.drawString(155*mm,193*mm,str(valor1)+" €")    
        if valor2 != 0:
            PDF.drawString(155*mm,183*mm,str(valor2)+" €")    

        # IVA
        if LRR111.get() == "Si":
            PDF.drawString(60*mm,173*mm,"IVA del: " + str(LRR122.get()) + " %:")
            try:
                valor3 = (valor1 + valor2)*(int(LRR122.get())/100)
                valor3 = round(valor3,2)
                PDF.drawString(155*mm,173*mm,str(valor3)+" €")
            except:
                valor3 = 0    
        else:
            valor3 = 0

        valor4 = valor1 + valor2 + valor3
        
        # Total
        PDF.setFillColorRGB(1,1,1)
        PDF.setFont('Helvetica-Bold',10)
        PDF.drawString(155*mm,163*mm,str(valor4)+" €")

        # Si lo que hay en la label LRR142 es distinto de  "100"
        if LRR142.get() != "100":
            valor5 = valor4*(float(LRR142.get())/100)
            PDF.drawString(155*mm,154*mm,str(valor5)+" €")
                                    
        # Salva el PDF CON el nombre que le hemos dado
        PDF.save()
        
        # Cerramos el proceso
        ventanaAviso("PDF generat. Recorda salvar l'arxiu", "green",2)
        LRR22.focus()                       # Pone el foco en el campo de texto

    except:
        ventanaAviso("ERROR al generar el PDF", "red",2)
        LRR22.focus()                       # Pone el foco en el campo de texto

def preMenuTablas           ():
    
    try:

        destruye_espacios_info(40,33)

    except:

        pass
    
    try:
        
        ventanaTabla.destroy()
    
    except:
        
        pass
    crea_espacios_info(frameLista,10,22)
    menuTablas()
# ------------------------------ Menus -------------------------------

def MenuInicial                             ():
    
    global usuarioNivel
    global avisoint
    BotonPrimeroQNada() 
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    # Si el valor de nivelUsuario es mayor que 0...
    if int(usuarioNivel) != 0 and avisoint == True:  
        # si diaGlobal tiene 1 dígito, le añadimos un 0 delante
        if len(diaGlobal) == 1:
            fdia = "0" + diaGlobal
        else:
            fdia = diaGlobal
        # Lo mismo con el mes
        if len(mesGlobal) == 1:
            fmes = "0" + mesGlobal
        else:
            fmes = mesGlobal
        # Lo mismo con el año pero sies solo 2 dígitos y añaadimos 20 delante
        if len(anyoGlobal) == 2:
            fanyo = "20" + anyoGlobal
        else:   
            fanyo = anyoGlobal   
        
        # Creamos la fecha en formato dd/mm/aaaa
        fechi = fdia + "/" + fmes + "/" + fanyo

        # Abrimos la base de datos BaseDeDatosIncidencias.db
        conexion = sqlite3.connect("databases/BasesDeDatosIncidencias.db")
        # Creamos el cursor
        cursora = conexion.cursor()
        # Query 
        cursora.execute("SELECT *, oid FROM bd_incidencias WHERE ((FECHA = '" + fechi + "') OR (FECHA_REV = '" + fechi + "')) AND (ESTADO != 'Fet') AND (ESTADO != 'Anul.lat')")
        # Crea el fetchall
        incidencritic = cursora.fetchall()
        inciHoy = 0
        inciRev = 0
        # Por cada Incidencia de la lista...
        for incident in incidencritic:
            # Si la fecha de la incidencia es igual a la fecha actual...
            if incident[0] == fechi:
                inciHoy += 1       
            # Si la fecha de revisión de la incidencia es igual a la fecha actual...
            if incident[17] == fechi:
                inciRev += 1
        if inciHoy !=0 or (inciRev != 0 and int(usuarioNivel) < 3):
            
            ventanaAviso("Hi ha "+str(inciHoy)+" incidències o grups per atendre avui", "red",1.5)
            if int(usuarioNivel) <= 2:
                ventanaAviso("Hi ha "+str(inciRev)+" incidències o grups per revisar avui", "blue",1.5)    
            avisoint = False            # Bloqueamos que vuelva a aparecer la ventana
            conexion.close()            # Cerramos la base de datos

             
    LimpiaLabelsRellena()
    if int(usuarioNivel) == 0:
        return
    
    textMenu.config(text = "MENU PRINCIPAL") 
    menusBotones("Tornar",cambioUsuario,"Registre",menuRegistros,"Venda",menuVentas,"Taules",menuTablas,"Arqueijos",menuArqueos,"Stock",menuStocks,"Incidències/grups",menuIncidencias,"Calendaris",menuCalendarios,"Dades",menuDatos,"Seguretat",menuSeguridad)
    
    # Nos enfocamos en raiz
    raiz.deiconify()
    BM1.focus()           

    if int(usuarioNivel) >= 2:
        BM9.config(text="")
    if int(usuarioNivel) >= 3:
        BM8.config(text="")
        BM5.config(text="")
    if int(usuarioNivel) >= 4:
        BM4.config(text="")
    if int(usuarioNivel) == 5:
        BM2.config(text="")
        
def menuRegistros                               ():

    # Globaliza las variables
    global vr1,vr2,vr3,vr4,vr5,vr6,vr7
    # bORRA LAS VARIABLES
    vr1,vr2,vr3,vr4,vr5,vr6,vr7 = "","","","","","",False
        
    # Si aquí se pulsan las teclas CTRL + D no pasa nada
    raiz.bind("<Control-d>", lambda event: regresaSinNada())
    raiz.bind("<Control-D>", lambda event: regresaSinNada())
    BotonPrimeroQNada() 
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    
    if  nomUsuario.cget("text") == "":

        return
    
    nomUsuario.config(text = usuarioReal)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal)
    MiraFecha(anyoFecha)

    ajusta_espacios_info(10,22,7,1,12,20,19,7,16,16,1,1)
    global puntero
    puntero = 0
    
    textMenu.config(text = "MENU REGISTRE")            
    LimpiaLabelsRellena()
    menusBotones("Tornar",MenuInicial,"Introduir (R)",menuRegistrosIntroducir,"Consultar",menuRegistrosConsultar,"Mirar/Corregir",menuRegistroCorregir,"Eliminar",menuRegistroEliminar)
    BM1.focus()            
def menuRegistrosIntroducir                         (modo=None):
    if modo != None:                                        # Si vinimos pulsando CTRL+R
        recuperaFechaActual()                               # Ponemos la fecha actual
    global EstamosEnIntroducir                              # Globalizamos la variable
    EstamosEnIntroducir = True                              # Ponemos la variable a True
    ajusta_espacios_info(10,22,7,1,12,20,19,7,16,16,1,1)    # Ajustamos los espacios
    textMenu.config(text = "MENU REGISTRE")                 # Ponemos el texto del menú        
    global stringBusqueda                                   # Globalizamos la variable
    stringBusqueda = ""                                     # Ponemos la variable a ""
    def menuRegistrosIntroducirIntroduce ():
        
        global stringBusqueda 
        global origenes
        stringBusqueda = ""
    
        # Rescata valores
        v1,v2,v3,v4,v5,v6,v7,v8,v9 = LRR21.get(),LRR31.get(),LRR41.get(),LRR51.get(),LRR61.get(),LRR73.get(1.0,END),anyoGlobaltk.get(),mesGlobaltk.get(),diaGlobaltk.get()
                        
        # Coteja fallos
        muralla = False
        muralla = cotejaVacio(muralla,v5,LRR61)
        muralla = cotejaVacio(muralla,v4,LRR51)
        muralla = cotejaVacio(muralla,v3,LRR41)
        muralla = cotejaVacio(muralla,v2,LRR31)
        muralla = cotejaVacio(muralla,v1,LRR21)
        muralla,v9,v8,v7 = cotejaFecha(muralla,v9,diaFecha,v8,mesFecha,v7,anyoFecha)
        if muralla == True: 
            LR23.config(fg = "red")         # Pintamos de rojo el campo LR23
            return    

        # Salva datos
        base_datos_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')        # Crea la base de datos o conecta con ella
        cursor = base_datos_datos.cursor()                                              # Crea el cursor
                                                                                        # Inserta en la base de tados
        cursor.execute("""INSERT INTO bd_registros VALUES (:usuario, :fecha,
                :descripcion, :origen, :hora, :producto, :fuente, :notas)""",
                {
                    'usuario':      usuarioReal,
                    'fecha':        v7 + "/" + v8 + "/" + v9,
                    'descripcion':  LRR21.get(),
                    'origen':       LRR31.get(),
                    'hora':         LRR41.get(),
                    'producto':     LRR51.get(),
                    'fuente':       LRR61.get(),
                    'notas':        LRR73.get(1.0,END)
                    })        
        base_datos_datos.commit()                                                       # Asegura los cambios
        base_datos_datos.close()                                                        # Cerrar conexion 

                   
        # Pinta datos en zona 3
        query_todos('databases/basesDeDatosRegistros.db',
                    "SELECT *, oid FROM bd_registros ORDER BY FECHA DESC, oid DESC",
                    8,
                    "EstamosEnRegistros",
                    "ID","","DATA","DESCRIPCIÓ","ORIGEN","HORA","PRODUCTE","FONT","")        
        
        LR23.config(text = "")                                                          # Limpia posibles mensajes anteriores innecesarios
        base_datos_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')        # Crea la base de datos o conecta con ella
        cursor = base_datos_datos.cursor()                                              # Crea el cursor 
        cursor.execute("SELECT *, oid FROM bd_registros WHERE ((FECHA LIKE'" +v7 + "/" + v8 + "/" + v9+"')AND(HORA ='"+ v3+"'))")        # Coge el valor del ultimo oid
        sumatorio = cursor.fetchall()                                                   # Sumatorio = a la cantidad de registros de la fecha y hora introducida
        base_datos_datos.close()                                                        # Cerrar conexion 
        LR23.config(text = "Recompte parcial: "+str(len(sumatorio)))                    # Pinta el sumatorio
        LR23.config(fg = "green")                                                       # Pinta el sumatorio en verde
        # Pinta la lista actualizada
        base_datos_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')        # Crea la base de datos o conecta con ella  
        cursor = base_datos_datos.cursor()                                              # Crea el cursor
        cursor.execute("SELECT *, oid FROM bd_registros")                               # Coge el valor del ultimo oid

        # Damos valor a idAdecuado
        try:
            datos = cursor.fetchall()
            dato = datos[-1]
            idAdecuado = dato[8]
        except:
            idAdecuado = 0         
        idCorrecto = int(idAdecuado)+1
        
        base_datos_datos.close()                                                        # Cerrar conexion    
        LRR1.config(text = idCorrecto)                                                  # Pinta el id adecuado
        LRR21.focus()                                                                   # Coloca foco

        
    # Crea la base de datos o conecta con ella
    base_datos_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        
    # Crea el cursor
    cursor = base_datos_datos.cursor()
    
    # Coge el valor del ultimo oid
    cursor.execute("SELECT *, oid FROM bd_registros")
    
    try:
        datos = cursor.fetchall()
        dato = datos[-1]
        idAdecuado = dato[8]
    except:
        idAdecuado = 0
        
    idCorrecto = int(idAdecuado)+1
    
    # Cerrar conexion 
    base_datos_datos.close() 
             
    menusBotones("Tornar",menuRegistros,"Introduir (R)")
    LimpiaLabelsRellena()
    
    OpcionesQuestionario(["1",LR1,"ID:",LRR1,idCorrecto],
                         ["X1",LR2,"DESCRIPCIÓ:",LRR21,descripciones],
                         ["X1",LR3,"ORIGEN:",LRR31,origenes],
                         ["X1",LR4,"HORA:",LRR41,horas],
                         ["X1",LR5,"PRODUCTE:",LRR51,productosR],
                         ["X1",LR6,"FONT:",LRR61,fuentes],
                         ["X3",LR7,"NOTES:",LRR73,""])

    # Hacemos globales las variables que vamos a usar
    global vr1,vr2,vr3,vr4,vr5,vr6,vr7
    # Si las variables vr1 a vr7 tienen datos, se copia esos valroes a las labels respectivas
    if vr7 == True:
        LRR21.set(vr1)
        LRR31.set(vr2)
        LRR41.set(vr3)
        LRR51.set(vr4)
        LRR61.set(vr5)
        LRR73.insert(1.0,vr6)
        vr7 = False
    Boton4activado2(menuRegistrosIntroducirIntroduce)
    query_todos('databases/basesDeDatosRegistros.db',
                "SELECT *, oid FROM bd_registros ORDER BY FECHA DESC, oid DESC",
                8,
                "EstamosEnRegistros",
                "ID","","DATA","DESCRIPCIÓ","ORIGEN","HORA","PRODUCTE","FONT","")        
    ActivaBotonPyFocus(LRR21,BotonPrimeroQ21) 
def menuRegistrosConsultar                          ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = False
           
    LimpiaLabelsRellena()    
    menusBotones("Tornar",menuRegistros,"",regresaSinNada,"Consultar")

    OpcionesQuestionario(["X2",LR1,"DIA:",LRR12],
                         ["X2",LR2,"MES:",LRR22],
                         ["X2",LR3,"ANY:",LRR32],
                         ["X1",LR4,"DESCRIPCIÓ:",LRR41,descripciones],
                         ["X1",LR5,"ORIGEN:",LRR51,origenes],
                         ["X1",LR6,"desde HORA:",LRR61,horas],
                         ["X1",LR7,"fins a HORA:",LRR71,horas],
                         ["X1",LR8,"PRODUCTE:",LRR81,productosR],
                         ["X1",LR9,"FONT:",LRR91,fuentes],
                         ["X1",LR10,"USUARI:",LRR101,usuariosO])
    
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustada())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustada())
         
    Boton4activado(query_todos_busca0,query_registros_busca)
    Boton5activado(prequery_todos,query_registros_busca)
    Boton6activado(query_registros_busca)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuRegistroCorregir                            ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    MiraFecha(anyoFecha)

    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
       
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuRegistros,"",regresaSinNada,"",regresaSinNada,"Mirar/Corregir")
    
    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])
    Boton4activado2(registroCorrigeUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuRegistroEliminar                            ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = True
        
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuRegistros,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Eliminar")
    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])
    Boton4activado2(registroBorraUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)

def menuVentas                                  ():
    
    return # Mientras no se haga el menu de ventas no se puede acceder a este menu
    if  nomUsuario.cget("text") == "":

        return
    global usuarioNivel
    if int(usuarioNivel) == 5:
        return
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    
    LimpiaLabelsRellena()
    textMenu.config(text = "MENU VENDES")   
    menusBotones("Tornar",MenuInicial,"Introduir (E)",menuVentasIntroducir,"Consultar",menuVentasConsultar,"Mirar/Corregir",menuVentasCorregir,"Eliminar",menuVentasEliminar)
    BM1.focus()
def menuVentasIntroducir                            ():
    textMenu.config(text = "MENU VENDES")   

    LimpiaLabelsRellena()
    menusBotones("Tornar",menuVentas,"Introduir (E)")
    
    LR1.config(text = "ID:")
    LRR1.grid(row=0, column=1)  
    LR2.config(text = "CUANTITAT:")
    LRR22.grid(row=1, column=1)  
    LR3.config(text = "PRODUCTE:")  
    LRR31.grid(row=2, column=1) 
    LRR31['values'] = (productos)  
    LR4.config(text = "MODE PAGAMENT:")  
    LRR41.grid(row=3, column=1)  
    LRR41['values'] = (tiposPago)  
    LR5.config(text = "PREU UNITARI:")  
    LRR5.grid(row=4, column=1)
    LRR5.config(text = "Coge el valor del producto")  
    LR6.config(text = "PREU TOTAL:")  
    LRR6.grid(row=5, column=1)
    LRR6.config(text = "multiplica valor por cantidad")
    LR7.config(text = "NOTES:")  
    LRR73.grid(row=6, column=1)
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")    
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ22)
def menuVentasConsultar                             ():
    
    LimpiaLabelsRellena()    
    menusBotones("Tornar",menuVentas,"",regresaSinNada,"Consultar")

    LR1.config(text = "inici DIA:")
    LRR12.grid(row=0, column=1)
    LR2.config(text = "MES:")
    LRR22.grid(row=1, column=1)
    LR3.config(text = "ANY:")  
    LRR32.grid(row=2, column=1)
    LR4.config(text = "final DIA:")  
    LRR42.grid(row=3, column=1)
    LR5.config(text = "MES:")  
    LRR52.grid(row=4, column=1)
    LR6.config(text = "ANY:")  
    LRR62.grid(row=5, column=1)
    LR7.config(text = "PRODUCTE:")  
    LRR71.grid(row=6, column=1)
    LRR71['values'] = (productos)      
    LR8.config(text = "MODE PAGAMENT:")  
    LRR81.grid(row=7, column=1)
    LRR81['values'] = (tiposPago)  
    LR9.config(text = "PREU UNITARI:")  
    LRR92.grid(row=8, column=1)

    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")    
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuVentasCorregir                              ():

    LimpiaLabelsRellena()
    menusBotones("Tornar",menuVentas,"",regresaSinNada,"",regresaSinNada,"Mirar/Corregir")
    
    LR1.config(text = "ID:")
    LRR12.grid(row=0, column=1)
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")     
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuVentasEliminar                              ():

    LimpiaLabelsRellena()
    menusBotones("Tornar",menuVentas,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Eliminar")
    
    LR1.config(text = "ID:")
    LRR12.grid(row=0, column=1)
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")     
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)

def menuTablas                                  ():

    # Si aquí se pulsan las teclas CTRL + D no pasa nada
    raiz.bind("<Control-d>", lambda event: regresaSinNada())
    raiz.bind("<Control-D>", lambda event: regresaSinNada())
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    
    if  nomUsuario.cget("text") == "":

        return
    LimpiaLabelsRellena()
    textMenu.config(text = "MENU TAULES")   
    menusBotones("Tornar",MenuInicial,"Pax",menuTablasPax,"Visitants per zona",menuTablasVGrupo,"Visitants per províncies",menuTablasVProvincia,"Visitants per comarca",menuTablasVComarca,"Visitants per perfil",menuTablasVPerfil,"Visitants per font",menuTablasVFuente,"Visitants per hora",menuTablasVHora,"Visitants per dia",menuTablasVDia,"Visitants per origen",menuTablasVOrigen)
    # Hacemos prioritaria y visible la raiz
    raiz.deiconify()
    BM1.focus()
def menuTablasPax                                   ():
    
    def menuTablasPaxMuestra ():
        
        # Rescata valores
        v1,v2,v3 = LRR12.get(),LRR22.get(),"01"
        # Coteja fallos        
        muralla = False                                             #   Si hay fallo en el registro
        # Si hay error en la fecha
        muralla,v3,v2,v1 = cotejaFecha(muralla,v3,LRR12,v2,LRR22,v1,LRR12)   
        if muralla == True:                                         # Si hay fallo en el registro
            LR23.config(fg = "red")                                 # Pone el fondo en rojo
            return                                                  # Sale de la función   
        LR23.config(text = "")                                      # Limpia posibles mensajes anteriores innecesarios
        ventanaTabla.deiconify()                                    # Importancia en la tabla
        # Crea el título de la tabla
        ventanaTabla.title('Taula Pax: any ' + v1 + '. Mes ' + v2 + '.')
        # Terminamos de dibujar las necesidades de la tabla
        columna = 1                                                 # Columna de la tabla
        for data in range (1,32,2):                                 # Recorre los días del mes            
            fila = 0                                                # Fila de la tabla
            for dato in range (39):                                 # Recorre las horas del día                
                num = "0" + str(fila) + "0" + str(columna)          # Crea el número de la celda
                globals()['VIEW%s' % num].config(bg = "#9A7048")    # Pone el fondo en marrón
                fila += 1                                           # Siguiente fila            
            columna += 2                                            # Siguiente columna     
        columna = 0                                                 # Columna de la tabla
        for dato in range (33):                                     # Recorre las columnas de la tabla            
            num = "000" + str(columna)                              # Crea el número de la celda           
            if num == "0000" or num == "00032":                     # Si es la primera o última columna                
                columna += 1                                        # Siguiente columna
            else:                                                   # Si no es la primera o última columna
                # Crea la celda con color de fondo gris
                globals()['VIEW%s' % num].config(text = str(dato),bg = "grey",fg = "#FFFFFF")
                columna += 1                                        # Siguiente columna
        columna = 0                                                 # Columna de la tabla
        global horas                                                # Hace global la lista de horas
        for dato in range (39):                                     # Recorre las horas del día            
            num = "0" + str(columna) + "00"                         # Crea el número de la celda            
            if num == "0000" or num == "04000":                     # Si es la primera o última columna 
                columna += 1                                        # Siguiente columna                
            else:                                                   # Si no es la primera o última columna                
                # Crea la celda con color de fondo gris
                globals()['VIEW%s' % num].config(text = horas[dato-1])
                columna += 1                                        # Siguiente columna             
        # Abre archivo con los datos en el mes y año necesarios
        # Crea una base de datos o se conecta a una
        base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        c = base_datos.cursor()                                     # Crea cursor
        # Query the database
        c.execute("SELECT * FROM bd_registros WHERE FECHA LIKE '" + v1 + "/" + v2 + "/%'")
        records = c.fetchall()                                      # Devuelve una lista de tuplas        
        for columna in range (1,39):                                # Repasa hora para pegar datos       
            for fila in range (1,32):                               # Recorre los días del mes
                valor = 0                                           # Inicializa el contador de pax
                for pax in records:                                 # Recorre los registros
                    fecha = pax[1].split("/")                       # Separa la fecha en día, mes y año                    
                    if str(int(fecha[2])) == str(fila):             # Si el día del registro es el mismo que el de la tabla
                        labelHora = "0" + str(columna) + "00"       # Crea el número de la celda
                        # Crea la celda con color de fondo gris
                        hora = globals()['VIEW%s' % labelHora].cget("text")
                        if  hora == pax[4]:                         # Si la hora del registro es la misma que la de la tabla
                            valor +=1                               # Suma un pax
                if valor == 0: valor = ""                           # Si no hay pax pone una cadena vacía           
                num = "0" + str(columna) + "0" + str(fila)          # Crea el número de la celda
                # Crea la celda con color de fondo gris
                globals()['VIEW%s' % num].config(text = str(valor))  
        base_datos.close()                                          # Cierra archivo 
        for columna in range(1,39):                                 # Suma totales y pinta resultados
            valor = 0                                               # Inicializa el contador de pax
            for fila in range (1,32):                               # Recorre los días
                labelPax = "0" + str(columna) + "0" + str(fila)     # Crea el número de la celda
                pax = globals()['VIEW%s' % labelPax].cget("text")   # Crea la celda con color de fondo gris
                if pax == "": pax = "0"                             # Si no hay pax pone una cadena vacía
                valor += int(pax)                                   # Suma un pax
            num = "0" + str(columna) + "032"                        # Crea el número de la celda
            globals()['VIEW%s' % num].config(text = str(valor))     # Crea la celda con color de fondo gris    
        valorTotal = 0                                              # Inicializa el contador de pax
        for fila in range(1,32):                                    # Suma totales y pinta resultados
            valor = 0                                               # Inicializa el contador de pax
            for columna in range (1,39):                            # Recorre los días del mes
                labelPax = "0" + str(columna) + "0" + str(fila)     # Crea el número de la celda
                pax = globals()['VIEW%s' % labelPax].cget("text")   # Crea la celda con color de fondo gris
                if pax == "": pax = "0"                             # Si no hay pax pone una cadena vacía
                valor += int(pax)                                   # Suma un pax
                valorTotal += int(pax)                              # Suma un pax
            num = "0390" + str(fila)                                # Crea el número de la celda
            globals()['VIEW%s' % num].config(text = str(valor))     # Crea la celda con color de fondo gris     
        num = "039032"                                              # Crea el número de la celda
        # Crea la celda con color de fondo gris
        globals()['VIEW%s' % num].config(text = str(valorTotal), font =("Helvetica",9,"bold"))                  
        # Elimina columnas sin datos y limpia su casilla de hora
        for columna in range(1,39):                                 # Recorre las horas del día
            num = "0" + str(columna) + "032"                        # Crea el número de la celda
            pax = globals()['VIEW%s' % num].cget("text")            # Crea la celda con color de fondo gris
            if pax == "0":                                          # Si no hay pax pone una cadena vacía
                globals()['VIEW%s' % num].config(text = "")         # Crea la celda con color de fondo gris
                num = "0" + str(columna) + "00"                     # Crea el número de la celda
                globals()['VIEW%s' % num].config(text = "")         # Crea la celda con color de fondo gris
                for fila in range (33):                             # Recorre los días del mes
                    num = "0" + str(columna) + "0" + str(fila)      # Crea el número de la celda
                    globals()['VIEW%s' % num].config(width = 0)     # Crea la celda con color de fondo gris
        # Boton de cerrar ventana    
        ventanaTabla.protocol("WM_DELETE_WINDOW", BotonRegresarForzado)        
        Boton7activado(PDFTablasPax)                                # Activa boton pdf
                          
    destruye_espacios_info(10,22)                       # Destruimos las labels de informacion para no sobrecargar el sistema
    ventanaTablas('Taula Pax',[0,0,3,300,50,"green"])   # Creamos ventana extra para esta tabla
    crea_espacios_info(frameTabla,40,33)             # Cramos las labels dentro de la tabla
    # Ajustamos las labels
    ajusta_espacios_info(40,33,8,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8)           
    menusBotones("Tornar",preMenuTablas,"Pax")          # Preparamos la salida
    # Datos a rellenar
    OpcionesQuestionario(["X2",LR1,"ANY:",LRR12],
                         ["X2",LR2,"MES:",LRR22])
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaPax())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaPax())
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)           # Foco en el año
    Boton4activado2(menuTablasPaxMuestra)               # Activa la tabla
def menuTablasVGrupo                                ():
    
    def menuTablasVGrupoMuestra ():
        
        # Rescata valores
        v1,v2,v3,v4,v5,v6 = LRR12.get(),LRR22.get(),LRR32.get(),LRR42.get(),LRR52.get(),LRR62.get()
        # Coteja fallos
        muralla = False
        muralla,v4,v5,v6 = cotejaFecha(muralla,v4,LRR42,v5,LRR52,v6,LRR62)
        muralla,v1,v2,v3 = cotejaFecha(muralla,v1,LRR12,v2,LRR22,v3,LRR32)
        muralla = cotejaVacio(muralla,v1,LRR12)
        muralla = cotejaVacio(muralla,v2,LRR22)
        muralla = cotejaVacio(muralla,v3,LRR32)
        muralla = cotejaVacio(muralla,v4,LRR42)
        muralla = cotejaVacio(muralla,v5,LRR52)
        muralla = cotejaVacio(muralla,v6,LRR62)
        if muralla == True:
            LR23.config(fg = "red")
            return      
        LR23.config(text = "")                      # Limpia posibles mensajes anteriores innecesarios       
        # Importancia en la tabla
        ventanaTabla.deiconify()
        ventanaTabla.title('Taula per zones: desde ' +v1 + '/'+v2+'/'+v3+' fins '+v4+'/'+v5+'/'+v6+'.')

        # Terminamos de dibujar las necesidades de la tabla
        columna = 1                                 # Iniciamos la columna  
        for data in range (1,35,2):                 # Recorremos las columnas            
            fila = 0                                # Iniciamos la fila
            for dato in range (3):                  # Recorremos las filas                
                # Creamos la celda
                num = "0" + str(fila) + "0" + str(columna)
                # Crea la celda con color de fondo gris 
                globals()['VIEW%s' % num].config(bg = "#9A7048")
                fila += 1                           # Avanzamos la fila            
            columna += 2                            # Avanzamos la columna      
        columna = 0                                 # Iniciamos la columna
        for dato in range (35):                     # Recorremos las filas                 
            num = "000" + str(columna)              # Crea el número de la celda          
            if num == "0000":                       # Si es la primera celda           
                columna += 1                        # Avanzamos la columna           
            else:                                   # Si no es la primera celda
                # Crea la celda con color de fondo gris
                globals()['VIEW%s' % num].config(bg = "grey",fg = "#FFFFFF")
                columna += 1                        # Avanzamos la columna
        columna = 0                                 # Iniciamos la columna
        # Pinta Casillas fijas
        globals()['VIEW%s' % "0000"].config(text="ZONA")
        globals()['VIEW%s' % "0100"].config(text="VISITANTS")
        globals()['VIEW%s' % "0200"].config(text="TANT PER CENT")
        globals()['VIEW%s' % "0001"].config(text="REUS")
        globals()['VIEW%s' % "0002"].config(text="CATALUNYA")
        globals()['VIEW%s' % "00013"].config(text="ESPANYA")
        globals()['VIEW%s' % "00024"].config(text="INTERNACIONAL")        
        # Preparamos las listas por grupos
        todosOrigenes = open("files/origens.DAT")   # Abrimos el archivo con los datos
        todosOrigenes = list(todosOrigenes)         # Lo convertimos en lista
        OrigenReus = 0                              # Iniciamos el contador de Reus
        OrigenCatalunya = []                        # Iniciamos la lista de Catalunya
        OrigenEspanya = []                          # Iniciamos la lista de España
        OrigenInternacional = []                    # Iniciamos la lista de Internacional
        for todos in todosOrigenes:                 # Recorremos la lista           
            todosPartido = todos.split(",")         # Separamos los datos
            todosPartido = list(todosPartido)       # Lo convertimos en lista
            try:                                    # Si hay datos
                if todosPartido[1] == "CATALUNYA":  # Si es de Catalunya
                    # Añadimos a la lista de Catalunya
                    OrigenCatalunya.append([todosPartido[0],0])
                elif todosPartido[1] == "ESPANYA":  # Si es de España
                    # Añadimos a la lista de España
                    OrigenEspanya.append([todosPartido[0],0])
                # Si es de Internacional
                elif todosPartido[1] == "INTERNACIONAL":
                    # Añadimos a la lista de Internacional
                    OrigenInternacional.append([todosPartido[0],0])
            except:                                 # Si no hay datos
                pass                                # Pasamos a la siguiente iteración       
        # Abre archivo con los datos en el mes y año necesarios
        # Crea una base de datos o se conecta a una
        base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        c = base_datos.cursor()                     # Crea cursor
        # Query the database
        c.execute("SELECT * FROM bd_registros WHERE FECHA >= '"+v3+"/"+v2+"/"+v1+"' and FECHA <= '"+v6+"/"+v5+"/"+v4+"'")
        records = c.fetchall()                      # Obtiene todos los registros
        for reu in records:                         # Repasa dia cada registro para poner sumar a la lista adecuada    
            if reu[3] == "REUS":                    # Si es de Reus
                OrigenReus += 1                     # Suma uno al contador de Reus 
        suma = 0                                    # Iniciamos el contador de sumas
        for cat in OrigenCatalunya:                 # Recorremos la lista de Catalunya
            for cata in records:                    # Recorremos los registros
                # Si el origen del registro es igual al origen de la lista
                if cata[3] != "REUS" and cata[3] == cat[0]:
                    cat[1] += 1                     # Suma uno al contador de ese origen
            suma +=1                                # Suma uno al contador de sumas
        suma = 0                                    # Iniciamos el contador de sumas
        for esp in OrigenEspanya:                   # Recorremos la lista de España
            for espa in records:
                if espa[3] == esp[0]:
                    esp[1] += 1
            suma +=1     
        suma = 0                                    # Iniciamos el contador de sumas
        for inter in OrigenInternacional:           # Recorremos la lista de Internacional
            for inte in records:                    # Recorremos los registros
                if inte[3] == inter[0]:             # Si el origen del registro es igual al origen de la lista
                    inter[1] += 1                   # Suma uno al contador de ese origen
            suma +=1                                # Suma uno al contador de sumas
        # Listas finales para usar y valor global de pax
        OrigenCatalunya = sorted(OrigenCatalunya, key=lambda valor: valor[1],reverse = True)
        OrigenEspanya = sorted(OrigenEspanya, key=lambda valor: valor[1],reverse = True)
        OrigenInternacional = sorted(OrigenInternacional, key=lambda valor: valor[1],reverse = True)
        CantidadRegistros = len(records)
        # Pintamos datos
        globals()['VIEW%s' % "0101"].config(text=OrigenReus,font=("Helvetica",9,"bold"))
        try:
            circun = (OrigenReus*100)/CantidadRegistros
            circun = round(circun,2)
        except:
            circun = 0
        globals()['VIEW%s' % "0201"].config(text=str(circun)+" %",font=("Helvetica",9,"bold"))
        
        for a in range(10):
            circun = list(OrigenCatalunya[a])
            globals()['VIEW%s' % "000" + str(a+3)].config(text=str(circun[0]),foreground = "yellow")
            globals()['VIEW%s' % "010" + str(a+3)].config(text=str(circun[1]))
            try:
                circun1 = (circun[1]*100)/CantidadRegistros
                circun1 = round(circun1,2)
            except:
                circun1 = 0
            globals()['VIEW%s' % "020" + str(a+3)].config(text=str(circun1)+" %")
        TotalCat = 0
        for a in OrigenCatalunya:
            TotalCat += a[1]
        globals()['VIEW%s' % "0102"].config(text=TotalCat,font=("Helvetica",9,"bold"))
        try:
            circun = (TotalCat*100)/CantidadRegistros
            circun = round(circun,2)
        except:
            circun = 0
        globals()['VIEW%s' % "0202"].config(text=str(circun)+" %",font=("Helvetica",9,"bold"))

        for a in range(10):
            circun = list(OrigenEspanya[a])
            globals()['VIEW%s' % "000" + str(a+14)].config(text=str(circun[0]),foreground = "yellow")
            globals()['VIEW%s' % "010" + str(a+14)].config(text=str(circun[1]))
            try:
                circun1 = (circun[1]*100)/CantidadRegistros
                circun1 = round(circun1,2)
            except:
                circun1 = 0
            globals()['VIEW%s' % "020" + str(a+14)].config(text=str(circun1)+" %")
        TotalEsp = 0
        for a in OrigenEspanya:
            TotalEsp += a[1]
        globals()['VIEW%s' % "01013"].config(text=TotalEsp,font=("Helvetica",9,"bold"))
        try:
            circun = (TotalEsp*100)/CantidadRegistros
            circun = round(circun,2)
        except:
            circun = 0
        globals()['VIEW%s' % "02013"].config(text=str(circun)+" %",font=("Helvetica",9,"bold"))
        for a in range(10):
            circun = list(OrigenInternacional[a])
            globals()['VIEW%s' % "000" + str(a+25)].config(text=str(circun[0]),foreground = "yellow")
            globals()['VIEW%s' % "010" + str(a+25)].config(text=str(circun[1]))
            try:
                circun1 = (circun[1]*100)/CantidadRegistros
                circun1 = round(circun1,2)
            except:
                circun = 0        
            globals()['VIEW%s' % "020" + str(a+25)].config(text=str(circun1)+" %")                        
        TotalInt = 0
        for a in OrigenInternacional:
            TotalInt += a[1]
        globals()['VIEW%s' % "01024"].config(text=TotalInt,font=("Helvetica",9,"bold"))
        try:
            circun = (TotalInt*100)/CantidadRegistros
            circun = round(circun,2)
        except:
            circun = 0
        globals()['VIEW%s' % "02024"].config(text=str(circun)+" %",font=("Helvetica",9,"bold"))
        # Cierra archivo
        base_datos.close()
        # Boton de cerrar ventana    
        ventanaTabla.protocol("WM_DELETE_WINDOW", BotonRegresarForzado)                    
        # Activa boton pdf
        Boton7activado(PDFTablasVGrupos)
                          
    destruye_espacios_info(10,22)                       # Destruimos las labels de informacion para no sobrecargar el sistema
    ventanaTablas('Taula zones',[0,0,1,300,50,"green"]) # Creamos ventana extra para esta tabla
    crea_espacios_info(frameTabla,3,35)                 # Ajustamos las labels
    ajusta_espacios_info(3,35,20,15,15)                 # Ajustamos las labels
    # Preparamos la salida
    menusBotones("Tornar",preMenuTablas,"",regresaSinNada,"Visitants per zona")
    # Datos a rellenar
    OpcionesQuestionario(["X2",LR1,"desde DIA:",LRR12],
                         ["X2",LR2,"MES:",LRR22],
                         ["X2",LR3,"ANY:",LRR32],
                         ["X2",LR4,"fins DIA:",LRR42],
                         ["X2",LR5,"MES:",LRR52],
                         ["X2",LR6,"ANY:",LRR62])
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaGru())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaGru())    
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)           # Foco en el año
    Boton4activado2(menuTablasVGrupoMuestra)            # Activa la tabla
def menuTablasVProvincia                            ():
    def menuTablasVProvinciasMuestra ():
        
        # Rescata valores
        v1,v2,v3,v4,v5,v6 = LRR12.get(),LRR22.get(),LRR32.get(),LRR42.get(),LRR52.get(),LRR62.get()
        # Coteja fallos
        muralla = False
        muralla,v4,v5,v6 = cotejaFecha(muralla,v4,LRR42,v5,LRR52,v6,LRR62)
        muralla,v1,v2,v3 = cotejaFecha(muralla,v1,LRR12,v2,LRR22,v3,LRR32)
        muralla = cotejaVacio(muralla,v1,LRR12)
        muralla = cotejaVacio(muralla,v2,LRR22)
        muralla = cotejaVacio(muralla,v3,LRR32)
        muralla = cotejaVacio(muralla,v4,LRR42)
        muralla = cotejaVacio(muralla,v5,LRR52)
        muralla = cotejaVacio(muralla,v6,LRR62)
        if muralla == True:
            LR23.config(fg = "red")
            return         
        LR23.config(text = "")          # Limpia posibles mensajes anteriores innecesarios 
        # Importancia en la tabla
        ventanaTabla.deiconify()        # Desiconifica la ventana
        # Preparamos la salida
        ventanaTabla.title('Taula per Provincies: desde ' +v1 + '/'+v2+'/'+v3+' fins '+v4+'/'+v5+'/'+v6+'.')
        # Terminamos de dibujar las necesidades de la tabla
        columna = 1                     # Columna 0 es la de los nombres de las provincias
        for data in range (1,5,2):
            
            fila = 0
            for dato in range (4):
                
                num = "0" + str(fila) + "0" + str(columna)
                            
                globals()['VIEW%s' % num].config(bg = "#9A7048")
                fila += 1   
            
            columna += 2        
        columna = 0                     
        for dato in range (5):
            
            num = "000" + str(columna)
            
            if num == "0000":
                
                columna += 1
                
            else:
                
                globals()['VIEW%s' % num].config(bg = "grey",fg = "#FFFFFF")
                columna += 1
        columna = 0
        LR23.config(text = "")        # Limpia posibles mensajes anteriores innecesarios       
        # Pinta Casillas fijas
        globals()['VIEW%s' % "0000"].config(text="PROVÍNCIES")
        globals()['VIEW%s' % "0100"].config(text="VISITANTS")
        globals()['VIEW%s' % "0200"].config(text="TANT PER CENT")
        globals()['VIEW%s' % "0300"].config(text="% GLOBAL")
        globals()['VIEW%s' % "0001"].config(text="BARCELONA")
        globals()['VIEW%s' % "0002"].config(text="TARRAGONA")
        globals()['VIEW%s' % "0003"].config(text="LLEIDA")
        globals()['VIEW%s' % "0004"].config(text="GIRONA")
        
        # Preparamos las listas por grupos
        todosOrigenes = open("files/origens.DAT")
        todosOrigenes = list(todosOrigenes)
        todosBarcelona = open("files/BARCELONA.DAT")
        todosBarcelona  = list(todosBarcelona)
        todosTarragona = open("files/TARRAGONA.DAT")
        todosTarragona  = list(todosTarragona)
        todosLerida = open("files/LLEIDA.DAT")
        todosLerida  = list(todosLerida)
        todosGerona = open("files/GIRONA.DAT")
        todosGerona  = list(todosGerona)
        OrigenBarcelona = 0
        OrigenTarragona = 0
        OrigenLerida = 0
        OrigenGerona = 0
       
        # Abre archivo con los datos en el mes y año necesarios
        # Crea una base de datos o se conecta a una
        base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        # Crea cursor
        c = base_datos.cursor()
        # Query the database
        c.execute("SELECT * FROM bd_registros WHERE FECHA >= '"+v3+"/"+v2+"/"+v1+"' and FECHA <= '"+v6+"/"+v5+"/"+v4+"'")
        records = c.fetchall()

        # Repasa dia cada registro para poner sumar a la lista adecuada    
        for todos in records:
        
            for origenes in todosOrigenes:
                
                origenesPartido = origenes.split(",")
                origenesPartido = list(origenesPartido)  
                
                try:

                    if  todos[3] == origenesPartido[0]:
                        if origenesPartido[2] in todosBarcelona:
                            OrigenBarcelona +=1
                        if origenesPartido[2] in todosTarragona:
                            OrigenTarragona +=1
                        if origenesPartido[2] in todosLerida:
                            OrigenLerida +=1
                        if origenesPartido[2] in todosGerona:
                            OrigenGerona +=1
                except:
                    pass
           
        CantidadRegistros = len(records)
        TotalCatalunya = OrigenBarcelona+OrigenTarragona+OrigenLerida+OrigenGerona
        try:
            PorcienBarcelona = str(round((OrigenBarcelona*100)/TotalCatalunya,2))+" %"
        except:
            PorcienBarcelona = "0.0 %"
        try:
            PorcienTarragona = str(round((OrigenTarragona*100)/TotalCatalunya,2))+" %"
        except:
            PorcienTarragona = "0.0 %"
        try:
            PorcienGerona = str(round((OrigenGerona*100)/TotalCatalunya,2))+" %"
        except:
            PorcienGerona = "0.0 %"
        try:
            PorcienLerida = str(round((OrigenLerida*100)/TotalCatalunya,2))+" %"
        except:
            PorcienLerida = "0.0 %"
        try:
            PorcienTotalBarcelona = str(round((OrigenBarcelona*100)/CantidadRegistros,2))+" %"
        except:
            PorcienTotalBarcelona = "0.0 %"
        try:
            PorcienTotalTarragona = str(round((OrigenTarragona*100)/CantidadRegistros,2))+" %"
        except:
            PorcienTotalTarragona = "0.0 %"
        try:
            PorcienTotalGerona = str(round((OrigenGerona*100)/CantidadRegistros,2))+" %"
        except:
            PorcienTotalGerona = "0.0 %"
        try:
            PorcienTotalLerida = str(round((OrigenLerida*100)/CantidadRegistros,2))+" %"
        except:
            PorcienTotalLerida = "0.0 %"

        # Pintamos datos
        globals()['VIEW%s' % "0101"].config(text=OrigenBarcelona)
        globals()['VIEW%s' % "0102"].config(text=OrigenTarragona)
        globals()['VIEW%s' % "0103"].config(text=OrigenLerida)
        globals()['VIEW%s' % "0104"].config(text=OrigenGerona)

        globals()['VIEW%s' % "0201"].config(text=PorcienBarcelona)
        globals()['VIEW%s' % "0202"].config(text=PorcienTarragona)
        globals()['VIEW%s' % "0203"].config(text=PorcienLerida)
        globals()['VIEW%s' % "0204"].config(text=PorcienGerona)

        globals()['VIEW%s' % "0301"].config(text=PorcienTotalBarcelona)
        globals()['VIEW%s' % "0302"].config(text=PorcienTotalTarragona)
        globals()['VIEW%s' % "0303"].config(text=PorcienTotalLerida)
        globals()['VIEW%s' % "0304"].config(text=PorcienTotalGerona)

        
        # Cierra archivo
        base_datos.close()
        # Boton de cerrar ventana    
        ventanaTabla.protocol("WM_DELETE_WINDOW", BotonRegresarForzado)                    
        # Activa boton pdf
        Boton7activado(PDFTablasVProvincias)
                          
    destruye_espacios_info(10,22)                               # Destruimos las labels de informacion para no sobrecargar el sistema
    ventanaTablas('Taula Províncies',[0,0,1,300,50,"green"])    # Creamos ventana extra para esta tabla
    crea_espacios_info(frameTabla,4,5)                          # Cramos las labels dentro de la tabla
    ajusta_espacios_info(4,5,20,15,15,15)                       # Ajustamos las labels dentro de la tabla
    # Preparamos la salida
    menusBotones("Tornar",preMenuTablas,"",regresaSinNada,"",regresaSinNada,"Visitants per províncies")
    # Datos a rellenar
    OpcionesQuestionario(["X2",LR1,"desde DIA:",LRR12],
                         ["X2",LR2,"MES:",LRR22],
                         ["X2",LR3,"ANY:",LRR32],
                         ["X2",LR4,"fins DIA:",LRR42],
                         ["X2",LR5,"MES:",LRR52],
                         ["X2",LR6,"ANY:",LRR62])
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaGru())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaGru())   
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)                   # Foco en el año
    Boton4activado2(menuTablasVProvinciasMuestra)               # Activa la tabla
def menuTablasVComarca                              ():
    def menuTablasVComarcasMuestra ():
        
        # Rescata valores
        v1,v2,v3,v4,v5,v6 = LRR12.get(),LRR22.get(),LRR32.get(),LRR42.get(),LRR52.get(),LRR62.get()
        # Coteja fallos
        muralla = False
        muralla,v4,v5,v6 = cotejaFecha(muralla,v4,LRR42,v5,LRR52,v6,LRR62)
        muralla,v1,v2,v3 = cotejaFecha(muralla,v1,LRR12,v2,LRR22,v3,LRR32)
        muralla = cotejaVacio(muralla,v1,LRR12)
        muralla = cotejaVacio(muralla,v2,LRR22)
        muralla = cotejaVacio(muralla,v3,LRR32)
        muralla = cotejaVacio(muralla,v4,LRR42)
        muralla = cotejaVacio(muralla,v5,LRR52)
        muralla = cotejaVacio(muralla,v6,LRR62)
        if muralla == True:
            LR23.config(fg = "red")
            return      
        LR23.config(text = "")        # Limpia posibles mensajes anteriores innecesarios       
        # Importancia en la tabla
        ventanaTabla.deiconify()
        ventanaTabla.title('Taula per Comarca: desde ' +v1 + '/'+v2+'/'+v3+' fins '+v4+'/'+v5+'/'+v6+'.')

        # Terminamos de dibujar las necesidades de la tabla
        columna = 1   
        for data in range (1,11,2):
            
            fila = 0
            for dato in range (3):
                
                num = "0" + str(fila) + "0" + str(columna)
                            
                globals()['VIEW%s' % num].config(bg = "#9A7048")
                fila += 1   
            
            columna += 2        
        columna = 0
        for dato in range (11):
            
            num = "000" + str(columna)
            
            if num == "0000":
                
                columna += 1
                
            else:
                
                globals()['VIEW%s' % num].config(bg = "grey",fg = "#FFFFFF")
                columna += 1
        columna = 0
        def leeArchivo (archivo):
                
                # Abre el archivo
                f = open(archivo,"r")
                
                # Lee el archivo
                contenido = f.read()
                
                # Cierra el archivo
                f.close()
                
                # Devuelve el contenido
                return contenido
            
        # Pinta Casillas fijas
        globals()['VIEW%s' % "0000"].config(text="COMARCA")
        globals()['VIEW%s' % "0100"].config(text="PAX")
        globals()['VIEW%s' % "0200"].config(text="TANT PER CENT")
        
        # Crea una lista de nombre 'lista'
        lista = []
        # Cada dato de la lista BARCELONA.DAT separado con '\n' lo añadimos como lista a la lista 'lista'
        for i in leeArchivo("files/BARCELONA.DAT").split('\n'):
                    
                    lista.append(i.split(','))
        # Cada dato de la lista TARRAGONA.DAT separado con '\n' lo añadimos como lista a la lista 'lista'
        for i in leeArchivo("files/TARRAGONA.DAT").split('\n'):
                    
                    lista.append(i.split(','))                    
        # Cada dato de la lista LLEIDA.DAT separado con '\n' lo añadimos como lista a la lista 'lista'
        for i in leeArchivo("files/LLEIDA.DAT").split('\n'):
                    
                    lista.append(i.split(','))
        # Cada dato de la lista GIRONA.DAT separado con '\n' lo añadimos como lista a la lista 'lista'
        for i in leeArchivo("files/GIRONA.DAT").split('\n'):
                    
                    lista.append(i.split(','))         
        
        # Borra las listas vacias
        for i in lista:
                
                if i == ['']:
                    
                    lista.remove(i)
                    
        # A cada lista dentro de la lista le añadimos un segundo valor que es un string de valor "0"
        for i in lista:
                
                i.append("0")
                 
        # Abre archivo con los datos en el mes y año necesarios
        # Crea una base de datos o se conecta a una
        base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        # Crea cursor
        c = base_datos.cursor()
        # Query the database
        c.execute("SELECT * FROM bd_registros WHERE FECHA >= '"+v3+"/"+v2+"/"+v1+"' and FECHA <= '"+v6+"/"+v5+"/"+v4+"'")
        records = c.fetchall()
        # Guardamos el total de los registros de records
        CantidadRegistros = len(records)     
        
        # Revisamos record 
        for record in records:
            
            # Abrimos el archivo de ORIGENS.DAT
            f = open("files/ORIGENS.DAT","r")
            # Convierte a f en lista separando por '\n'
            f = f.read().split('\n')
            # Combierte cada dato de f en lista separando por ','
            for i in range(len(f)):
                f[i] = f[i].split(',')
                
            # Revisamos todos los datos de f
            for linea in f:
                
                # Si el dato 1 del registro de ORIGENS.DAT es igual al registro 3 de records
                if linea[0] == record[3]:
                    
                    # Buscamos el dato 1 de linea en lista
                    for i in lista:
                        # Si linea[0] y lista[i][0] son iguales
                        if linea[2] == i[0]:
                            # Aumentamos el valor de lista[i][1] en 1
                            i[1] = str(int(i[1]) + 1)
                            # Salimos del bucle
                            break
        # Organizamos lista de mayor a menor por el SEGUNDO elemento de sus listas  
        lista = sorted(lista, key=lambda valor: int(valor[1]),reverse = True)
     
        # Pintamos datos      
        for linea in range(10):
            circun = lista[linea]
            globals()['VIEW%s' % "000" + str(linea+1)].config(text=str(circun[0]),foreground = "yellow")
            globals()['VIEW%s' % "010" + str(linea+1)].config(text=str(circun[1]))
            try:
                circun1 = int(circun[1])
                circun1 = (circun1*100)/CantidadRegistros
                circun1 = round(circun1,2)
            except:
                circun1 = 0

            globals()['VIEW%s' % "020" + str(linea+1)].config(text=str(circun1)+" %")
        # Boton de cerrar ventana    
        ventanaTabla.protocol("WM_DELETE_WINDOW", BotonRegresarForzado)                    
        # Activa boton pdf
        Boton7activado(PDFTablasVComarcas)
                          
    # Destruimos las labels de informacion para no sobrecargar el sistema
    destruye_espacios_info(10,22)
    # Creamos ventana extra para esta tabla
    ventanaTablas('Taula Comarques',[0,0,1,300,50,"green"])      
    # Cramos las labels dentro de la tabla
    crea_espacios_info(frameTabla,3,11)
    ajusta_espacios_info(3,11,20,15,15)                
    # Preparamos la salida
    menusBotones("Tornar",preMenuTablas,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Visitants per comarca")
    # Datos a rellenar
    OpcionesQuestionario(["X2",LR1,"desde DIA:",LRR12],
                         ["X2",LR2,"MES:",LRR22],
                         ["X2",LR3,"ANY:",LRR32],
                         ["X2",LR4,"fins DIA:",LRR42],
                         ["X2",LR5,"MES:",LRR52],
                         ["X2",LR6,"ANY:",LRR62])
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaGru())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaGru())    
    # Foco en el año
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
    # Activa la tabla
    Boton4activado2(menuTablasVComarcasMuestra)
def menuTablasVPerfil                               ():
    def menuTablasVPerfilesMuestra ():
        
        # Rescata valores
        v1,v2,v3,v4,v5,v6 = LRR12.get(),LRR22.get(),LRR32.get(),LRR42.get(),LRR52.get(),LRR62.get()
        # Coteja fallos
        muralla = False
        muralla,v4,v5,v6 = cotejaFecha(muralla,v4,LRR42,v5,LRR52,v6,LRR62)
        muralla,v1,v2,v3 = cotejaFecha(muralla,v1,LRR12,v2,LRR22,v3,LRR32)
        muralla = cotejaVacio(muralla,v1,LRR12)
        muralla = cotejaVacio(muralla,v2,LRR22)
        muralla = cotejaVacio(muralla,v3,LRR32)
        muralla = cotejaVacio(muralla,v4,LRR42)
        muralla = cotejaVacio(muralla,v5,LRR52)
        muralla = cotejaVacio(muralla,v6,LRR62)
        if muralla == True:
            LR23.config(fg = "red")
            return      
        LR23.config(text = "")        # Limpia posibles mensajes anteriores innecesarios       
        # Importancia en la tabla
        ventanaTabla.deiconify()
        ventanaTabla.title('Taula per perfils: desde ' +v1 + '/'+v2+'/'+v3+' fins '+v4+'/'+v5+'/'+v6+'.')

        # Terminamos de dibujar las necesidades de la tabla
        columna = 1   
        for data in range (1,11,2):
            
            fila = 0
            for dato in range (3):
                
                num = "0" + str(fila) + "0" + str(columna)
                            
                globals()['VIEW%s' % num].config(bg = "#9A7048")
                fila += 1   
            
            columna += 2        
        columna = 0
        for dato in range (11):
            
            num = "000" + str(columna)
            
            if num == "0000":
                
                columna += 1
                
            else:
                
                globals()['VIEW%s' % num].config(bg = "grey",fg = "#FFFFFF")
                columna += 1
        columna = 0

        # Pinta Casillas fijas
        globals()['VIEW%s' % "0000"].config(text="PERFIL")
        globals()['VIEW%s' % "0100"].config(text="PAX")
        globals()['VIEW%s' % "0200"].config(text="TANT PER CENT")
        
        # Abrimos el archivo de las descripciones
        archivo = open("files/DESCRIPCIONS.DAT","r")
        # Convertimos en lista de listas
        lista = []
        # itera sobre cada línea del archivo
        for datos in archivo:
        # divide cada línea en una lista utilizando la función split() y almacena
        # el resultado en la lista de datos
            lista.append(datos.split('\n'))
        
        # Revisa que todas las listas de lista tengan "0" en la posición 1
        # Si no es así, le pone "0" en la posición 1
        for i in lista:
            if (i[1]) == "":
                    i[1] = "0" 
    
      
        # Cerramos el archivo
        archivo.close()
                    
        # Abre archivo con los datos en el mes y año necesarios
        # Crea una base de datos o se conecta a una
        base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        # Crea cursor
        c = base_datos.cursor()
        # Query the database
        c.execute("SELECT * FROM bd_registros WHERE FECHA >= '"+v3+"/"+v2+"/"+v1+"' and FECHA <= '"+v6+"/"+v5+"/"+v4+"'")
        records = c.fetchall()
        # Guardamos el total de los registros de records
        CantidadRegistros = len(records)
        
        # Revisamos record 
        for record in records:
                
                # Revisamos la lista
                for linea in lista:
                    # Si coincide el campo 2 de record con el campo 1 de linea
                    if record[2] == linea[0]:
                        # +1 al campo 1 de linea
                        try:
                            valor = linea[1]
                            valor = int(valor)
                            valor += 1
                            linea[1] = str(valor)
                        except:
                            linea[1] = 1

                        # Salimos del bucle
                        break
                                           
        # Organizamos lista de mayor a menor por el SEGUNDO elemento de sus listas  
        lista = sorted(lista, key=lambda valor: str(valor[1]),reverse = True)
     
        # Pintamos datos      
        for linea in range(10):
            circun = lista[linea]
            globals()['VIEW%s' % "000" + str(linea+1)].config(text=str(circun[0]),foreground = "yellow")
            globals()['VIEW%s' % "010" + str(linea+1)].config(text=str(circun[1]))
            try:
                circun1 = int(circun[1])
                circun1 = (circun1*100)/CantidadRegistros
                circun1 = round(circun1,2)
            except:
                circun1 = 0

            globals()['VIEW%s' % "020" + str(linea+1)].config(text=str(circun1)+" %")
        # Boton de cerrar ventana    
        ventanaTabla.protocol("WM_DELETE_WINDOW", BotonRegresarForzado)                    
        # Activa boton pdf
        Boton7activado(PDFTablasVPerfiles)
                          
    # Destruimos las labels de informacion para no sobrecargar el sistema
    destruye_espacios_info(10,22)
    
    # Creamos ventana extra para esta tabla
    ventanaTablas('Taula perfils',[0,0,1,300,50,"green"])
    # Cramos las labels dentro de la tabla
    crea_espacios_info(frameTabla,3,11)
    ajusta_espacios_info(3,11,20,15,15)                 
    # Preparamos la salida
    menusBotones("Tornar",preMenuTablas,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Visitants per perfil")
    # Datos a rellenar
    OpcionesQuestionario(["X2",LR1,"desde DIA:",LRR12],
                         ["X2",LR2,"MES:",LRR22],
                         ["X2",LR3,"ANY:",LRR32],
                         ["X2",LR4,"fins DIA:",LRR42],
                         ["X2",LR5,"MES:",LRR52],
                         ["X2",LR6,"ANY:",LRR62])
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaGru())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaGru())    
    # Foco en el año
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
    # Activa la tabla
    Boton4activado2(menuTablasVPerfilesMuestra)
def menuTablasVFuente                               ():
    def menuTablasVFuentesMuestra ():
        
        # Rescata valores
        v1,v2,v3,v4,v5,v6 = LRR12.get(),LRR22.get(),LRR32.get(),LRR42.get(),LRR52.get(),LRR62.get()
        # Coteja fallos
        muralla = False
        muralla,v4,v5,v6 = cotejaFecha(muralla,v4,LRR42,v5,LRR52,v6,LRR62)
        muralla,v1,v2,v3 = cotejaFecha(muralla,v1,LRR12,v2,LRR22,v3,LRR32)
        muralla = cotejaVacio(muralla,v1,LRR12)
        muralla = cotejaVacio(muralla,v2,LRR22)
        muralla = cotejaVacio(muralla,v3,LRR32)
        muralla = cotejaVacio(muralla,v4,LRR42)
        muralla = cotejaVacio(muralla,v5,LRR52)
        muralla = cotejaVacio(muralla,v6,LRR62)
        if muralla == True:
            LR23.config(fg = "red")
            return      
        LR23.config(text = "")        # Limpia posibles mensajes anteriores innecesarios       
        # Importancia en la tabla
        ventanaTabla.deiconify()
        ventanaTabla.title('Taula per perfils: desde ' +v1 + '/'+v2+'/'+v3+' fins '+v4+'/'+v5+'/'+v6+'.')

        # Terminamos de dibujar las necesidades de la tabla
        columna = 1   
        for data in range (1,11,2):
            
            fila = 0
            for dato in range (3):
                
                num = "0" + str(fila) + "0" + str(columna)
                            
                globals()['VIEW%s' % num].config(bg = "#9A7048")
                fila += 1   
            
            columna += 2        
        columna = 0
        for dato in range (11):
            
            num = "000" + str(columna)
            
            if num == "0000":
                
                columna += 1
                
            else:
                
                globals()['VIEW%s' % num].config(bg = "grey",fg = "#FFFFFF")
                columna += 1
        columna = 0

        # Pinta Casillas fijas
        globals()['VIEW%s' % "0000"].config(text="FONT")
        globals()['VIEW%s' % "0100"].config(text="PAX")
        globals()['VIEW%s' % "0200"].config(text="TANT PER CENT")
        
        # Abrimos el archivo de las descripciones
        archivo = open("files/FONTS.DAT","r")
        # Convertimos en lista de listas
        lista = []
        # itera sobre cada línea del archivo
        for datos in archivo:
        # divide cada línea en una lista utilizando la función split() y almacena
        # el resultado en la lista de datos
            lista.append(datos.split('\n'))
        
        # Revisa que todas las listas de lista tengan "0" en la posición 1
        # Si no es así, le pone "0" en la posición 1
        for i in lista:
            if (i[1]) == "":
                    i[1] = "0" 
    
      
        # Cerramos el archivo
        archivo.close()
                    
        # Abre archivo con los datos en el mes y año necesarios
        # Crea una base de datos o se conecta a una
        base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        # Crea cursor
        c = base_datos.cursor()
        # Query the database
        c.execute("SELECT * FROM bd_registros WHERE FECHA >= '"+v3+"/"+v2+"/"+v1+"' and FECHA <= '"+v6+"/"+v5+"/"+v4+"'")
        records = c.fetchall()
        # Guardamos el total de los registros de records
        CantidadRegistros = len(records)
        
        # Revisamos record 
        for record in records:
                
                # Revisamos la lista
                for linea in lista:
                    # Si coincide el campo 2 de record con el campo 1 de linea
                    if record[6] == linea[0]:
                        # +1 al campo 1 de linea
                        try:
                            valor = linea[1]
                            valor = int(valor)
                            valor += 1
                            linea[1] = str(valor)
                        except:
                            linea[1] = 1

                        # Salimos del bucle
                        break
                                           
        # Organizamos lista de mayor a menor por el SEGUNDO elemento de sus listas  
        lista = sorted(lista, key=lambda valor: int(valor[1]),reverse = True)
    
        # Pintamos datos      
        for linea in range(10):
            circun = lista[linea]
            globals()['VIEW%s' % "000" + str(linea+1)].config(text=str(circun[0]),foreground = "yellow")
            globals()['VIEW%s' % "010" + str(linea+1)].config(text=str(circun[1]))
            try:
                circun1 = int(circun[1])
                circun1 = (circun1*100)/CantidadRegistros
                circun1 = round(circun1,2)
            except:
                circun1 = 0

            globals()['VIEW%s' % "020" + str(linea+1)].config(text=str(circun1)+" %")
        # Boton de cerrar ventana    
        ventanaTabla.protocol("WM_DELETE_WINDOW", BotonRegresarForzado)                           
        # Activa boton pdf
        Boton7activado(PDFTablasVFuentes)
                          
    # Destruimos las labels de informacion para no sobrecargar el sistema
    destruye_espacios_info(10,22)
    # Creamos ventana extra para esta tabla
    ventanaTablas('Taula fonts',[0,0,1,300,50,"green"])
    # Cramos las labels dentro de la tabla
    crea_espacios_info(frameTabla,3,11)
    ajusta_espacios_info(3,11,20,15,15)                
    # Preparamos la salida
    menusBotones("Tornar",preMenuTablas,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Visitants per font")
    # Datos a rellenar
    OpcionesQuestionario(["X2",LR1,"desde DIA:",LRR12],
                         ["X2",LR2,"MES:",LRR22],
                         ["X2",LR3,"ANY:",LRR32],
                         ["X2",LR4,"fins DIA:",LRR42],
                         ["X2",LR5,"MES:",LRR52],
                         ["X2",LR6,"ANY:",LRR62])
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaGru())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaGru())    
    # Foco en el año
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
    # Activa la tabla
    Boton4activado2(menuTablasVFuentesMuestra)
def menuTablasVHora                                 ():
    def menuTablasVHorasMuestra ():
        
        # Rescata valores
        v1,v2,v3,v4,v5,v6 = LRR12.get(),LRR22.get(),LRR32.get(),LRR42.get(),LRR52.get(),LRR62.get()
        # Coteja fallos
        muralla = False
        muralla,v4,v5,v6 = cotejaFecha(muralla,v4,LRR42,v5,LRR52,v6,LRR62)
        muralla,v1,v2,v3 = cotejaFecha(muralla,v1,LRR12,v2,LRR22,v3,LRR32)
        muralla = cotejaVacio(muralla,v1,LRR12)
        muralla = cotejaVacio(muralla,v2,LRR22)
        muralla = cotejaVacio(muralla,v3,LRR32)
        muralla = cotejaVacio(muralla,v4,LRR42)
        muralla = cotejaVacio(muralla,v5,LRR52)
        muralla = cotejaVacio(muralla,v6,LRR62)
        if muralla == True:
            LR23.config(fg = "red")
            return      
        LR23.config(text = "")        # Limpia posibles mensajes anteriores innecesarios       
        # Importancia en la tabla
        ventanaTabla.deiconify()
        ventanaTabla.title('Taula per hores: desde ' +v1 + '/'+v2+'/'+v3+' fins '+v4+'/'+v5+'/'+v6+'.')
        # Terminamos de dibujar las necesidades de la tabla
        columna = 1   
        for data in range (1,11,2):
            
            fila = 0
            for dato in range (3):
                
                num = "0" + str(fila) + "0" + str(columna)
                            
                globals()['VIEW%s' % num].config(bg = "#9A7048")
                fila += 1   
            
            columna += 2        
        columna = 0
        for dato in range (11):
            
            num = "000" + str(columna)
            
            if num == "0000":
                
                columna += 1
                
            else:
                
                globals()['VIEW%s' % num].config(bg = "grey",fg = "#FFFFFF")
                columna += 1
        columna = 0

        # Pinta Casillas fijas
        globals()['VIEW%s' % "0000"].config(text="HORES")
        globals()['VIEW%s' % "0100"].config(text="PAX")
        globals()['VIEW%s' % "0200"].config(text="TANT PER CENT")
        
        # Abrimos el archivo de las descripciones
        archivo = open("files/HORARIS.DAT","r")
        # Convertimos en lista de listas
        lista = []
        # itera sobre cada línea del archivo
        for datos in archivo:
        # divide cada línea en una lista utilizando la función split() y almacena
        # el resultado en la lista de datos
            lista.append(datos.split('\n'))
        
        # Revisa que todas las listas de lista tengan "0" en la posición 1
        # Si no es así, le pone "0" en la posición 1
        for i in lista:
            if (i[1]) == "":
                    i[1] = "0" 
    
      
        # Cerramos el archivo
        archivo.close()
                    
        # Abre archivo con los datos en el mes y año necesarios
        # Crea una base de datos o se conecta a una
        base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        # Crea cursor
        c = base_datos.cursor()
        # Query the database
        c.execute("SELECT * FROM bd_registros WHERE FECHA >= '"+v3+"/"+v2+"/"+v1+"' and FECHA <= '"+v6+"/"+v5+"/"+v4+"'")
        records = c.fetchall()
        # Guardamos el total de los registros de records
        CantidadRegistros = len(records)
        
        # Revisamos record 
        for record in records:
                
                # Revisamos la lista
                for linea in lista:
                    # Si coincide el campo 2 de record con el campo 1 de linea
                    if record[4] == linea[0]:
                        # +1 al campo 1 de linea
                        try:
                            valor = linea[1]
                            valor = int(valor)
                            valor += 1
                            linea[1] = str(valor)
                        except:
                            linea[1] = 1

                        # Salimos del bucle
                        break
                                           
        # Organizamos lista de mayor a menor por el SEGUNDO elemento de sus listas  
        lista = sorted(lista, key=lambda valor: int(valor[1]),reverse = True)
     
        # Pintamos datos      
        for linea in range(10):
            circun = lista[linea]
            globals()['VIEW%s' % "000" + str(linea+1)].config(text=str(circun[0]),foreground = "yellow")
            globals()['VIEW%s' % "010" + str(linea+1)].config(text=str(circun[1]))
            try:
                circun1 = int(circun[1])
                circun1 = (circun1*100)/CantidadRegistros
                circun1 = round(circun1,2)
            except:
                circun1 = 0

            globals()['VIEW%s' % "020" + str(linea+1)].config(text=str(circun1)+" %")
        # Boton de cerrar ventana    
        ventanaTabla.protocol("WM_DELETE_WINDOW", BotonRegresarForzado)                       
        # Activa boton pdf
        Boton7activado(PDFTablasVHoras)
                          
    # Destruimos las labels de informacion para no sobrecargar el sistema
    destruye_espacios_info(10,22)
# Creamos ventana extra para esta tabla
    ventanaTablas('Taula hores',[0,0,1,300,50,"green"])
    # Cramos las labels dentro de la tabla
    crea_espacios_info(frameTabla,3,11)
    ajusta_espacios_info(3,11,20,15,15)                 
    # Preparamos la salida
    menusBotones("Tornar",preMenuTablas,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Visitants per hora")
    # Datos a rellenar
    OpcionesQuestionario(["X2",LR1,"desde DIA:",LRR12],
                         ["X2",LR2,"MES:",LRR22],
                         ["X2",LR3,"ANY:",LRR32],
                         ["X2",LR4,"fins DIA:",LRR42],
                         ["X2",LR5,"MES:",LRR52],
                         ["X2",LR6,"ANY:",LRR62])
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaGru())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaGru())    
    # Foco en el año
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
    # Activa la tabla
    Boton4activado2(menuTablasVHorasMuestra)
def menuTablasVDia                                  ():
    def menuTablasVDiasMuestra ():
        
        # Rescata valores
        v1,v2,v3,v4,v5,v6 = LRR12.get(),LRR22.get(),LRR32.get(),LRR42.get(),LRR52.get(),LRR62.get()
        # Coteja fallos
        muralla = False
        muralla,v4,v5,v6 = cotejaFecha(muralla,v4,LRR42,v5,LRR52,v6,LRR62)
        muralla,v1,v2,v3 = cotejaFecha(muralla,v1,LRR12,v2,LRR22,v3,LRR32)
        muralla = cotejaVacio(muralla,v1,LRR12)
        muralla = cotejaVacio(muralla,v2,LRR22)
        muralla = cotejaVacio(muralla,v3,LRR32)
        muralla = cotejaVacio(muralla,v4,LRR42)
        muralla = cotejaVacio(muralla,v5,LRR52)
        muralla = cotejaVacio(muralla,v6,LRR62)
        if muralla == True:
            LR23.config(fg = "red")
            return      
        LR23.config(text = "")        # Limpia posibles mensajes anteriores innecesarios       
        # Importancia en la tabla
        ventanaTabla.deiconify()
        ventanaTabla.title('Taula per dies: desde ' +v1 + '/'+v2+'/'+v3+' fins '+v4+'/'+v5+'/'+v6+'.')

        # Terminamos de dibujar las necesidades de la tabla
        columna = 1   
        for data in range (1,12,2):
            
            fila = 0
            for dato in range (3):
                
                num = "0" + str(fila) + "0" + str(columna)
                            
                globals()['VIEW%s' % num].config(bg = "#9A7048")
                fila += 1   
            
            columna += 2        
        columna = 0
        for dato in range (12):
            
            num = "000" + str(columna)
            
            if num == "0000":
                
                columna += 1
                
            else:
                
                globals()['VIEW%s' % num].config(bg = "grey",fg = "#FFFFFF")
                columna += 1
        columna = 0
        globals()['VIEW%s' % "0106"].config(bg = "grey",fg = "#FFFFFF")
        globals()['VIEW%s' % "0206"].config(bg = "grey",fg = "#FFFFFF")

        # Pinta Casillas fijas
        globals()['VIEW%s' % "0000"].config(text="DIES MILLORS")
        globals()['VIEW%s' % "0006"].config(text="DIES PITJORS")
        globals()['VIEW%s' % "0100"].config(text="PAX")
        globals()['VIEW%s' % "0200"].config(text="TANT PER CENT")
        globals()['VIEW%s' % "0106"].config(text="PAX")
        globals()['VIEW%s' % "0206"].config(text="TANT PER CENT")                                  
        # Abre archivo con los datos en el mes y año necesarios
        # Crea una base de datos o se conecta a una
        base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        # Crea cursor
        c = base_datos.cursor()
        # Query the database
        c.execute("SELECT * FROM bd_registros WHERE FECHA >= '"+v3+"/"+v2+"/"+v1+"' and FECHA <= '"+v6+"/"+v5+"/"+v4+"'")
        records = c.fetchall()
        
        # Crea una lista de listas de nombre 'lista' con 2 elementos cada una
        # El primer elemento es cada una de las fechas de "c" y el segundo elemento es un 0
        lista = []
        for record in records:
            lista.append([record[1],0])
        # Elimina las listas repetidas de la lista
        lista = list(set(tuple(i) for i in lista))
        # Convierte la tupla en una lista de listas
        lista = [list(elem) for elem in lista]
                
        # Guardamos el total de los registros de records
        CantidadRegistros = len(records)

        # Revisamos record 
        for record in records:
                
                # Revisamos la lista
                for linea in lista:
                    # Si coincide el campo 2 de record con el campo 1 de linea
                    if record[1] == linea[0]:
                        # +1 al campo 1 de linea
                        try:
                            valor = linea[1]
                            valor = int(valor)
                            valor += 1
                            linea[1] = str(valor)
                        except:
                            linea[1] = 1

                        # Salimos del bucle
                        break
        
        try:
            # Organizamos lista de mayor a menor por el SEGUNDO elemento de sus listas  
            lista = sorted(lista, key=lambda valor: int(valor[1]),reverse = True)
            # Pintamos datos      
            for linea in range(5):
                circun = lista[linea]
                globals()['VIEW%s' % "000" + str(linea+1)].config(text=str(circun[0]),foreground = "yellow")
                globals()['VIEW%s' % "010" + str(linea+1)].config(text=str(circun[1]))
                try:
                    circun1 = int(circun[1])
                    circun1 = (circun1*100)/CantidadRegistros
                    circun1 = round(circun1,2)
                except:
                    circun1 = 0

                globals()['VIEW%s' % "020" + str(linea+1)].config(text=str(circun1)+" %")
        except:
            pass
        
        try:
            # Organizamos lista de menor a mayor por el SEGUNDO elemento de sus listas  
            lista = sorted(lista, key=lambda valor: int(valor[1]),reverse = False)
            # Pintamos datos      
            for linea in range(5):
                circun = lista[linea]
                globals()['VIEW%s' % "000" + str(linea+7)].config(text=str(circun[0]),foreground = "yellow")
                globals()['VIEW%s' % "010" + str(linea+7)].config(text=str(circun[1]))
                try:
                    circun1 = int(circun[1])
                    circun1 = (circun1*100)/CantidadRegistros
                    circun1 = round(circun1,2)
                except:
                    circun1 = 0

                globals()['VIEW%s' % "020" + str(linea+7)].config(text=str(circun1)+" %")
        except:
            pass
        # Boton de cerrar ventana    
        ventanaTabla.protocol("WM_DELETE_WINDOW", BotonRegresarForzado)                    
        # Activa boton pdf
        Boton7activado(PDFTablasVDias)
                          
    # Destruimos las labels de informacion para no sobrecargar el sistema
    destruye_espacios_info(10,22)
    # Creamos ventana extra para esta tabla
    ventanaTablas('Taula dies',[0,0,1,300,50,"green"])       
    # Cramos las labels dentro de la tabla
    crea_espacios_info(frameTabla,3,12)
    ajusta_espacios_info(3,12,20,15,15)                
    # Preparamos la salida
    menusBotones("Tornar",preMenuTablas,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Visitants per dia")
    # Datos a rellenar
    OpcionesQuestionario(["X2",LR1,"desde DIA:",LRR12],
                         ["X2",LR2,"MES:",LRR22],
                         ["X2",LR3,"ANY:",LRR32],
                         ["X2",LR4,"fins DIA:",LRR42],
                         ["X2",LR5,"MES:",LRR52],
                         ["X2",LR6,"ANY:",LRR62])
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaGru())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaGru())    
    # Foco en el año
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
    # Activa la tabla
    Boton4activado2(menuTablasVDiasMuestra)
def menuTablasVOrigen                               ():
    def menuTablasVOrigenesMuestra ():
        
        # Rescata valores
        v1,v2,v3,v4,v5,v6 = LRR12.get(),LRR22.get(),LRR32.get(),LRR42.get(),LRR52.get(),LRR62.get()
        # Coteja fallos
        muralla = False
        muralla,v4,v5,v6 = cotejaFecha(muralla,v4,LRR42,v5,LRR52,v6,LRR62)
        muralla,v1,v2,v3 = cotejaFecha(muralla,v1,LRR12,v2,LRR22,v3,LRR32)
        muralla = cotejaVacio(muralla,v1,LRR12)
        muralla = cotejaVacio(muralla,v2,LRR22)
        muralla = cotejaVacio(muralla,v3,LRR32)
        muralla = cotejaVacio(muralla,v4,LRR42)
        muralla = cotejaVacio(muralla,v5,LRR52)
        muralla = cotejaVacio(muralla,v6,LRR62)
        if muralla == True:
            LR23.config(fg = "red")
            return      
        LR23.config(text = "")        # Limpia posibles mensajes anteriores innecesarios       
        # Importancia en la tabla
        ventanaTabla.deiconify()
        ventanaTabla.title('Taula per Origens: desde ' +v1 + '/'+v2+'/'+v3+' fins '+v4+'/'+v5+'/'+v6+'.')
        # Terminamos de dibujar las necesidades de la tabla
        columna = 1   
        for data in range (1,11,2):
            
            fila = 0
            for dato in range (3):
                
                num = "0" + str(fila) + "0" + str(columna)
                            
                globals()['VIEW%s' % num].config(bg = "#9A7048")
                fila += 1   
            
            columna += 2        
        columna = 0
        for dato in range (11):
            
            num = "000" + str(columna)
            
            if num == "0000":
                
                columna += 1
                
            else:
                
                globals()['VIEW%s' % num].config(bg = "grey",fg = "#FFFFFF")
                columna += 1
        columna = 0
        # Pinta Casillas fijas
        globals()['VIEW%s' % "0000"].config(text="ORIGENS")
        globals()['VIEW%s' % "0100"].config(text="PAX")
        globals()['VIEW%s' % "0200"].config(text="TANT PER CENT")        
        # Abrimos el archivo de las descripciones
        archivo = open("files/ORIGENS.DAT","r")
        # Convertimos en lista de listas
        lista = []
        # itera sobre cada línea del archivo
        for datos in archivo:
        # divide cada línea en una lista utilizando la función split() y almacena
        # el resultado en la lista de datos
            lista.append(datos.split('\n'))
        
        # De todas las listas de lista borra todo lo que hay en la posición 1 a partir de la prmera ","
        for i in lista:
            i[0] = i[0].split(",")[0]
            
        # Revisa que todas las listas de lista tengan "0" en la posición 1
        # Si no es así, le pone "0" en la posición 1
        for i in lista:
            if (i[1]) != "0":
                    i[1] = "0" 
    
      
        # Cerramos el archivo
        archivo.close()
                    
        # Abre archivo con los datos en el mes y año necesarios
        # Crea una base de datos o se conecta a una
        base_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        # Crea cursor
        c = base_datos.cursor()
        # Query the database
        c.execute("SELECT * FROM bd_registros WHERE FECHA >= '"+v3+"/"+v2+"/"+v1+"' and FECHA <= '"+v6+"/"+v5+"/"+v4+"'")
        records = c.fetchall()
        # Guardamos el total de los registros de records
        CantidadRegistros = len(records)
        
        # Revisamos record 
        for record in records:
                
                # Revisamos la lista
                for linea in lista:
                    # Si coincide el campo 2 de record con el campo 1 de linea
                    if record[3] == linea[0]:
                        # +1 al campo 1 de linea
                        try:
                            valor = linea[1]
                            valor = int(valor)
                            valor += 1
                            linea[1] = str(valor)
                        except:
                            linea[1] = 1

                        # Salimos del bucle
                        break
                                           
        # Organizamos lista de mayor a menor por el SEGUNDO elemento de sus listas  
        lista = sorted(lista, key=lambda valor: int(valor[1]),reverse = True)
     
        # Pintamos datos      
        for linea in range(10):
            circun = lista[linea]
            globals()['VIEW%s' % "000" + str(linea+1)].config(text=str(circun[0]),foreground = "yellow")
            globals()['VIEW%s' % "010" + str(linea+1)].config(text=str(circun[1]))
            try:
                circun1 = int(circun[1])
                circun1 = (circun1*100)/CantidadRegistros
                circun1 = round(circun1,2)
            except:
                circun1 = 0

            globals()['VIEW%s' % "020" + str(linea+1)].config(text=str(circun1)+" %")
        # Boton de cerrar ventana    
        ventanaTabla.protocol("WM_DELETE_WINDOW", BotonRegresarForzado)                           
        # Activa boton pdf
        Boton7activado(PDFTablasVOrigen)
                          
    # Destruimos las labels de informacion para no sobrecargar el sistema
    destruye_espacios_info(10,22)
    # Creamos ventana extra para esta tabla
    ventanaTablas('Taula origens',[0,0,1,300,50,"green"])
    # Cramos las labels dentro de la tabla
    crea_espacios_info(frameTabla,3,11)
    ajusta_espacios_info(3,11,20,15,15)                 
    # Preparamos la salida
    menusBotones("Tornar",preMenuTablas,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Visitants per origen")
    # Datos a rellenar
    OpcionesQuestionario(["X2",LR1,"desde DIA:",LRR12],
                         ["X2",LR2,"MES:",LRR22],
                         ["X2",LR3,"ANY:",LRR32],
                         ["X2",LR4,"fins DIA:",LRR42],
                         ["X2",LR5,"MES:",LRR52],
                         ["X2",LR6,"ANY:",LRR62])
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaGru())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaGru())    
    # Foco en el año
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
    # Activa la tabla
    Boton4activado2(menuTablasVOrigenesMuestra)

def menuArqueos                                 ():
    
    return # Mientras no se haga el arqueo no se puede acceder a este menú

    if  nomUsuario.cget("text") == "":

        return
    global usuarioNivel
    if int(usuarioNivel) >= 4:
        return
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    LimpiaLabelsRellena()
    textMenu.config(text = "MENU ARQUEIJOS")   
    menusBotones("Tornar",MenuInicial,"Arqueig diari",menuArqueoDiario,"Arqueig global",regresaSinNada,"Resum econòmic parcial")         
    BM1.focus()
def menuArqueoDiario                                ():

    LimpiaLabelsRellena()   
    textMenu.config(text = "ARQUEIG DIARI")   
    menusBotones("Tornar",menuArqueos,"Matí",menuArqueoDiarioMatí,"Tarda",menuArqueoDiarioTarde)         
def menuArqueoDiarioMatí                                ():

    # Carga los datos en zona 3 del arqueo de mañana de ese día
    return
def menuArqueoDiarioTarde                               ():
    
    # Carga los datos en zona 3 del arqueo de tarde de ese día
    return                            

def menuStocks                                  ():
    
    return # Mientras no se haga el arqueo no se puede acceder a este menú
    
    if  nomUsuario.cget("text") == "":

        return
    global usuarioNivel
    if int(usuarioNivel) >= 3:
        return
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
      
    LimpiaLabelsRellena()
    textMenu.config(text = "MENU STOCKS")   
    menusBotones("Tornar",MenuInicial,"Introduir",menuStockIntroducir,"Consultar",menustockConsultar)         
    BM1.focus()
def menuStockIntroducir                             ():
    
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuStocks,"Introduir",regresaSinNada) 

    LR1.config(text = "PRODUCTE:")  
    LRR11.grid(row=0, column=1)  
    LRR11['values'] = (["Guiada","Vermut","Fotogràfica","Teatralitzada"])  
    LR2.config(text = "QUANTITAT:")  
    LRR22.grid(row=1, column=1)  
        
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")    
    LRR11.focus()           
def menustockConsultar                              ():
    
    LimpiaLabelsRellena()
    textMenu.config(text = "CONSULTA STOCKS")   
    menusBotones("Tornar",menuStocks,"Total",menustockConsultarTotal,"Específica",menustockConsultarEspecifica)         
def menustockConsultarTotal                             ():
    
    # Salta a un resumen total de productos en la zona 3
    return
def menustockConsultarEspecifica                        ():
    
    LimpiaLabelsRellena()
    textMenu.config(text = "CONSULTA STOCKS")   
    menusBotones("Tornar",menustockConsultar,"",regresaSinNada,"Específica",regresaSinNada)       

    LR1.config(text = "PRODUCTE:")  
    LRR11.grid(row=0, column=1)  
    LRR11['values'] = (["Guiada","Vermut","Fotogràfica","Teatralitzada"])  
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")    
    LRR11.focus()  

def menuIncidencias                             ():

    # Globaliza las variables
    global vr1,vr2,vr3,vr4,vr5,vr6,vr7,vr8,vr9,vr10,vr11,vr12,vr13,vr14
    # Borra las variables
    vr1,vr2,vr3,vr4,vr5,vr6,vr7,vr8,vr9,vr10,vr11,vr12,vr13,vr14 = "","","","","","",False,"","","","","","",False                       # Inicializamos las variables
        
    # Si aquí se pulsan las teclas CTRL + D no pasa nada
    raiz.bind("<Control-d>", lambda event: regresaSinNada())
    raiz.bind("<Control-D>", lambda event: regresaSinNada())
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    
    if  nomUsuario.cget("text") == "":

        return
    
    nomUsuario.config(text = usuarioReal)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal)
    MiraFecha(anyoFecha)
    
    global usuarioNivel
    LimpiaLabelsRellena()
       
    textMenu.config(text = "MENU INCIDÈNC./GRUPS")   
    menusBotones("Tornar",MenuInicial,"Introduir (I)",menuIncidenciasIntroducirPre,"Consultar (O)",menuIncidenciasConsultar,"Mirar/Corregir",menuIncidenciasCorregir,"Eliminar",menuIncidenciasEliminar,"",regresaSinNada,"Factures proforma",menuIncidenciasFacturaProforma,"",regresaSinNada,"Bloquejos",menuIncidenciasBloqueos)         
    BM1.focus()
    
    if int(usuarioNivel) >= 3:
            menusBotones("Tornar",MenuInicial,"",regresaSinNada,"Consultar",menuIncidenciasConsultar,"Mirar/Corregir",menuIncidenciasCorregir)        
            # Pon el foco en el botón de consultar
            BM2.focus()
    if int(usuarioNivel) >= 3:
        BM6.config(text="")
    
    # Campor LRR11 sólo permite que se introduzca algo de la lsita de selección
        LRR11.config(state = "readonly")
            
    ajusta_espacios_info(10,22,7,12,7,5,20,8,17,16,7,1)
def menuIncidenciasIntroducirPre                    ():
    global usuarioNivel
    if int(usuarioNivel) >= 3:
        return
    menuIncidenciasIntroducir()    
def menuIncidenciasIntroducir                       (modo=None):

    if modo != None:                                        # Si vinimos pulsando CTRL+I
        recuperaFechaActual()                               # Ponemos la fecha actual
    global EstamosEnIntroducir
    EstamosEnIntroducir = True
    EstamosEnIncidencias = True
    ajusta_espacios_info(10,22,7,12,7,5,20,8,17,16,7,1)
    textMenu.config(text = "MENU INCIDÈNC./GRUPS")   
    
    def menuIncidenciasIntroducirIntroduce ():
        global horas
        # Rescata los valores de los campos
        v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v16,v17,v18,v19,v20,v21,v22 = LR1.cget("text"),LRR22.get(),LRR31.get(),LRR42.get(),LRR52.get(),LRR61.get(),LRR72.get(),LRR82.get(),LRR92.get(),LRR102.get(),LRR112.get(),LRR122.get(),LRR131.get(),LRR141.get(),LRR161.get(),LRR172.get(),LRR181.get(),LRR213.get(1.0,END),LRR201.get(),LRR192.get(),LRR152.get()
              
        muralla = False
        muralla     = cotejaVacio(muralla,v20,LRR201)                               # Comprueba que el campo no esté vacío
        muralla,v17 = cotejaFechaBlock(muralla,v17,LRR172)                          # Comprueba que la fecha no esté bloqueada
        muralla,v2  = cotejaFechaBlock(muralla,v2,LRR22)                            # Comprueba que la fecha no esté bloqueada
        v2          = cotejaCondicional(v2,"Per definir",v20,"Pendent gaudir")      # Si el campo v20 es "Pendent gaudir" el campo v2 es "Per definir"
        muralla     = cotejaVacioCond1(muralla,v2,LRR22,v20,"Pendent gaudir")       # Si el campo v20 no es "Pendent gaudir" el campo v2 no puede estar vacío
        muralla     = cotejaFechaBloqueada(muralla,v2,v6,LRR22)                     # Comprueba que la fecha no esté bloqueada
        v4,v5,v22   = cotejaDatosCliente(v3,v4,v5,v22)                              # Comprueba si hay que aprovechar datos del cliente
        # Comprueba que no exista una incidencia con los mismos datos
        if muralla == False:
            muralla     = cotejaDatoCoincidente(muralla,False,True,
                                            'databases/basesDeDatosIncidencias.db',
                                            'bd_incidencias',
                                            "SELECT *,oid FROM bd_incidencias WHERE ((FECHA = '" + v2 + "') AND (HORA = '" + v6+ "'))","",
                                            "¡¡ATENCIÓ!! Ja existeix una altra incidència amb aquesta data i hora",3,v1,"red")        
     
        # Si hay algún error
        if muralla == True:                                                         # Si hay algún error
            LR23.config(fg = "red")                                                 # Pintamos de rojo el campo LR23
            return                                                                  # Salimos de la función
        
        # Salva datos
        base_datos_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')  # Crea la base de datos o conecta con ella
        cursor = base_datos_datos.cursor()                                          # Crea el cursor
        # Inserta en la base de tados
        cursor.execute("""INSERT INTO bd_Incidencias VALUES (:fecha,:hora,:pax1,:pax2,:producto,
                       :idioma,:tel_extra,:estado,:usuario,:fecha_cre,:cliente,:mail_extra,:precio1,
                       :tipo1,:precio2,:tipo2,:agendado,:fecha_rev,:pagat,:notas,:factura,:contacto)""",
                {
                    'fecha':        v2,
                    'hora':         v6,
                    'pax1':         v7,
                    'pax2':         v10,
                    'producto':     v13,
                    'idioma':       v14,
                    'tel_extra':    v4,
                    'estado':       v20,
                    'usuario':      usuarioReal,
                    'fecha_cre':    anyoGlobaltk.get() + "/" + mesGlobaltk.get() + "/" + diaGlobaltk.get(),
                    'cliente':      v3,
                    'mail_extra':   v5,
                    'precio1':      v8,
                    'tipo1':        v9,
                    'precio2':      v11,
                    'tipo2':        v12,
                    'agendado':     v16,
                    'fecha_rev':    v17,
                    'pagat' :       v18,
                    'notas':        v21,
                    'factura':      v19,
                    'contacto':     v22
                    })
        base_datos_datos.commit()                                                   # Asegura los cambios
        base_datos_datos.close()                                                    # Cerrar conexion             
        # Pinta datos en zona 3
        query_todos('databases/basesDeDatosIncidencias.db',
                    "SELECT *, oid FROM bd_incidencias ORDER BY FECHA_CREA DESC, HORA DESC",
                    8,
                    "EstamosEnIncidencias",
                    "ID","DATA","HORA","PAX","PRODUCTE","IDIOMA","ESTAT","CLIENT","PAGAT") 
        LR23.config(text = "")                                                      # Limpia posibles mensajes anteriores innecesarios

        # Pinta la lista actualizada
        base_datos_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')  # Crea la base de datos o conecta con ella  
        cursor = base_datos_datos.cursor()                                          # Crea el cursor
        cursor.execute("SELECT *, oid FROM bd_incidencias")                         # Coge el valor del ultimo oid
        try:                                                                        # Si hay datos
            datos = cursor.fetchall()
            dato = datos[-1]
            idAdecuado = dato[22]
        except:
            idAdecuado = 0
            
        idCorrecto = int(idAdecuado)+1                                              # Prepara el nuevo ID
        base_datos_datos.close()                                                    # Cerrar conexion 
        LimpiaElegibles()                                                           # Limpia los campos
        LRR1.config(text = idCorrecto)                                              # Prepara el nuevo ID    
        LRR31.config(state = "readandwrite")                                        # Liberamos la escritura de la etiqueta CLIENT
        LRR22.focus()                                                               # Coloca foco

    base_datos_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')      # Crea la base de datos o conecta con ella
    cursor = base_datos_datos.cursor()                                              # Crea el cursor
    cursor.execute("SELECT *, oid FROM bd_Incidencias")                             # Coge el valor del ultimo oid
    try:
        datos = cursor.fetchall()
        dato = datos[-1]
        idAdecuado = dato[22]
    except:
        idAdecuado = 0 
    idCorrecto = int(idAdecuado)+1                                                  # Prepara el nuevo ID
    base_datos_datos.close()                                                        # Cerrar conexion 
    LimpiaLabelsRellena()                                                           # Limpia los campos
    menusBotones("Tornar",menuIncidencias,"Introduir (I)")                          # Pinta los botones
    # Pinta los campos
    OpcionesQuestionario(["1",LR1,"ID:",LRR1,idCorrecto],
                         ["X2",LR2,"DIA/MES/ANY:",LRR22],
                         ["X1",LR3,"CLIENT:",LRR31,clientes,regresaSinNada1,"readandwrite"],
                         ["X2",LR4,"TELF. EXTRA:",LRR42],
                         ["X2",LR5,"MAIL EXTRA:",LRR52],
                         ["X1",LR6,"HORA:",LRR61,horas],
                         ["X2",LR7,"PAX:",LRR72],
                         ["X2",LR8,"PREU:",LRR82],
                         ["X2",LR9,"TIPUS:",LRR92],
                         ["X2",LR10,"PAX:",LRR102],
                         ["X2",LR11,"PREU:",LRR112],
                         ["X2",LR12,"TIPUS:",LRR122],
                         ["X1",LR13,"PRODUCTE:",LRR131,productosR],
                         ["X1",LR14,"IDIOMA:",LRR141,idiomas],
                         ["X2",LR15,"CONTACTE:",LRR152],
                         ["X1",LR16,"AGENDAT:",LRR161,["Si","No"]],
                         ["X2",LR17,"DATA REV.:",LRR172],
                         ["X1",LR18,"PAGAT:",LRR181,["Si","No"]],
                         ["X2",LR19,"FACTURA:",LRR192],
                         ["X1",LR20,"ESTAT:",LRR201,estados],
                         ["X3",LR21,"NOTES:",LRR213])
    Boton4activado2(menuIncidenciasIntroducirIntroduce)                              # Boton 4 activado
    # Pinta datos en zona 3
    query_todos('databases/basesDeDatosIncidencias.db',
                "SELECT *, oid FROM bd_incidencias ORDER BY FECHA_CREA DESC, HORA DESC",
                8,
                "EstamosEnIncidencias",
                "ID","DATA","HORA","PAX","PRODUCTE","IDIOMA","ESTAT","CLIENT","PAGAT")        
    # Si el usuario tiene un nivel de 3 o más...
    if int(usuarioNivel) >= 3:
        # Ponemos el foco en el botón de estado
        LRR213.focus()
        return  
    notasAmpliacion()                                                               # Mirmaos si hay que ampliar el blog de notas
    ActivaBotonPyFocus(LRR22,BotonPrimeroQ22)                                       # Activa el boton de la fecha
def menuIncidenciasConsultar                        (modo=None):

    if modo != None:                                        # Si vinimos pulsando CTRL+O
        recuperaFechaActual()                               # Ponemos la fecha actual
    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    textMenu.config(text = "MENU INCIDÈNC./GRUPS")   
    ajusta_espacios_info(10,22,7,12,7,5,20,8,17,16,7,1)
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidencias,"",regresaSinNada,"Consultar (O)")    

    OpcionesQuestionario(["X1",LR1,"CLIENT:",LRR11,clientes,regresaSinNada1,"readandwrite"],
                         ["X2",LR2,"esdeveniment DIA:",LRR22],
                         ["X2",LR3,"MES:",LRR32],
                         ["X2",LR4,"ANY:",LRR42],
                         ["X1",LR5,"PRODUCTE:",LRR51,productosR],
                         ["X1",LR6,"IDIOMA:",LRR61,idiomas],
                         ["X1",LR7,"AGENDAT:",LRR71,["Si","No"]],
                         ["X2",LR8,"revisió DIA:",LRR82],
                         ["X2",LR9,"MES:",LRR92],
                         ["X2",LR10,"ANY:",LRR102],
                         ["X2",LR11,"FACTURA:",LRR112],
                         ["X1",LR12,"ESTAT:",LRR121,estados],
                         ["X1",LR13,"PAGAT:",LRR131,["Si","No"]],
                         ["X2",LR14,"MAIL:",LRR142])

    # Hacemos globales las variables que vamos a usar
    global vr1,vr2,vr3,vr4,vr5,vr6,vr7,vr8,vr9,vr10,vr11,vr12,vr13,vr14
    # Si las variables vr1 a vr7 tienen datos, se copia esos valroes a las labels respectivas
    if vr14 == True:
        LRR22.insert(0,vr1)
        LRR32.insert(0,vr2)
        LRR42.insert(0,vr3)
        LRR51.set(vr4)
        LRR61.set(vr5)
        LRR71.set(vr6)
        LRR82.insert(0,vr8)
        LRR92.insert(0,vr9)
        LRR102.insert(0,vr10)
        LRR112.insert(0,vr11)
        LRR121.set(vr12)
        LRR131.set(vr13)

        vr14 = False        
    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustadaInc())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustadaInc())
            
    Boton4activado(query_todos_busca0,query_incidencias_busca)
    Boton5activado(prequery_todos,query_incidencias_busca)
    Boton6activado(query_incidencias_busca)
    ActivaBotonPyFocus(LRR11,BotonPrimeroQ11)
def menuIncidenciasCorregir                         ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    MiraFecha(anyoFecha)

    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
     
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidencias,"",regresaSinNada,"",regresaSinNada,"Mirar/Corregir")

    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])
        
    Boton4activado2(incidenciasCorrigeUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuIncidenciasEliminar                         ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = True

    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidencias,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Eliminar")

    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])
 
    Boton4activado2(incidenciasBorraUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
     
def menuIncidenciasFacturaProforma               ():
 
    global usuarioNivel
    if int(usuarioNivel) >= 3:
        return
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    
    global VieneDeIncGrups
    VieneDeIncGrups = "None"
    
    nomUsuario.config(text = usuarioReal)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal)
    MiraFecha(anyoFecha)
    
    ajusta_espacios_info(10,22,8,11,1,12,25,9,25,7,1,1)
    textMenu.config(text = "PROFORMA")   
    LimpiaLabelsRellena() 
    menusBotones("Tornar",menuIncidencias,"Introduir",menuIncidenciasFacturaProformaIntroducir,"Consultar",menuIncidenciasFacturaProformaConsultar,"Mirar/Corregir",menuIncidenciasFacturaProformaCorregir,"Eliminar",menuIncidenciasFacturaProformaEliminar)
    BM1.focus()
def menuIncidenciasFacturaProformaIntroducir        ():
    
    if nomUsuario.cget("text") == "":
        return
    textMenu.config(text = "PROFORMA INTRODUIR")   
    LimpiaLabelsRellena() 
    menusBotones("Tornar",menuIncidenciasFacturaProforma,"Produir",menuIncidenciasFacturaProformaIntroducirProducir,"Clonar",menuIncidenciasFacturaProformaIntroducirClonar,"Crear",menuIncidenciasFacturaProformaIntroducirCrear)
    BM1.focus()
def menuIncidenciasFacturaProformaIntroducirProducir    ():
    
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidenciasFacturaProformaIntroducir,"Produir")

    LR1.config(text = "ID Incidència/grup:")
    LRR12.grid(row=0, column=1)
        
    Boton4activado2(ProformaProduceUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuIncidenciasFacturaProformaIntroducirClonar      ():

    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidenciasFacturaProformaIntroducir,"Produir",regresaSinNada,"Clonar")

    LR1.config(text = "ID Proforma:")
    LRR12.grid(row=0, column=1)
        
    Boton4activado2(ProformaClonaUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuIncidenciasFacturaProformaIntroducirCrear       ():
    
    global EstamosEnIntroducir
    EstamosEnIntroducir = True
    
    global VieneDeIncGrups
    ajusta_espacios_info(10,22,8,11,1,12,25,9,25,7,1,1)
    
    def menuProformaIntroducirIntroduce ():
        # Rescata los valores de los campos
        v1 = LRR1.cget("text")
        v2 = LRR22.get()
        v3 = LRR31.get()
        v4 = LRR42.get()
        v5 = LRR52.get()
        v6 = LRR62.get()
        v7 = LRR72.get()
        v8 = LRR82.get()
        v9 = LRR92.get()
        v10 = LRR102.get()
        v11 = LRR111.get()
        v12 = LRR122.get()
        v13 = LRR131.get()
        v15 = LRR142.get()
        # Guardamos en v14 el valor de ID de incedències/grups si existe
        global v14
        v14 = VieneDeIncGrups
            
        # Coteja errores
        # Miramos si v2 está vacío
        if v2 == "":
            LR23.config(text = "Falta proforma")
            LRR22.focus()
            return
        
        # Miramos si v2 existe como NUM_PRO
        # Abrimos la tabla de proformas
        conn = sqlite3.connect('databases/basesDeDatosProforma.db')
        c = conn.cursor()
        # Bucle revisando todas las proformas
        for row in c.execute('SELECT * FROM bd_Proforma'):
            # Si el NUM_PRO coincide con v2
            if row[2] == v2:
                # Cerramos la tabla
                conn.close()
                # Mostramos el error
                LR23.config(text = "Proforma duplicat")
                # Ponemos el foco en NUM_PRO
                LRR22.focus()
                return
        
        # Si en v2 hay el símbolo "/" avisamos que no es válido
        if "/" in v2:
            LR23.config(text = "No es pot posar '/' al nom de proforma")
            LRR22.focus()
            return
        # Miramos si ha puesto un cliente
        if v3 == "":
            LR23.config(text = "Falta Client")
            LRR31.focus()
            return
        
        # Miramos si el va15 es un número
        try:
            v15 = float(v15)
        except:
            LR23.config(text = "El tant % a pagar no és un número")
            LRR142.focus()
            return
        # Miramos si el cliente existe
        # Abrimos la tabla de clientes
        conn = sqlite3.connect('databases/basesDeDatosClientes.db')
        c = conn.cursor()
        # Bucle revisando todos los clientes
        exist = False
        for row in c.execute('SELECT * FROM bd_Clientes'):
            # Si el ID coincide con v3
            if row[0] == v3:
                # Cerramos la tabla
                conn.close()
                # Ponemos la variable exist en True
                exist = True
                # Salimos del bucle
                break
        if exist == False:
            LR23.config(text = "Client inexistent")
            LRR31.focus()
            return  
          
        # Miramos que la fecha esté bien escrita
        try:
            # Si el principio de v4 es 1 dígito y "/"
            if v4[1] == "/":
                #Añadimos un 0 delante
                v4 = "0" + v4
            # Si el principio de v4 no es 2 dígitos y "/"
            if v4[0:2].isdigit() == False:
                LR23.config(text = "Dia incorrecte")
                LRR42.focus()
                return

            # Si la posición 4 es "/"
            if v4[4] == "/":
                # Añadimos un 0 entre la posición 2 y 3
                v4 = v4[0:3] + "0" + v4[3:]
            # Si v4 no contiene "/" dos digitos y "/"
            if v4[3:5].isdigit() == False:
                LR23.config(text = "Mes incorrecte")
                LRR42.focus()
                return

            # Si el largo de la cadena v4 es inferior a 10 caracteres
            if len(v4) <= 9:
                # Añadimos 20 entre las posiciones 5 y 6
                v4 = v4[0:6] + "20" + v4[6:] 
            # Si v4 no acaba en 4 dígitos
            if v4[6:10].isdigit() == False:
                LR23.config(text = "Any incorrecte")
                LRR42.focus()
                return
            # Si el largo es superior a 10 caracteres
            if len(v4) > 10:
                LR23.config(text = "DOta incorrecte")
                LRR42.focus()
                return
        except:
                LR23.config(text = "Data incorrecte")
                LRR42.focus() 
                return 
        
        # Si v5 no es un número y no está en blanco
        if v5 != "" and v5.isdigit() == False:
            LR23.config(text = "Quantitat incorrecte")
            LRR52.focus()
            return
        # Si v7 no es un número real y no está en blanco
        if v7 != "" and v7.replace(".","",1).isdigit() == False:
            LR23.config(text = "Preu incorrecte")
            LRR72.focus()
            return
        
        # Si v8 no es un número y no está en blanco
        if v8 != "" and v8.isdigit() == False:
            LR23.config(text = "Quantitat incorrecte")
            LRR82.focus()
            return
        
        # Si v10 no es un número y no está en blanco
        if v10 != "" and v10.isdigit() == False:
            LR23.config(text = "Preu incorrecte")
            LRR102.focus()
            return
        
        # Si v11 está vacío
        if v11 == "":
            LR23.config(text = "No sabem si hi ha IVA")
            LRR111.focus()
            return
        
        # Si v11 es sí y v12 está vacío
        if  v11 == "Si" and v12 == "":
            LR23.config(text = "No sabem el tan % d'IVA?")
            LRR122.focus()
            return
        
        # Si v11 es sí y v12 no es un número
        if  v11 == "Si" and v12.isdigit() == False:
            LR23.config(text = "L'IVA ha de ser un número")
            LRR122.focus()
            return
        
        # Si v11 es sí y v13 está vacío
        if  v11 == "Si" and v13 == "":
            LR23.config(text = "No sabem si l'IVA està inclòs")
            LRR131.focus()
            return
                        
        # Salva datos
        # Crea la base de datos o conecta con ella
        base_datos_datos = sqlite3.connect('databases/basesDeDatosProforma.db')
          
        # Crea el cursor
        cursor = base_datos_datos.cursor()   
    
        # Inserta en la base de tados
        cursor.execute("""INSERT INTO bd_Proforma VALUES (:fecha,:fechaPro,:numPro,:cliente,:cant1,
                       :concept1,:precio1,:cant2,:concept2,:precio2,:iva,:tipoIva,:incluidoIva,
                       :idIncidencias,:parte)""",
                {
                    'fecha':           v4,
                    'fechaPro':        anyoGlobaltk.get() + "/" + mesGlobaltk.get() + "/" + diaGlobaltk.get(),
                    'numPro':          v2,
                    'cliente':         v3,
                    'cant1':           v5,
                    'concept1':        v6,
                    'precio1':         v7,
                    'cant2':           v8,
                    'concept2':        v9,
                    'precio2':         v10,
                    'iva':             v11,
                    'tipoIva':         v12,
                    'incluidoIva':     v13,
                    'idIncidencias':   v14,
                    'parte':           v15
                    })


        # Asegura los cambios
        base_datos_datos.commit()

        # Cerrar conexion 
        base_datos_datos.close() 
                            
        # Pinta datos en zona 3
        query_todos('databases/basesDeDatosProforma.db',
                    "SELECT *, oid FROM bd_proforma ORDER BY NUM_PRO DESC",
                    8,
                    "EstamosEnProformas",
                    "ID","DATA","","PROFORMA","CLIENT","QUANTITAT","CONCEPTE","PREU","")        

        # Limpia posibles mensajes anteriores innecesarios
        LR23.config(text = "")

        # Pinta la lista actualizada
        # Crea la base de datos o conecta con ella
        base_datos_datos = sqlite3.connect('databases/basesDeDatosProforma.db')
            
        # Crea el cursor
        cursor = base_datos_datos.cursor()
        
        # Coge el valor del ultimo oid
        cursor.execute("SELECT *, oid FROM bd_proforma")
        
        try:
            datos = cursor.fetchall()
            dato = datos[-1]
            idAdecuado = dato[21]
        except:
            idAdecuado = 0
            
        idCorrecto = int(idAdecuado)+1
        
        # Cerrar conexion 
        base_datos_datos.close() 
        
        # Prepara el nuevo ID    
        LRR1.config(text = idCorrecto)

        # Limpia los campos
        LimpiaElegibles()
        
        # Liberamos la escritura de la etiqueta CLIENT
        LRR31.config(state = "readandwrite")
        
        # Abrimos db_incidencias
        db_incidencias = sqlite3.connect('databases/basesDeDatosIncidencias.db')

        # Creamos el cursor
        c = db_incidencias.cursor()
        
        c.execute("""UPDATE bd_incidencias SET
                                NOTAS           = :notas                
                                WHERE oid = :v14""",
                                {
                                    'notas' : v2,
                                    'v14': v14
                                    })

        #Asegura los cambios
        db_incidencias.commit()

        # Cierra la conexión 
        db_incidencias.close()  
            
        # Coloca foco
        LRR22.focus()
           
    # Crea la base de datos o conecta con ella
    base_datos_datos = sqlite3.connect('databases/basesDeDatosProforma.db')
        
    # Crea el cursor
    cursor = base_datos_datos.cursor()
    
    # Coge el valor del ultimo oid
    cursor.execute("SELECT *, oid FROM bd_Proforma ORDER BY NUM_PRO DESC")
    
    try:
        datos = cursor.fetchall()
        dato = datos[-1]
        idAdecuado = dato[21]
    except:
        idAdecuado = 0
        
    idCorrecto = int(idAdecuado)+1
    
    # Cerrar conexion 
    base_datos_datos.close()
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidenciasFacturaProforma,"",regresaSinNada,"",regresaSinNada,"Crear") 
    
    OpcionesQuestionario(["1",LR1,"ID:",LRR1,idCorrecto],
                         ["X2",LR2,"PROFORMA:",LRR22],
                         ["X1",LR3,"CLIENT:",LRR31,clientes,regresaSinNada1,"readandwrite"],
                         ["X2",LR4,"DATA ACTE D/M/A:",LRR42],
                         ["X2",LR5,"QUANTITAT 1:",LRR52],
                         ["X2",LR6,"CONCEPTE 1:",LRR62],
                         ["X2",LR7,"PREU 1:",LRR72],
                         ["X2",LR8,"QUANTITAT 2:",LRR82],
                         ["X2",LR9,"CONCEPTE 2:",LRR92],
                         ["X2",LR10,"PREU 2:",LRR102],
                         ["X1",LR11,"REPERCUTEIX IVA:",LRR111,["Si","No"]],
                         ["x2",LR12,"% IVA:",LRR122],
                         ["X1",LR13,"INCLÒS:",LRR131,["Si","No"]],
                         ["X2",LR14,"TANT % A PAGAR:",LRR142])

    # Si la casilla REPERCUTEIX IVA está vacía:
    if LRR111.get() == "":
        # Por defecto no se repercutirá IVA
        LRR111.current(1)

    # Si la label LRR142 está vacía:
    if LRR142.get() == "":
        # Le ponemos valor 100
        LRR142.insert(0,"100")
      
    # Si en cualquier momento se pulsan las teclas CTRL + P se fuerza la impresión de PDF
    raiz.bind("<Control-p>", lambda event: BotonImprimirForzado())
    raiz.bind("<Control-P>", lambda event: BotonImprimirForzado())     
    Boton7activado(PDFProforma)
    Boton4activado2(menuProformaIntroducirIntroduce)
    query_todos('databases/basesDeDatosProforma.db',
                "SELECT *, oid FROM bd_proforma ORDER BY NUM_PRO DESC",
                8,
                "EstamosEnProformas",
                "ID","DATA","","PROFORMA","CLIENT","QUANTITAT","CONCEPTE","PREU","")        
    
    ActivaBotonPyFocus(LRR22,BotonPrimeroQ22)
def menuIncidenciasFacturaProformaConsultar         ():
    
    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    LimpiaLabelsRellena()    
    menusBotones("Tornar",menuIncidenciasFacturaProforma,"",regresaSinNada,"Consultar")

    OpcionesQuestionario(["X2",LR1,"PROFORMA:",LRR12],
                         ["X1",LR2,"CLIENT:",LRR21,clientes],
                         ["X2",LR3,"Acte: DIA:",LRR32],
                         ["X2",LR4,"MES:",LRR42],
                         ["X2",LR5,"ANY:",LRR52],
                         ["X2",LR6,"QUANTITAT PAX:",LRR62],
                         ["X2",LR7,"PREU PAX:",LRR72])

    # Si aquí se pulsan las teclas CTRL + D se pone la fecha actual
    raiz.bind("<Control-d>", lambda event: FechaActualIncrustada())
    raiz.bind("<Control-D>", lambda event: FechaActualIncrustada())
        
    Boton4activado(query_todos_busca0,query_proforma_busca)
    Boton5activado(prequery_todos,query_proforma_busca)
    Boton6activado(query_proforma_busca)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuIncidenciasFacturaProformaCorregir          ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal) 
     
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidenciasFacturaProforma,"",regresaSinNada,"",regresaSinNada,"Mirar/Corregir")

    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])
       
    Boton4activado2(ProformaCorrigeUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuIncidenciasFacturaProformaEliminar          ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = True

    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidenciasFacturaProforma,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Eliminar")

    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])
   
    Boton4activado2(ProformaBorraUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)

def menuIncidenciasBloqueos                      ():
 
    global usuarioNivel
    if int(usuarioNivel) >= 3:
        return
    
    global VieneDeIncGrups
    VieneDeIncGrups = "None"
    
    nomUsuario.config(text = usuarioReal)
    diaGlobaltk.set(diaGlobal)
    mesGlobaltk.set(mesGlobal)
    anyoGlobaltk.set(anyoGlobal)
    MiraFecha(anyoFecha)
    
    ajusta_espacios_info(10,22,10,10,10,10,10,10,10,10,10,10)
    textMenu.config(text = "BLOQUEJOS")   
    LimpiaLabelsRellena() 
    menusBotones("Tornar",menuIncidencias,"Bloquejar",menuIncidenciasBloqueosBloquear,"Desbloquejar",menuIncidenciasBloqueosDesbloquear)
    BM1.focus()
def menuIncidenciasBloqueosBloquear                 ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = True
    global usuarioNivel
    if int(usuarioNivel) >= 3:
        return
    ajusta_espacios_info(10,22,10,10,10,10,10,10,10,10,10,10)

    
    def menuIncidenciasBloqueosBloquea ():
        # Rescata los valores de los campos
        v2 = LRR12.get()
        v3 = LRR21.get()
        v4 = LRR31.get()
        
        # Coteja errores
        try:
            # Si el principio de v2 es 1 dígito y "/"
            if v2[1] == "/":
                #Añadimos un 0 delante
                v2 = "0" + v2
            # Si el principio de v2 no es 2 dígitos y "/"
            if v2[0:2].isdigit() == False:
                LR23.config(text = "Dia incorrecte")
                LRR22.focus()
                return

            # Si la posición 4 es "/"
            if v2[4] == "/":
                # Añadimos un 0 entre la posición 2 y 3
                v2 = v2[0:3] + "0" + v2[3:]
            # Si v2 no contiene "/" dos digitos y "/"
            if v2[3:5].isdigit() == False:
                LR23.config(text = "Mes incorrecte")
                LRR22.focus()
                return

            # Si el largo de la cadena v2 es inferior a 10 caracteres
            if len(v2) <= 9:
                # Añadimos 20 entre las posiciones 5 y 6
                v2 = v2[0:6] + "20" + v2[6:] 
            # Si v2 no acaba en 4 dígitos
            if v2[6:10].isdigit() == False:
                LR23.config(text = "Any incorrecte")
                LRR22.focus()
                return
            # Si el largo es superior a 10 caracteres
            if len(v2) > 10:
                LR23.config(text = "Data incorrecte")
                LRR22.focus()
                return
            # Si v2 no contiene 2 dígitos, "/", 2 dígitos, "/", 4 dígitos
            if v2[2] != "/" or v2[5] != "/":
                LR23.config(text = "Data incorrecte")
                LRR22.focus()
                return
        except:
                LR23.config(text = "Data incorrecte")
                LRR22.focus() 
                return 
         
        # Miramos si existe una incidencia con la misma fecha y hora
        # Abrimos la base de datos de incidencias
        conn = sqlite3.connect('databases/basesDeDatosIncidencias.db')    
        # Creamos el cursor
        miCursor = conn.cursor()
        # Crea una lista con los datos FECHA
        miCursor.execute("SELECT *,oid FROM bd_incidencias WHERE ((FECHA = '" + v2 + "') AND (HORA >='"+ v3 + "') AND (HORA <'" + v4 + "'))")
        casos = miCursor.fetchall()
        cant_casos = len(casos)
        # Si hay más de un caso con la misma fecha y hora
        if cant_casos > 0:
            ventanaAviso("Ja existeixen incidències a la franja.", "red",2)                                                          
        # Salva datos
        # Crea la base de datos o conecta con ella
        base_datos_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')
        
        
        # Crea el cursor
        cursor = base_datos_datos.cursor()   
    
        # Inserta en la base de tados
        cursor.execute("""INSERT INTO bd_Bloqueos VALUES (:fecha, :desde, :hasta)""",
                {
                    'fecha':        v2,
                    'desde':        v3,
                    'hasta':        v4
                    })


        # Asegura los cambios
        base_datos_datos.commit()

        # Cerrar conexion 
        base_datos_datos.close() 
                            
        # Pinta datos en zona 3
        query_todos('databases/basesDeDatosIncidencias.db',
                    "SELECT *, oid FROM bd_bloqueos ORDER BY FECHA",
                    8,
                    "EstamosEnBloqueos",
                    "ID","DATA","DESDE","FINS","","","","","")

        # Limpia posibles mensajes anteriores innecesarios
        LR23.config(text = "")
        
        # Limpia los campos
        LimpiaElegibles()
                
        # Coloca foco
        LRR12.focus()
           
    # Crea la base de datos o conecta con ella
    base_datos_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')
        
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidenciasBloqueos ,"Bloquejar") 
            
    OpcionesQuestionario(["X2",LR1,"DIA/MES/ANY:",LRR12],
                         ["X1",LR2,"HORA INICI:",LRR21,horas],
                         ["X1",LR3,"HORA FINAL:",LRR31,horas])
          
    Boton4activado2(menuIncidenciasBloqueosBloquea)
    query_todos('databases/basesDeDatosIncidencias.db',
                "SELECT *, oid FROM bd_bloqueos ORDER BY FECHA",
                8,"EstamosEnBloqueos",
                "ID","DATA","DESDE","FINS","","","","","")
              
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuIncidenciasBloqueosDesbloquear              ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = True
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuIncidenciasBloqueos,"",regresaSinNada,"Desbloqueja")

    OpcionesQuestionario(["X2",LR1,"DIA/MES/ANY:",LRR12])       
    Boton4activado2(bloqueoBorraUno)
    query_todos('databases/basesDeDatosIncidencias.db',
                "SELECT *, oid FROM bd_bloqueos ORDER BY FECHA",
                8,
                "EstamosEnBloqueos",
                "ID","DATA","DESDE","FINS","","","","","")


    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)

def menuCalendarios                             ():
    
    return # Desactivado por el momento
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    
    if  nomUsuario.cget("text") == "":

        return
    global usuarioNivel
    LimpiaLabelsRellena()
    textMenu.config(text = "MENU CALENDARI")   
    menusBotones("Tornar",MenuInicial,"Crear",menuCalendarioCrear,"Mostrar",menuCalendarioMostrar)
    
    if int(usuarioNivel) >= 3:
        BM1.config(text = "")
        BM3.config(text = "")               
    BM1.focus()
def menuCalendarioCrear                             ():

    global usuarioNivel
    if int(usuarioNivel) >= 3:
        return
    
    LimpiaLabelsRellena()

    textMenu.config(text = "CREAR CALEND.")   
    menusBotones("Tornar",menuCalendarios,"Usuaris",MenuCalendarioCrearUsuarios,"Visites",MenuCalendarioCrearVisitas)
def MenuCalendarioCrearUsuarios                         ():
    
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuCalendarioCrear,"Usuaris")
    
    LR1.config(text = "MES:")
    LRR12.grid(row=0, column=1)
    LR2.config(text = "ANY:")
    LRR22.grid(row=1, column=1)
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")     
    LRR12.focus()       
def MenuCalendarioCrearVisitas                          ():
    
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuCalendarioCrear,"",regresaSinNada,"Visites")
    
    LR1.config(text = "MES:")
    LRR12.grid(row=0, column=1)
    LR2.config(text = "ANY:")
    LRR22.grid(row=1, column=1)
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")     
    LRR12.focus()   
def menuCalendarioMostrar                           ():
 
    LimpiaLabelsRellena()

    textMenu.config(text = "MOSTRAR CALEND.")        
    menusBotones("Tornar",menuCalendarios,"Usuaris",menuCalendarioMostrarUsuarios,"Visites",menuCalendarioMostrarVisitas,"Hores",menuCalendarioMostrarHoras)

    global usuarioNivel
    if int(usuarioNivel) >= 3:
        BM3.config(text = "")      
def menuCalendarioMostrarUsuarios                       ():
    
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuCalendarioMostrar,"Usuaris")
    
    LR1.config(text = "MES:")
    LRR12.grid(row=0, column=1)
    LR2.config(text = "ANY:")
    LRR22.grid(row=1, column=1)
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")     
    LRR12.focus()   
def menuCalendarioMostrarVisitas                        ():
    
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuCalendarioMostrar,"",regresaSinNada,"Visites")
    
    LR1.config(text = "MES:")
    LRR12.grid(row=0, column=1)
    LR2.config(text = "ANY:")
    LRR22.grid(row=1, column=1)
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")     
    LRR12.focus()   
def menuCalendarioMostrarHoras                          ():

    global usuarioNivel
    if int(usuarioNivel) >= 3:
        return
        
    global usoUsuarios
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuCalendarioMostrar,"",regresaSinNada,"",regresaSinNada,"Hores")
    
    LR1.config(text = "USUARI:")
    LRR11.grid(row=0, column=1)
    LRR11['values'] = (usoUsuarios)  
    LR2.config(text = "MES:")
    LRR22.grid(row=1, column=1)
    LR3.config(text = "ANY:")
    LRR32.grid(row=2, column=1)
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
    cambiaPasaEncima(BB4,"green","#27779d")     
    LRR12.focus()   

def menuDatos                                   ():
    if  nomUsuario.cget("text") == "":

        return
    global usuarioNivel
    if int(usuarioNivel) >= 3:
        return  
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    LimpiaLabelsRellena()
    borra_datos()   
    textMenu.config(text = "MENU DADES")   
    menusBotones("Tornar",MenuInicial,"Producte",MenuDatosProducto,"Clients",MenuDatosCliente,"Usuaris",menuDatosUsuario,"Empresa",menuDatosEmpresa)             
    BM1.focus()
def MenuDatosProducto                               ():

    ajusta_espacios_info(10,22,7,52,13,13,10,1,1,1,1,1)
    global puntero
    puntero = 0
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    

    textMenu.config(text = "MENU PRODUCTE")   
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuDatos,"Introduir",MenuDatosProductoIntroducir,"Consultar",MenuDatosProductoConsultar,"Mirar/Corregir",MenuDatosProductoCorregir,"Eliminar",menuDatosProductoEliminar)            
    BM1.focus()
def MenuDatosProductoIntroducir                         ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = True
    
    def MenuDatosProductoIntroducirIntroduce():
       
        # Rescata valores
        v1 = LRR22.get()
        v2 = LRR32.get()
        v3 = LRR42.get()
        v4 = LRR51.get()
                
        # Coteja fallos
        if v1 == "" or v2 == "" or v3 == "" or v4 == "":
            
            LR23.config(text = "Registre incomplert")
            return
        
        try:
            
            circunstancial = float(v2)
            
        except:
            
            LR23.config(text = "Valor no numéric")
            LRR32.focus()
            return
            
        try:
            
            circunstancial = float(v3)
            
        except:
            
            LR23.config(text = "Valor no numéric")
            LRR42.focus()
            return
                    
        # Salva datos       
        # Crea la base de datos o conecta con ella
        base_datos_datos = sqlite3.connect('databases/basesDeDatosDatos.db')
        
        # Crea el cursor
        cursor = base_datos_datos.cursor()   
                            
        # Inserta en la base de tados
        cursor.execute("""INSERT INTO bd_productos VALUES (:nombre, :precio_habitual, 
                :precio_actual, :registrable)""",
                {
                    'nombre':           LRR22.get(),
                    'precio_habitual':  LRR32.get(),
                    'precio_actual':    LRR42.get(),
                    'registrable':      LRR51.get()
                    })


        # Asegura los cambios
        base_datos_datos.commit()

        # Cerrar conexion 
        base_datos_datos.close() 
        
        # Pinta datos en zona 3
        query_todos('databases/basesDeDatosDatos.db',
                    "SELECT *, oid FROM bd_productos ORDER BY oid DESC",
                    4,
                    "EstamosEnProductos",
                    "ID","NOM","PREU REAL","PREU ACTUAL","TIPUS")


        # Limpia posibles mensajes anteriores innecesarios
        LR23.config(text = "")
        LimpiaElegibles()

        # Pinta la lista actualizada
        # Crea la base de datos o conecta con ella
        base_datos_datos = sqlite3.connect('databases/basesDeDatosDatos.db')
            
        # Crea el cursor
        cursor = base_datos_datos.cursor()
        
        # Coge el valor del ultimo oid
        cursor.execute("SELECT *, oid FROM bd_productos")
        
        try:
            datos = cursor.fetchall()
            dato = datos[-1]
            idAdecuado = dato[4]
        except:
            idAdecuado = 0
            
        idCorrecto = int(idAdecuado)+1
        
        # Cerrar conexion 
        base_datos_datos.close() 
            
        LRR1.config(text = idCorrecto)
        
        # Actualiza las listas
        abreLasListas()            
        
        # Coloca foco
        LRR22.focus()

    # Crea la base de datos o conecta con ella
    base_datos_datos = sqlite3.connect('databases/basesDeDatosDatos.db')
        
    # Crea el cursor
    cursor = base_datos_datos.cursor()
    
    # Coge el valor del ultimo oid
    cursor.execute("SELECT *, oid FROM bd_productos")
    
    try:
        datos = cursor.fetchall()
        dato = datos[-1]
        idAdecuado = dato[4]
    except:
        idAdecuado = 0
        
    idCorrecto = int(idAdecuado)+1
    
    # Cerrar conexion 
    base_datos_datos.close() 
                    
    LimpiaLabelsRellena()
    menusBotones("Tornar",MenuDatosProducto,"Introduir")

    OpcionesQuestionario(["1",LR1,"ID:",LRR1,idCorrecto],
                         ["X2",LR2,"PRODUCTE:",LRR22],
                         ["X2",LR3,"PREU REAL:",LRR32],
                         ["X2",LR4,"PREU ACTUAL:",LRR42],
                         ["X1",LR5,"REGISTRE/STOCK:",LRR51,["Registre","Stock"]])
    
    Boton4activado2(MenuDatosProductoIntroducirIntroduce)
    query_todos('databases/basesDeDatosDatos.db',
                "SELECT *, oid FROM bd_productos ORDER BY oid DESC",
                4,
                "EstamosEnProductos",
                "ID","NOM","PREU REAL","PREU ACTUAL","TIPUS")
    ActivaBotonPyFocus(LRR22,BotonPrimeroQ22)
def MenuDatosProductoConsultar                          ():
 
    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    LimpiaLabelsRellena()
    menusBotones("Tornar",MenuDatosProducto,"",regresaSinNada,"Consultar")

    OpcionesQuestionario(["X1",LR1,"PRODUCTE:",LRR11,productos],
                         ["X2",LR2,"PREU REAL:",LRR22],
                         ["X2",LR3,"PREU ACTUAL:",LRR32],
                         ["X1",LR4,"REGISTRE/STOCK:",LRR41,["Registre","Stock"]])
    
    Boton4activado(query_todos_busca0,query_productos_busca)
    Boton5activado(prequery_todos,query_productos_busca)
    Boton6activado(query_productos_busca)
 
    ActivaBotonPyFocus(LRR11,BotonPrimeroQ11)
def MenuDatosProductoCorregir                           ():
    
    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    LimpiaLabelsRellena()
    menusBotones("Tornar",MenuDatosProducto,"",regresaSinNada,"",regresaSinNada,"Mirar/Corregir")
    
    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])     
    
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10,  command = productoCorrigeUno)
    cambiaPasaEncima(BB4,"green","#27779d")     
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuDatosProductoEliminar                           ():
    
    global EstamosEnIntroducir
    EstamosEnIntroducir = True

    LimpiaLabelsRellena()
    menusBotones("Tornar",MenuDatosProducto,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Eliminar")
    
    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])     
   
    Boton4activado2(productoBorraUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def MenuDatosCliente                                ():
    
    ajusta_espacios_info(10,22,5,30,1,1,17,13,19,12,1,1)
    global puntero
    puntero = 0
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    
    textMenu.config(text = "MENU CLIENT")   
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuDatos,"Introduir",MenuDatosClienteIntroducir,"Consultar",MenuDatosClienteConsultar,"Mirar/Corregir",MenuDatosClienteCorregir,"Eliminar",menuDatosClienteEliminar)            
    BM1.focus()
def MenuDatosClienteIntroducir                          ():

    global EstamosEnIntroducir
    EstamosEnIntroducir = True

    def MenuDatosClienteIntroducirIntroduce():
       
        # Rescata valores
        v1 = LRR22.get()
        v4 = LRR62.get()
                
        # Coteja fallos
        if v1 == "":
            
            LR23.config(text = "Nom del client obligatori")
            LRR22.focus()
            return
        
        # Si se incluye ' o " en el nombre, No se puede avanzar
        if "'" in v1 or '"' in v1:
            
            LR23.config(text = "No es pot utilitzar ' o \" al nom")  
            LRR22.focus()
            return         
        
        if v4 != "":
            try:
                
                circunstancial = int(v4)
                
            except:
                
                LR23.config(text = "Telèfon erroni")
                LRR52.focus()
                return
                    
        # Salva datos       
        # Crea la base de datos o conecta con ella
        base_datos_datos = sqlite3.connect('databases/basesDeDatosClientes.db')
        
        # Crea el cursor
        cursor = base_datos_datos.cursor()   
                            
        # Inserta en la base de tados
        cursor.execute("""INSERT INTO bd_clientes VALUES (:nombre, :direccion1, 
                :direccion2, :direccion3, :telefono, :mail, :nifcif, :contacto, :telefonocont, :mailcont)""",
                {
                    'nombre':           LRR22.get(),
                    'direccion1':       LRR32.get(),
                    'direccion2':       LRR42.get(),
                    'direccion3':       LRR52.get(),
                    'telefono':         LRR62.get(),
                    'mail':             LRR72.get(),
                    'nifcif':           LRR82.get(),
                    'contacto':         LRR92.get(),
                    'telefonocont':     LRR102.get(),
                    'mailcont':         LRR112.get()
                    })


        # Asegura los cambios
        base_datos_datos.commit()

        # Cerrar conexion 
        base_datos_datos.close() 
        
        # Pinta datos en zona 3
        query_todos('databases/basesDeDatosClientes.db',
                    "SELECT *, oid FROM bd_clientes ORDER BY oid DESC",
                    7,
                    "EstamosEnClientes",
                    "ID","NOM","","","CIUTAT/PAIS","TELÈFON","MAIL","NIF/CIF")

        # Limpia posibles mensajes anteriores innecesarios
        LR23.config(text = "")
        LimpiaElegibles()

        # Pinta el nuevo id
        # Crea la base de datos o conecta con ella
        base_datos_datos = sqlite3.connect('databases/basesDeDatosClientes.db')
            
        # Crea el cursor
        cursor = base_datos_datos.cursor()
        
        # Coge el valor del ultimo oid
        cursor.execute("SELECT *, oid FROM bd_clientes")
        
        try:
            datos = cursor.fetchall()
            dato = datos[-1]
            idAdecuado = dato[10]
        except:
            idAdecuado = 0
            
        idCorrecto = int(idAdecuado)+1
        
        # Cerrar conexion 
        base_datos_datos.close() 
            
        LRR1.config(text = idCorrecto)            
        
        # Actualiza las listas
        abreLasListas()  
        
        # Coloca foco
        LRR22.focus()

    # Crea la base de datos o conecta con ella
    base_datos_datos = sqlite3.connect('databases/basesDeDatosClientes.db')
        
    # Crea el cursor
    cursor = base_datos_datos.cursor()
    
    # Coge el valor del ultimo oid
    cursor.execute("SELECT *, oid FROM bd_clientes")
    
    try:
        datos = cursor.fetchall()
        dato = datos[-1]
        idAdecuado = dato[10]
    except:
        idAdecuado = 0
        
    idCorrecto = int(idAdecuado)+1
    
    # Cerrar conexion 
    base_datos_datos.close() 
             
    LimpiaLabelsRellena()
    menusBotones("Tornar",MenuDatosCliente,"Introduir")

    OpcionesQuestionario(["1",LR1,"ID:",LRR1,idCorrecto],
                         ["X2",LR2,"NOM:",LRR22],
                         ["X2",LR3,"ADREÇA:",LRR32],
                         ["X2",LR4,"C.P.:",LRR42],
                         ["X2",LR5,"CIUTAT/PAIS:",LRR52],
                         ["X2",LR6,"TELÈFON:",LRR62],
                         ["X2",LR7,"E-MAIL:",LRR72],
                         ["X2",LR8,"NIF/CIF:",LRR82],
                         ["X2",LR9,"CONTACTE:",LRR92],
                         ["X2",LR10,"TELÈFON CONTACTE:",LRR102],
                         ["X2",LR11,"MAIL CONTACTE:",LRR112])
        
    BB4.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10, command =MenuDatosClienteIntroducirIntroduce)
    cambiaPasaEncima(BB4,"green","#27779d") 
    
    query_todos('databases/basesDeDatosClientes.db',
                "SELECT *, oid FROM bd_clientes ORDER BY oid DESC",
                7,
                "EstamosEnClientes",
                "ID","NOM","","","CIUTAT/PAIS","TELÈFON","MAIL","NIF/CIF")
       
    ActivaBotonPyFocus(LRR22,BotonPrimeroQ22)
def MenuDatosClienteConsultar                           ():
 
    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    LimpiaLabelsRellena()
    menusBotones("Tornar",MenuDatosCliente,"",regresaSinNada,"Consultar")
    
    OpcionesQuestionario(["X1",LR1,"NOM:",LRR11,clientes],
                         ["X2",LR2,"TELÈFON:",LRR22],
                         ["X2",LR3,"E-MAIL:",LRR32],
                         ["X2",LR4,"NIF/CIF:",LRR42])

    Boton4activado(query_todos_busca0,query_clientes_busca)
    Boton5activado(prequery_todos,query_clientes_busca)
    Boton6activado(query_clientes_busca)
    ActivaBotonPyFocus(LRR11,BotonPrimeroQ11)
def MenuDatosClienteCorregir                            ():
    
    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    LimpiaLabelsRellena()
    menusBotones("Tornar",MenuDatosCliente,"",regresaSinNada,"",regresaSinNada,"Mirar/Corregir")
    
    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])     

    Boton4activado2(clienteCorrigeUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuDatosClienteEliminar                            ():
    
    global EstamosEnIntroducir
    EstamosEnIntroducir = True

    LimpiaLabelsRellena()
    menusBotones("Tornar",MenuDatosCliente,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Eliminar")
    
    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])     
  
    Boton4activado2(clienteBorraUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuDatosUsuario                                ():
    
    ajusta_espacios_info(10,22,7,34,6,8,9,9,9,9,7,1)
    global puntero
    puntero = 0
    global usuarioNivel
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    

    if int(usuarioNivel) >= 3:
        return
    
    textMenu.config(text = "MENU USUARIS") 
    LimpiaLabelsRellena()
    LRR22.config(show="")
    LRR32.config(show="")
    menusBotones("Tornar",menuDatos,"Introduir",menuDatosUsuarioIntroducir,"Consultar",menuDatosUsuarioConsultar,"Mirar/Corregir",menuDatosUsuarioCorregir,"Eliminar",menuDatosUsuarioEliminar)            
    BM1.focus()
def menuDatosUsuarioIntroducir                          ():
    
    global EstamosEnIntroducir
    EstamosEnIntroducir = True

    def MenuDatosUsuarioIntroducirIntroduce():
        
        # Rescata valores
        v1,v2,v3,v4,v5,v6,v7,v8,v9 = LRR12.get(),LRR22.get(),LRR32.get(),LRR41.get(),LRR51.get(),LRR61.get(),LRR71.get(),LRR81.get(),LRR92.get()
        # Coteja fallos
        muralla = False                                 # Si muralla = True, no se salva
        muralla = cotejaIgualdad(muralla,v2,v3,LRR22)   # Coteja que no sean iguales
        muralla = cotejaEsNumero(muralla,v9,LRR92)      # Coteja que sea numero
        muralla = cotejaVacio(muralla,v1,LRR12)         # Coteja que no esten vacios
        muralla = cotejaVacio(muralla,v2,LRR22)         # Coteja que no esten vacios
        muralla = cotejaVacio(muralla,v3,LRR32)         # Coteja que no esten vacios
        muralla = cotejaVacio(muralla,v4,LRR41)         # Coteja que no esten vacios
        muralla = cotejaVacio(muralla,v5,LRR51)         # Coteja que no esten vacios
        muralla = cotejaVacio(muralla,v6,LRR61)         # Coteja que no esten vacios
        muralla = cotejaVacio(muralla,v7,LRR71)         # Coteja que no esten vacios
        muralla = cotejaVacio(muralla,v8,LRR81)         # Coteja que no esten vacios
        muralla = cotejaVacio(muralla,v9,LRR92)         # Coteja que no esten vacio
        if muralla == True:                             # Si muralla = True, no se salva
            LR23.config(fg = "red")                     # Pintamos de rojo el campo LR23
            return                                      # Salimos de la funcion
 

        # Salva datos       
        # Crea la base de datos o conecta con ella
        base_datos_datos = sqlite3.connect('databases/basesDeDatosDatos.db')
        
        # Crea el cursor
        cursor = base_datos_datos.cursor()   
                            
        # Inserta en la base de tados
        cursor.execute("""INSERT INTO bd_usuarios VALUES (:nombre, :clave, :nivel, 
                :ingles, :castellano, :catalan, :frances, :horas)""",
                {
                    'nombre':           LRR12.get(),
                    'clave':            LRR22.get(),
                    'nivel':            LRR41.get(),
                    'ingles':           LRR51.get(),
                    'castellano':       LRR61.get(),
                    'catalan':          LRR71.get(),
                    'frances':          LRR81.get(),
                    'horas':            LRR92.get()
                    })


        # Asegura los cambios
        base_datos_datos.commit()

        # Cerrar conexion 
        base_datos_datos.close() 
        
        # Pinta datos en zona 3
        query_todos('databases/basesDeDatosDatos.db',
                    "SELECT *, oid FROM bd_usuarios ORDER BY oid DESC",
                    7,
                    "EstamosEnUsuarios",
                    "ID","NOM","CLAU","NIVELL","ANGLÈS","CASTELLÀ"," CATALÀ","FRANCÈS","HORES")
      

        # Limpia posibles mensajes anteriores innecesarios
        LR23.config(text = "")
        LimpiaElegibles()

        # Coloca foco
        LRR12.focus()
        
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuDatosUsuario,"Introduir")
    
    OpcionesQuestionario(["X2",LR1,"NOM:",LRR12],
                         ["X2",LR2,"CLAU:",LRR22],
                         ["X2",LR3,"REPETEIX CLAU:",LRR32],
                         ["X1",LR4,"NIVELL D'ACCÉS:",LRR41,["1","2","3","4","5"]],
                         ["X1",LR5,"ANGLÈS:",LRR51,["Si","No"]],
                         ["X1",LR6,"CASTELLÀ:",LRR61,["Si","No"]],
                         ["X1",LR7,"CATALÀ:",LRR71,["Si","No"]],
                         ["X1",LR8,"FRANCÈS:",LRR81,["Si","No"]],
                         ["X2",LR9,"HORES LABORALS:",LRR92])
        
    Boton4activado2(MenuDatosUsuarioIntroducirIntroduce)
    query_todos('databases/basesDeDatosDatos.db',
                "SELECT *, oid FROM bd_usuarios ORDER BY oid DESC",
                8,
                "EstamosEnUsuarios",
                "ID","NOM","CLAU","NIVELL","ANGLÈS","CASTELLÀ","CATALÀ","FRANCÈS","HORES")
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuDatosUsuarioConsultar                           ():
      
    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    global usuariosO
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuDatosUsuario,"",regresaSinNada,"Consultar")

    OpcionesQuestionario(["X2",LR1,"NOM:",LRR12],
                         ["X1",LR2,"NIVELL D'ACCÉS:",LRR21,["1","2","3","4","5"]],
                         ["X1",LR3,"ANGLÈS:",LRR31,["Si","No"]],
                         ["X1",LR4,"CASTELLÀ:",LRR41,["Si","No"]],
                         ["X1",LR5,"CATALÀ:",LRR51,["Si","No"]],
                         ["X1",LR6,"FRANCÈS:",LRR61,["Si","No"]])    
        
    Boton4activado(query_todos_busca0,query_usuarios_busca)
    Boton5activado(prequery_todos,query_usuarios_busca)
    Boton6activado(query_usuarios_busca)
    ActivaBotonPyFocus(LRR11,BotonPrimeroQ11)
def menuDatosUsuarioCorregir                            ():
    
    global EstamosEnIntroducir
    EstamosEnIntroducir = False

    LimpiaLabelsRellena()
    menusBotones("Tornar",menuDatosUsuario,"",regresaSinNada,"",regresaSinNada,"Mirar/Corregir")
    
    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])     
   
    Boton4activado2(usuariosCorrigeUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuDatosUsuarioEliminar                            ():
    
    global EstamosEnIntroducir
    EstamosEnIntroducir = True

    LimpiaLabelsRellena()
    menusBotones("Tornar",menuDatosUsuario,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Eliminar")

    OpcionesQuestionario(["X2",LR1,"ID:",LRR12])     
       
    Boton4activado2(usuariosBorraUno)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
def menuDatosEmpresa                                ():

    def MenuDatosEmpresaSalva():
        # Guarda los datos de la empresa en el archivo "files/empresa.DAT"
        # Un campo por cada línea
        empresa = [LRR12.get(),LRR22.get(),LRR32.get(),LRR42.get()]         


        with open("files/EMPRESA.DAT", "w") as f:
            for i in empresa:
                f.write(i + "\n")
        # Vuelve al menú de datos
        menuDatos()
            
    LimpiaLabelsRellena()
    menusBotones("Tornar",menuDatos,"",regresaSinNada,"",regresaSinNada,"",regresaSinNada,"Empresa")

    LR1.config(text = "NOM:")
    LRR12.grid(row=0, column=1) 
    LR2.config(text = "ADREÇA 1:")  
    LRR22.grid(row=1, column=1)
    LR3.config(text = "ADREÇA 2:")  
    LRR32.grid(row=2, column=1)
    LR4.config(text = "NIF:")  
    LRR42.grid(row=3, column=1)

    # Abre el archivo "files/empresa.DAT" o lo crea si no existe
    # y lo lee para rellenar los campos
    try:
        with open("files/EMPRESA.DAT", "r") as f:
            
            # Creamos la lista empresa con los datos del archivo EMPRESA.DAT cada "\n" separa los diferentes campos
            empresa = f.read().split("\n")
            
            LRR12.insert(0,empresa[0])
            LRR22.insert(0,empresa[1])
            LRR32.insert(0,empresa[2])
            LRR42.insert(0,empresa[3])
    except:
        pass        
    Boton4activado2(MenuDatosEmpresaSalva)
    ActivaBotonPyFocus(LRR12,BotonPrimeroQ12)
    
def menuSeguridad                               ():
    if  nomUsuario.cget("text") == "":

        return 
    global usuarioNivel
    if int(usuarioNivel) >= 2:
        return
    BotonPrimeroQNada()                
    raiz.bind("<Control-Q>", lambda event: regresaSinNada())    
    LimpiaLabelsRellena()
    textMenu.config(text = "MENU SEGURETAT")   
    menusBotones("Tornar",MenuInicial,"Còpia de seguretat",menuSeguridadCopiaDeSeguridad,"Carregar",menuSeguridadCargar,"Fussionar",menuSeguridadFusionar,"Esborrar",menuSeguridadBorrar,"Netejar I/G",menuSeguridadLimpiarIncidenciasGrupos)
    BM1.focus()
def menuSeguridadCopiaDeSeguridad                   ():
        CopiaSeguridadGlobal()
        MenuInicial()
def menuSeguridadCargar                             ():
        pass
def menuSeguridadFusionar                           ():
        pass
def menuSeguridadFusionarTodos                          ():
        pass
def menuSeguridadFusionarRegistro                       ():
        pass
def menuSeguridadFusionarVentas                         ():
    pass                  
def menuSeguridadBorrar                             ():
    pass
def menuSeguridadBorrarTodos                            ():
    pass
def menuSeguridadBorrarRegistro                         ():
    pass
def menuSeguridadBorrarVentas                           ():
    pass                  
def menuSeguridadLimpiarIncidenciasGrupos           ():
        pass

def cambioUsuario1          ():
    
    MenuInicial()
    cambioUsuario()   
#  ------------------------------- Frames ----------------------------------

def frames(nombreFrame,fila,columna,expansioncolumnas,largo,alto,color):    # Función para crear frames
    
    nombreFrame.grid(row=fila, column=columna, columnspan=expansioncolumnas)
    nombreFrame.config(width=largo, height=alto)
    nombreFrame.config(bg=color)
    nombreFrame.config(bd=5)
    nombreFrame.config(relief="groove")

frameUsuario = Frame(raiz)                      # Frame de usuario
frames(frameUsuario,0,0,3,300,50,"#b7b493")
frameUsuario.grid(padx=10, pady=10)

frameFecha = Frame(raiz)                        # Frame de fecha
frames(frameFecha,0,3,4,400,50,"#b7b493")
frameFecha.grid(padx=10, pady=10)

frameBotones = Frame(raiz)                      # Frame de botones
frames(frameBotones,0,7,4,400,50,"#b7b493")
frameBotones.grid(padx=10, pady=10)

frameMenu = Frame(raiz)                         # Frame de menú  
frames(frameMenu,1,0,2,200,500,"#b7b493")
frameMenu.grid(padx=10, pady=10)

frameRellena = Frame(raiz)                      # Frame de casillas a rellenar
frames(frameRellena,1,2,3,300,500,"#b7b493")
frameRellena.grid(padx=10, pady=10)

frameLista = Frame(raiz)                        # Frame de listas
frames(frameLista,1,5,6,600,500,"#b7b493")
frameLista.grid(padx=10, pady=10)
frameLista._last_clicked = None                 # Para definir el atributo _last_clicked

# ------------------------------- Crea Listas -----------------------------------

abreLasListas()                                 # Abre las listas

# ------------------------------- Crea Usuario ----------------------------------

ConfiguraColumnas(frameUsuario,2,1,1,1)
frameUsuario.rowconfigure(0,weight = 1)
textUsuario = creaLabel("textUsuario",frameUsuario,"Usuari:",0,0,1,1,5,"#b7b493","#FFFFFF",E,12,"bold")

nomUsuario = Label(frameUsuario,text=usuarioReal)
nomUsuario.grid(row=0, column=1,rowspan=2,columnspan=1)
nomUsuario.config(padx = 5,bg= "#b7b493",fg="#FFFFFF", anchor=W, font=("Helvetica", 12))

# ------------------------------- Crea Fecha -----------------------------------

def recuperaFechaActual():
    print("Ha entrado")      
    fecha = datetime.now()
    diaGlobal = str(fecha.day)
    #if int(diaGlobal) < 10: diaGlobal = "0" + diaGlobal
    diaGlobaltk = StringVar()
    diaGlobaltk.set(diaGlobal)
    mesGlobal = str(fecha.month)
    #if int(mesGlobal) < 10: mesGlobal = "0" + mesGlobal
    mesGlobaltk = StringVar()
    mesGlobaltk.set(mesGlobal)
    anyoGlobal = str(fecha.year)
    anyoGlobaltk = StringVar()
    anyoGlobaltk.set(anyoGlobal)

    diaFecha.config(text=diaGlobaltk)
    mesFecha.config(text=mesGlobaltk)
    anyoFecha.config(text=anyoGlobaltk)
    frameFecha.config(bg = "#b7b493")
    textFecha.config(bg = "#b7b493")
    textBarra1.config(bg = "#b7b493")
    textBarra2.config(bg = "#b7b493")
    textSpace.config(bg = "#b7b493") 
     
ConfiguraColumnas(frameFecha,7,5,2,1,2,1,4,1,12)

textFecha = Label(frameFecha,text="Data:",textvariable="Data:")
textFecha.grid(row=0, column=0,rowspan=1,columnspan=1)
textFecha.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor=E, font=("Helvetica", 12, "bold"))
textFecha.grid(padx=10, pady=10)
    
diaFecha = Entry(frameFecha,textvariable=diaGlobaltk,justify = CENTER)
diaFecha.grid(row=0, column=1)
diaFecha.config(bg="#5d5b45",fg="#FFFFFF",  width = 2, font=("Helvetica", 12))
diaFecha.bind("<KeyRelease>",MiraFecha)

textBarra1 = Label(frameFecha,text="/",textvariable="/")
textBarra1.grid(row=0, column=2,rowspan=1,columnspan=1)
textBarra1.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor=E, font=("Helvetica", 12, "bold"))
textBarra1.grid(padx=10, pady=10)

mesFecha = Entry(frameFecha,textvariable=mesGlobaltk,justify = CENTER)
mesFecha.grid(row=0, column=3)
mesFecha.config(bg="#5d5b45",fg="#FFFFFF",  width = 2, font=("Helvetica", 12))
mesFecha.bind("<KeyRelease>",MiraFecha)

textBarra2 = Label(frameFecha,text="/",textvariable="/")
textBarra2.grid(row=0, column=4,rowspan=1,columnspan=1)
textBarra2.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor=E, font=("Helvetica", 12, "bold"))
textBarra2.grid(padx=10, pady=10)

anyoFecha = Entry(frameFecha,textvariable=anyoGlobaltk,justify = CENTER)
anyoFecha.grid(row=0, column=5)
anyoFecha.config(bg="#5d5b45",fg="#FFFFFF",  width = 4, font=("Helvetica", 12))
anyoFecha.bind("<KeyRelease>",MiraFecha)

textSpace = Label(frameFecha,text=" ",textvariable=" ")
textSpace.grid(row=0, column=6,rowspan=1,columnspan=1)
textSpace.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor=E, font=("Helvetica", 12, "bold"))
textSpace.grid(padx=10, pady=10)

botonRegresaFecha = creaBoton("botonRegresaFecha",frameFecha,"Torna a avui",recuperaFechaActual,0,7,"#27779d","#FFFFFF",1,12,"green")

#------------------------------- Crea Botonera -------------------------------------

ConfiguraColumnas(frameBotones,4,1,1,1,1,1,1,1)

Label(frameBotones,text=" ",bg="#b7b493").grid(row=0,column=0)

BB1 = Button(frameBotones, text="-", command=TamanyoMenos, font=(10))
BB1.grid(row=0, column=1)
BB1.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 5)
BB1.grid(pady=10)
cambiaPasaEncima(BB1,"green","#27779d")


BB2 = Button(frameBotones, text="+", command=TamanyoMas, font=(10))
BB2.grid(row=0, column=2)
BB2.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 5)
cambiaPasaEncima(BB2,"green","#27779d")

Label(frameBotones,text=" ",bg="#b7b493").grid(row=0,column=3)

BB5 = Button(frameBotones, text="ant.", font=(10))
BB5.grid(row=0, column=4)
BB5.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 5)
cambiaPasaEncima(BB5,"green","#27779d")

BB6 = Button(frameBotones, text="post.", font=(10))
BB6.grid(row=0, column=5)
BB6.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 5)
cambiaPasaEncima(BB6,"green","#27779d")

Label(frameBotones,text=" ",bg="#b7b493").grid(row=0,column=6)

BB7 = Button(frameBotones, text="PDF (P)", font=(10))
BB7.grid(row=0, column=7)
BB7.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
cambiaPasaEncima(BB7,"green","#27779d")

Label(frameBotones,text=" ",bg="#b7b493").grid(row=0,column=8)

# ------------------------------ Crea etiquetas de menú ----------------------

tamanyoFont = TamanyoLetra+15
textMenu = Label(frameMenu,text="")
textMenu.grid(row=0, column=0,rowspan=1,columnspan=1)
textMenu.config(padx = 5,bg="#5d5b45",fg="#FFFFFF", font=("Helvetica", tamanyoFont,"bold"),width = 19)

for i in range(0,13):
    
    globals()['BM%s' % (i)] = Button(frameMenu, text="", command=regresaSinNada, font=("Helvetica", tamanyoFont))
    globals()['BM%s' % (i)].grid(row=i+1, column=0)
    globals()['BM%s' % (i)].config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 20, relief='groove')
    cambiaPasaEncima(globals()['BM%s' % (i)],"green","#27779d")
    globals()['BM%s' % (i)].grid(padx=5, pady=2)
    # Cambia el color del botón cuando está enfocado
    globals()['BM%s' % (i)].bind("<FocusIn>", lambda event, i=i: globals()['BM%s' % (i)].config(bg="#87779d"))
    # Devuelve el color original si el botón no está enfocado
    globals()['BM%s' % (i)].bind("<FocusOut>", lambda event, i=i: globals()['BM%s' % (i)].config(bg="#27779d"))
    if i>1: 
        globals()['BM%s' % (i)].bind("<Up>", lambda event, i=i: globals()['BM%s' % (i-1)].focus_set())
    if i<11:
        globals()['BM%s' % (i)].bind("<Down>", lambda event, i=i: globals()['BM%s' % (i+1)].focus_set())
tamanyoFont = TamanyoLetra+12
creaLabel("sep1",frameMenu," ",1,0,1,1,5,"#b7b493","#b7b493",E,tamanyoFont,"bold")   
creaLabel("sep2",frameMenu," ",14,0,1,1,5,"#b7b493","#b7b493",E,tamanyoFont,"bold")  

# ------------------------------ Crea etiquetas de cuestionario ---------------

ConfiguraColumnas(frameRellena,2,1,3)
tamanyoFont = TamanyoLetra+10

mantieneDistancia = Label(frameRellena,text="")
mantieneDistancia.grid(row=0, column=1,rowspan=1,columnspan=1)
mantieneDistancia.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor = E, font=("Helvetica", tamanyoFont,"bold"),width = 30)

# LRx = título; LRRx = texto; LRRx1 = Combobox; LRRx2 = Entry; LRRx3 = Text (multilinea)

for i in range (1,24):
    globals()['LR%s' % (i)] = Label(frameRellena,text="")   
    globals()['LR%s' % (i)].grid(row=i-1, column=0,rowspan=1,columnspan=1)
    globals()['LR%s' % (i)].config(padx = 5,bg="#b7b493",fg="#000000", anchor = E, font=("Helvetica", tamanyoFont,"bold"),width = 15)

    globals()['LRR%s' % (i) + '1'] = Combobox(frameRellena,state="readonly")                                                                                  
    globals()['LRR%s' % (i) + '1'].grid(rowspan=1,columnspan=1)
    globals()['LRR%s' % (i) + '1'].config(font=("Helvetica", tamanyoFont),width = 30)
    globals()['LRR%s' % (i) + '1'].grid(padx=10, pady=10)
    globals()['LRR%s' % (i) + '1'].bind('<Key>', pulsaTeclaCombobox)                 # Para que se actualice el combobox cuando se pulsa una tecla
    
    globals()['LRR%s' % (i) + '2'] = Entry(frameRellena)                                                                                                    
    globals()['LRR%s' % (i) + '2'].grid(rowspan=1,columnspan=1)
    globals()['LRR%s' % (i) + '2'].config(font=("Helvetica", tamanyoFont),width = 33)
    globals()['LRR%s' % (i) + '2'].grid(padx=10, pady=10)

# LRR31.bind('<Key>', pulsaTeclaCombobox)                 # Para que se actualice el combobox cuando se pulsa una tecla

LRR1 = Label(frameRellena,text="PENDIENTE")                                                                                      
LRR1.grid(rowspan=1,columnspan=1)
LRR1.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor = W, font=("Helvetica", tamanyoFont),width = 30)

LRR5 = Label(frameRellena,text="")                                                                                      
LRR5.grid(rowspan=1,columnspan=1)
LRR5.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor = W, font=("Helvetica", tamanyoFont),width = 30)

LRR6 = Label(frameRellena,text="")                                                                                      
LRR6.grid(rowspan=1,columnspan=1)
LRR6.config(padx = 5,bg="#b7b493",fg="#FFFFFF", anchor = W, font=("Helvetica", tamanyoFont),width = 30)

LRR73 = Text(frameRellena)
LRR73.grid(rowspan=1,columnspan=1)
LRR73.config(font=("Helvetica", tamanyoFont),width = 32,height = 5,state = NORMAL)

LRR213 = Text(frameRellena)
LRR213.grid(rowspan=1,columnspan=1)
LRR213.config(font=("Helvetica", tamanyoFont),width = 32,height = 5,state = NORMAL)
bindNotasEvento(LRR213)

LR22.grid(columnspan=3)
LR22.config(fg = "blue",width = 30)
LR23.grid(columnspan=3)
LR23.config(fg = "red",width = 30)

BB4 = Button(frameRellena, text="Valida  (int)", font=(10))
BB4.grid(row=23, column=0,columnspan=1)
BB4.config(bg="#27779d",fg="#27779d",  height = 1, width = 10)
BB4.grid(padx=10, pady=10)

cambiaPasaEncima(BB4,"grey","#27779d")
BB3 = Button(frameRellena, text="neteja (N)", command=LimpiaElegibles, font=(10))
BB3.grid(row=23, column=1, columnspan=1)
BB3.config(bg="#27779d",fg="#FFFFFF",  height = 1, width = 10)
BB3.grid(padx=10, pady=10)

cambiaPasaEncima(BB3,"green","#27779d")

# ------------------------------ Bases de datos -------------------------------

# Creamnos la base de datos o conectamos con ella si ya existe
base_datos_datos = sqlite3.connect('databases/basesDeDatosDatos.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

# Creamos las tablas (en caso de que existan saltarán este paso)

try:
    cursor.execute("""CREATE TABLE bd_productos (
        NOM             text,
        PREU_HABITUAL   text,
        PREU_ACTUAL     text,
        REGISTRABLE     text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

try:
    cursor.execute("""CREATE TABLE bd_usuarios (
        NOM             text,
        CLAVE           text,
        NIVEL           text,
        INGLES          text,
        CASTELLANO      text,
        CATALAN         text,
        FRANCES         text,
        HORASMES        text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass


# Cierra la conexión con la base de datos
base_datos_datos.close()

# Creamnos la base de datos o conectamos con ella si ya existe
base_datos_datos = sqlite3.connect('databases/basesDeDatosClientes.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

try:
    cursor.execute("""CREATE TABLE bd_clientes (
        NOM             text,
        DIRECCION1      text,
        DIRECCION2      text,
        DIRECCION3      text,
        TELEFONO        text,
        MAIL            text,
        NIFCIF          text,
        CONTACTO        text,
        TELCONTACTO     text,
        MAILCONTACTO    text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

# Cierra la conexión con la base de datos
base_datos_datos.close()

# Creamnos la base de datos o conectamos con ella si ya existe
base_datos_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

# Creamos la tabla (en caso de que exista saltará este paso)

try:
    cursor.execute("""CREATE TABLE bd_registros (
        USUARIO         text,
        FECHA           text,
        DESCRIPCION     text,
        ORIGEN          text,
        HORA            text,
        PRODUCTO        text,
        FUENTE          text,
        NOTAS           text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

# Cierra la conexión con la base de datos
base_datos_datos.close()

# Creamnos la base de datos o conectamos con ella si ya existe
base_datos_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

# Creamos la tabla (en caso de que exista saltará este paso)

try:
    cursor.execute("""CREATE TABLE bd_incidencias (
        FECHA           text,
        HORA            text,
        PAX1            text,
        PAX2            text,
        PRODUCTO        text,
        IDIOMA          text,
        TEL_EXTRA       text,
        ESTADO          text,
        USUARIO         text,
        FECHA_CREA      text,
        CLIENTE         text,
        MAIL_EXTRA      text,
        PRECIO1         text,
        TIPO1           text,
        PRECIO2         text,
        TIPO2           text,
        AGENDADO        text,
        FECHA_REV       text,
        PAGAT           text,
        NOTAS           text,
        FACTURA         text,
        CONTACTO        text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

try:
    cursor.execute("""CREATE TABLE bd_bloqueos (
        FECHA           text,
        DESDE           text,
        HASTA           text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

# Cierra la conexión con la base de datos
base_datos_datos.close()

# Creamnos la base de datos o conectamos con ella si ya existe
base_datos_datos = sqlite3.connect('databases/basesDeDatosProforma.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

# Creamos la tabla (en caso de que exista saltará este paso)

try:
    cursor.execute("""CREATE TABLE bd_Proforma (
        FECHA           text,
        FECHA_PRO       text,
        NUM_PRO         text,
        CLIENTE         text,
        CANT_1          text,
        CONCEPT_1       text,
        PRECIO_1        text,
        CANT_2          text,
        CONCEPT_2       text,
        PRECIO_2        text,
        IVA             text,
        TIPO_IVA        text,
        INCLUIDO_IVA    text,
        ID_INCIDENCIA   text,
        PARTE           text,)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

# Cierra la conexión con la base de datos
base_datos_datos.close()

# ------------------------------ Loop -----------------------------------------
crea_espacios_info(frameLista,10,22)
MenuInicial()
if  DatosUsuario == ():     DatosUsuario = cargaUsuario()  
raiz.mainloop()  