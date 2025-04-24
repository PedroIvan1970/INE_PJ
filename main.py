from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar la base de datos CSV
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

    # 💡 Mostrar mensaje si solo hay filtro por entidad o ningún filtro
    filtros_aplicados = [k for k, v in filtros.items() if v]
    if filtros_aplicados == ["entidad"] or not filtros_aplicados:
        return jsonify({
            "detalle": "La respuesta a tu consulta es excesivamente larga. Puedes filtrar por nombre, posición en la boleta, cargo, etc."
        })

    return jsonify(resultados.fillna("").to_dict(orient="records"))

