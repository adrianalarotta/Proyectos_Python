import pandas as pd
import sqlite3

z = 0
maestros = {}#almacenar datos de los maestros
clientes = {}
c={}#guarda el cc de los maestros que ya tenia almacenados en la base de datos
fact={}#guarda el numero de factura y su valor
CYM={}#guarda la relacion del cliente con el maestro que fue referido
pun={}#guarda los puntos por cada cliente
punt={}#almacena los puntos totales para cada maestro
CYV={}#diccionario para almacenar la cedula y vlor de compra del cliente


class CRM:  # Definición de la clase
    def agregar_maestro(self): #Definir el metodo de agregar un maestro
        print('')
        print('Añadir Maestro Nuevo')
        print(' ')
        conn=sqlite3.connect('CRMDB.db')# conectar a la base de datos
        cur= conn.cursor() # Acceso a la base de datos
        cur.execute("""CREATE TABLE IF NOT EXISTS MAESTRO (CCM INTEGER UNIQUE,
                                   NOMBRE TEXT, CUMPLEANOS TEXT ,CORREO TEXT ,TELEFONO INTEGER)""")# crear la tabla si no existe

        self.ccm = input('ingrese el numero de cedula ') #solicitar la cedula del maestro


        if self.ccm in maestros:
            print('El maestro ya esta creado')
        else: #solicita todos los atributos.
            self.nombrem = input('ingrese nombre ')
            self.cumpleanos = input('ingrese la fecha de cumpleaños')
            self.telefonom = int(input('ingrese número telefónico '))
            self.correom = input('ingrese correo electrónico ')
            maestros[self.ccm] = ('nombre', self.nombrem, 'fecha_cumple', self.cumpleanos,
                                  'telefono', self.telefonom, 'coreo', self.correom, '')
            #agregar a la clave(cc del maestro) y en el valor de una tupla compuesta por los datos del maestro
            print(maestros)
        try:
            cur.execute("""INSERT INTO MAESTRO (CCM,NOMBRE, CUMPLEANOS, CORREO, TELEFONO) VALUES(?,?,?,?,?) """,
                    (self.ccm, self.nombrem,
                     self.cumpleanos,
                     self.correom, self.telefonom))#inserta los datos en la tabla maestro
            conn.commit()  # guarda las actualizaciones en la tabla.
            print('Maestro agregado exitosamente')
        except:
            print('Maestro no valido. Verifique que el maestro no este creado')

            conn.commit()#guarda las actualizaciones en la tabla.
            conn.close()#cierra la conexión con la base.
    def cliente(self):

        print('')
        print('Añadir Cliente Nuevo')
        print(' ')
        conexion = sqlite3.connect('CRMDB.db')
        cursor = conexion.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS CLIENTES (CC INTEGER,
                                           NOMBRE TEXT ,CORREO TEXT ,TELEFONO INTEGER,MAESTRO INTEGER)""")
        self.cc = input('ingrese el numero de cedula ')
        if self.cc in clientes:
            print('El cliente ya esta creado')
        else:
            self.nombre = input('ingrese nombre ')
            self.telefono = int(input('ingrese número telefónico '))
            self.correo = input('ingrese correo electrónico ')
            self.maestro = input('ingrese la cedula del maestro')


            cursor.execute('SELECT * FROM MAESTRO ') # Recuperamos los registros de la tabla de MAESTRO
            maes=cursor.fetchall()# Recorremos todos los registros con fetchall
            for self.ccm in maes: # Ahora podemos recorrer todos los MAESTROS y los obtengo dentro de tuplas
                c[int(self.ccm[0])]=self.ccm[1]#guardo las cedulas de los maestros que ya estaban en la base de datos dentro de un diccionario
            print(self.maestro)
            if self.maestro in maestros or int(self.maestro) in c:#
                clientes[self.cc] = ('nombre', self.nombre, 'telefono', self.telefono, 'coreo', self.correo, 'maestro', self.maestro)
                print(clientes)

            else:
                print('el numero de cedula del maestro digitado no existente ')

            cursor.execute("""INSERT INTO CLIENTES (CC,NOMBRE, CORREO, TELEFONO,MAESTRO) VALUES(?,?,?,?,?) """,
                           (self.cc, self.nombre,
                            self.correo, self.telefono, self.maestro))
            conexion.commit()


    def factura(self):
        conn = sqlite3.connect('CRMDB.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS FACTURAS (FACTURA N° TEXT,
                                           CC CLIENTES INTEGER,VALOR DE FACTURA INTEGER)""")

        x = pd.ExcelFile('puntos.xlsx')#A través de pandas se conectó al archivo puntos
        df = x.parse('Hoja1') #convertí la hoja 1 en un data frame
        print(df)
        l = df['NF']#extrae los valores de la columna llamada NF
        l1=df['CC']
        l2=df['V']
        a = list(l)#Vectoriza el listado
        b=list(l1)
        c=list(l2)
        v=range(0,len(a))
        for i in v:
            #print(a[i])
            cur.execute('SELECT * FROM FACTURAS ')  # Seleciono las facturas
            facturas = cur.fetchall()  # Vectorizo las facturas
            for self.fac in facturas:  # Ahora podemos recorrer todos las facturas y los obtengo dentro de una tupla
                fact[self.fac[0]] = self.fac[2]
                # guardo el numero de las facturas con su valor en un diccionario
                CYV[self.fac[1]]=self.fac[2]
            if a[i] in fact:
                print('la factura ya existe ')# Evaluo que la factura no este cargada previamente
            else:
                cur.execute("""INSERT INTO FACTURAS (FACTURA,CC,VALOR) VALUES(?,?,?) """,
                            (a[i], b[i],
                             c[i]))# Inserto cada campo del excel en la base
                conn.commit()

    def reporte(self):
        conn = sqlite3.connect('CRMDB.db')
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS PUNTOS_PARCIALES')
        cur.execute('DROP TABLE IF EXISTS PUNTOS_TOTALES')
        cur.execute("""CREATE TABLE IF NOT EXISTS PUNTOS_PARCIALES (CC_MAESTRO INTEGER,CC_CLIENTE INTEGER ,PUNTOS_ACUMULADOS INTEGER)""")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS PUNTOS_TOTALES (CC_MAESTRO INTEGER ,PUNTOS_ACUMULADOS INTEGER)""")
        cur.execute('SELECT * FROM  CLIENTES')  # Recuperamos los registros de la tabla de CLIENTES
        cli= cur.fetchall()  # Vectorizar todos los registros de los clientes con fetchall
        for i in cli:  # Ahora podemos recorrer todos las facturas y los obtengo dentro de una tupla
            CYM[i[0]] = i[4]#en mi diccionario CYM relaciono la cedula del cliente con la cedula del maestro
        for clave in CYM.keys():#accedo a las claves de mi diccionario CYM
            for clave2 in CYV.keys():#accedo a las claves de mi diccionario CYV(cedula cliente y valor factura)
                if clave==clave2:#valido que las claves de mis dos ciccionarios sean iguales
                    p=CYV[clave2]#guardo en mi variable p el valor de la factura
                    print('v',CYM[clave])
                    if CYM[clave] in pun:#hago la validacion que la cedula del maestro ya se encuentra en mi dicionario pun(puntos parciales)
                        v=float(pun[CYM[clave]])+float(p/1000)#en mi variable v sumo los puntos totales para cada maestro
                        punt[CYM[clave]]=v#en mi diccionario punt(puntos totales) guardo en la clave la cedula del maestro y en su valor los puntos totales
                    pun[CYM[clave]]=p/1000#en mi diccionario pun guardo la cedula del maestro y el valor de compra dividida en 1000
                    if CYM[clave] not in punt: #hago la validacion que esa cedula de maestro no este en puntos totales
                        punt[CYM[clave]] = p / 1000#guardo en mi diccionario punt la cedula del maestro y los puntos (valor factura/1000)

                    cur.execute("""INSERT INTO PUNTOS_PARCIALES (CC_MAESTRO ,CC_CLIENTE,PUNTOS_ACUMULADOS) VALUES(?,?,?) """,
                                (CYM[clave],clave,p/1000))
                    conn.commit()
                    print(pun)
        print(pun)
        for i in punt:
            cur.execute("""INSERT INTO PUNTOS_TOTALES (CC_MAESTRO ,PUNTOS_ACUMULADOS) VALUES(?,?) """,
                        (i, punt[i]))
            conn.commit()
        print('puntos totales ', punt)


    def actualizar(self):
        c=input('digite el numero cedula de cliente que quiere actualizar ')
        cm=input('digite el numero de cedula del maestro que quiere actualizar')
        conn = sqlite3.connect('CRMDB.db')
        cur = conn.cursor()
        cur.execute(''' UPDATE CLIENTES SET MAESTRO = '%s' WHERE CC = '%s' '''%(cm,c))
        conn.commit()
        conn.close()


CRM = CRM()

while z == 0:
    print('Bienvenido al administrador de CRM para los maestros\n'
          ' 1. Añadir Maestro', '\n',
          '2. Añadir Cliente\n',
          '3. Actualizar Facturas\n',
          '4. Generar reporte\n',
          '5. Actualizar Base de Datos\n',
          '6. Cerrar')
    op = int(input('digite su opcion'))
    if op == 1:
        CRM.agregar_maestro()
    elif op == 2:
        CRM.cliente()
    elif op == 3:
        CRM.factura()
    elif op== 4:
        CRM.factura()
        CRM.reporte()
    elif op == 5:
        CRM.actualizar()
    elif op == 6:
        print('gracias por usar CRM')
        z = 1