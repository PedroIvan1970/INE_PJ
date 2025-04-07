from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("baseDatosCandidatos-CSV.csv")
df.columns = [col.lower().strip() for col in df.columns]

@app.route("/candidatos", methods=["GET"])
def get_candidatos():
    filtros = {
        "nombre_candidato": request.args.get("nombre"),
        "cargo": request.args.get("cargo"),
        "entidad": request.args.get("entidad"),
        "num_lista_en_boleta": request.args.get("posicion")
    }

    resultados = df.copy()
    for campo, valor in filtros.items():
        if valor:
            if campo == "num_lista_en_boleta":
                try:
                    valor = int(valor)
                    resultados = resultados[resultados[campo] == valor]
                except ValueError:
                    continue
            else:
                resultados = resultados[resultados[campo].str.contains(valor, case=False, na=False)]

    return jsonify(resultados.to_dict(orient="records"))

@app.route("/candidato", methods=["GET"])
def get_candidato():
    nombre = request.args.get("nombre")
    if not nombre:
        return jsonify({"error": "Falta el nombre del candidato"}), 400

    resultado = df[df["nombre_candidato"].str.contains(nombre, case=False, na=False)]
    if resultado.empty:
        return jsonify({"error": "Candidato no encontrado"}), 404

    return jsonify(resultado.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)

