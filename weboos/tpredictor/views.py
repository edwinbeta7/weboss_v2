from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

n_estimators_value =100
model = RandomForestRegressor(n_estimators=n_estimators_value, random_state=42)

def tpredictor(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        print(action)
        
        if action == "fit":
            print(f"fit")

            #Cargar archivo
            ruta_archivo = 'data_4g_df0.xlsx'
            print(f"Cargando datos {ruta_archivo} ...")
            df0 = pd.read_excel(ruta_archivo)

            # Definimos Dataset y variable supervisada
            X = df0.drop('THROUGHPUTUSER_DL_MBPS', axis=1)            
            print(f"Definiendo X_datos ...")
            y = df0['THROUGHPUTUSER_DL_MBPS']           
            print(f"Definiendo y_datos ...")
            n_estimators_value =100

            #defino data de test y data de prueba para entrenamiento        
            print(f"Definiendo X_train, X_test, y_train, y_test ...")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2 , random_state=42)

            # Crear y entrenar el modelo    
            print(f"Entrenando Modelo ...")
            #model = RandomForestRegressor(n_estimators=n_estimators_value, random_state=42)
            model.fit(X_train, y_train)

            # Hacer predicciones
            y_pred = model.predict(X_test)

            # Evaluar el modelo
            print(f"Evaluando Modelo ...")
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            print(f"n_estimators: {n_estimators_value}")
            print(f"Error cuadrático medio: {mse}")
            print(f"R2 Score: {r2} \n")
            n_estimators_value = f"n_estimators: {n_estimators_value}"
            mse = f"Error cuadrático medio: {mse}"
            r2 = f"R2 Score: {r2}"
            return render(request, 'tpredictor.html', {'n_estimators': n_estimators_value,'mse': mse,'r2': r2})

        elif action == "Predecir":
            HORA = float(request.POST.get('HORA'))
            PER_DISPONIBILIDAD = float(request.POST.get('PER_DISPONIBILIDAD'))
            TRAFFIC_DATA_MB = float(request.POST.get('TRAFFIC_DATA_MB'))
            TRAFICO_VOZ_ERL = float(request.POST.get('TRAFICO_VOZ_ERL'))
            USERS = float(request.POST.get('USERS'))
            RECUSRSOS_DL = float(request.POST.get('RECUSRSOS_DL'))
            PER_USO_RECURSOS_DL = float(request.POST.get('PER_USO_RECURSOS_DL'))
            INTENTOS_RRC = float(request.POST.get('INTENTOS_RRC'))
            PER_FAIL_RRC = float(request.POST.get('PER_FAIL_RRC'))
            PER_DROP_DATOS = float(request.POST.get('PER_DROP_DATOS'))
            PWR_INTERFER_UL = float(request.POST.get('PWR_INTERFER_UL'))
            CQI = float(request.POST.get('CQI'))
            PER_DL_PKTLOSS = float(request.POST.get('PER_DL_PKTLOSS'))
            CPU_LOAD = float(request.POST.get('CPU_LOAD'))
            PER_DROP_VOZ = float(request.POST.get('PER_DROP_VOZ'))
            SITIO_SECTOR = float(request.POST.get('SITIO_SECTOR'))         
            X_valores =np.array([[HORA,  PER_DISPONIBILIDAD,  TRAFFIC_DATA_MB,  TRAFICO_VOZ_ERL,
                                USERS,  RECUSRSOS_DL,  PER_USO_RECURSOS_DL,  INTENTOS_RRC,
                                PER_FAIL_RRC, PER_DROP_DATOS, PWR_INTERFER_UL,  CQI,
                                PER_DL_PKTLOSS,  CPU_LOAD,  PER_DROP_VOZ,  SITIO_SECTOR]])
            y_pred = model.predict(X_valores)
            valor1 = f"Predicción THROUGHPUTUSER_DL_MBPS: {y_pred} MBPS"
            return render(request, 'tpredictor.html', {'valor1': valor1})

    else:
        return render(request, 'tpredictor.html')