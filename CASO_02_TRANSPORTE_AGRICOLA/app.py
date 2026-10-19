from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Cargar y entrenar el modelo al iniciar
datos = pd.read_csv('datos.csv')
X = datos[['distancia_km', 'carga_kg', 'via_no_asfaltada']]
y = datos['costo_transporte_soles']

modelo = LinearRegression()
modelo.fit(X, y)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulador', methods=['GET', 'POST'])
def simulador():
    resultado = None
    error = None
    v = {'distancia': 25, 'carga': 400, 'via': 0}
    
    if request.method == 'POST':
        try:
            v['distancia'] = float(request.form['distancia_km'])
            v['carga'] = float(request.form['carga_kg'])
            v['via'] = int(request.form['via_no_asfaltada'])
            
            entrada = pd.DataFrame([[v['distancia'], v['carga'], v['via']]], 
                                   columns=['distancia_km', 'carga_kg', 'via_no_asfaltada'])
            resultado = round(modelo.predict(entrada)[0], 2)
        except Exception:
            error = "Por favor ingresa valores numéricos válidos."
            
    return render_template('simulador.html', resultado=resultado, error=error, v=v)

@app.route('/comparar', methods=['GET', 'POST'])
def comparar():
    res_a, res_b = None, None
    va = {'distancia': 25, 'carga': 400, 'via': 0}
    vb = {'distancia': 100, 'carga': 1200, 'via': 1}
    
    if request.method == 'POST':
        try:
            va['distancia'] = float(request.form['dist_a'])
            va['carga'] = float(request.form['carga_a'])
            va['via'] = int(request.form['via_a'])
            
            vb['distancia'] = float(request.form['dist_b'])
            vb['carga'] = float(request.form['carga_b'])
            vb['via'] = int(request.form['via_b'])
            
            df_a = pd.DataFrame([[va['distancia'], va['carga'], va['via']]], columns=['distancia_km', 'carga_kg', 'via_no_asfaltada'])
            df_b = pd.DataFrame([[vb['distancia'], vb['carga'], vb['via']]], columns=['distancia_km', 'carga_kg', 'via_no_asfaltada'])
            
            res_a = round(modelo.predict(df_a)[0], 2)
            res_b = round(modelo.predict(df_b)[0], 2)
        except Exception:
            pass
            
    return render_template('comparar.html', res_a=res_a, res_b=res_b, va=va, vb=vb)

@app.route('/modelo')
def modelo_info():
    return render_template('modelo.html')

if __name__ == '__main__':
    app.run(debug=True)