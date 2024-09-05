import subprocess

from flask import Flask, request, jsonify
import firewall_manager as nft
import json
app = Flask(__name__)


# Endpoint para listar todas las reglas (ruleset completo)
@app.route('/ruleset', methods=['GET'])
def get_ruleset():

    ruleset=nft.list_ruleset()
    output = {
        "tables": {}
    }
    lines = ruleset.splitlines()
    current_table=None
    current_chain=None

    for line in lines:
        line = line.strip()
        if line.startswith('table'):
            _, family, table_name = line.split()[:3]
            current_table = table_name
            output["tables"][current_table] = {
                "family": family,
                "chains": {}
            }

        elif line.startswith('chain'):
            _, chain_name = line.split()[:2]
            current_chain = chain_name
            output["tables"][current_table]["chains"][current_chain]={
                "rules":[]
            }

        elif line.startswith('type') or line.startswith('policy'):
            # Regla asociada a la cadena
            output["tables"][current_table]["chains"][current_chain]["rules"].append(line)
        elif line and not line.startswith('}') and current_chain:
            output["tables"][current_table]["chains"][current_chain]["rules"].append(line)


    return jsonify(output)


@app.route('/tables', methods=['POST'])
def create_table():
    try:
        data = request.json
        name = data.get('name')
        if name:
            nft.add_table(name)
            return jsonify({"message": f"Tabla '{name}' añadida"}), 201
        else:
            return jsonify({"error": "Falta el nombre de la tabla"}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

@app.route('/tables', methods=['GET'])
def get_tables():
    try:
        data=str(nft.list_tables()).splitlines()
        return jsonify({"message": 'Listado de tablas ejecutado: ', "tables": data})
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route('/tables/<string:name>', methods=['DELETE'])
def delete_table(name):
    try:
        nft.delete_table(name)
        return jsonify({"message": f"Tabla '{name}' eliminada"})
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route('/tables/<string:name>/flush', methods=['POST'])
def flush_table(name):
    try:
        nft.flush_table(name)
        return jsonify({"message": f"Tabla '{name}' vaciada"})
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route('/tables/<string:table>/chains', methods=['POST'])
def create_chain(table):
    try:
        data = request.json
        name = data.get('name')
        type = data.get('type')
        hook = data.get('hook')
        priority = data.get('priority')
        policy = data.get('policy')
        comment = data.get('comment')

        if name and type and hook and priority:
            nft.add_chain(table, name, type, hook, priority, policy, comment)
            return jsonify({"message": f"Cadena '{name}' añadida a la tabla '{table}'"}), 201
        else:
            return jsonify({"error": "Faltan parámetros necesarios para crear la cadena"}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route('/tables/<string:table>/chains/<string:name>', methods=['DELETE'])
def delete_chain(table, name):
    try:
        nft.delete_chain(table, name)
        return jsonify({"message": f"Cadena '{name}' eliminada de la tabla '{table}'"})
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route('/tables/<string:table>/chains/<string:chain>/rules', methods=['POST'])
def create_rule(table, chain):
    try:
        data = request.json
        rule = data.get('rule')
        if rule:
            nft.add_rule(table, chain, rule)
            return jsonify({"message": f"Regla añadida a la cadena '{chain}' en la tabla '{table}'"}), 201
        else:
            return jsonify({"error": "Falta la regla a añadir"}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route('/tables/<string:table>/rules', methods=['GET'])
def get_rules_from_table(table):
    try:
        data = str(nft.list_rules_from_tables(table)).splitlines()
        return jsonify({"message": f"Listado de reglas en la tabla '{table}'", "rules": data})
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route('/tables/<string:table>/chains/<string:chain>/rules/<int:handle>', methods=['DELETE'])
def delete_rule(table, chain, handle):
    try:
        nft.delete_rule(table, chain, str(handle))
        return jsonify({"message": f"Regla con handle '{handle}' eliminada de la cadena '{chain}' en la tabla '{table}'"})
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
