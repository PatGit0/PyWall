function getRuleset() {
    axios.get('http://localhost:5000/ruleset')
        .then(response => {
            const rulesetDiv = document.getElementById('ruleset');
            rulesetDiv.innerHTML = ''; // Limpiar contenido previo

            // Formatear el JSON en HTML
            const tables = response.data.tables;
            for (const table in tables) {
                const tableDiv = document.createElement('div');
                tableDiv.innerHTML = `<h4>Tabla: ${table}</h4>`;

                const chains = tables[table].chains;
                for (const chain in chains) {
                    const chainDiv = document.createElement('div');
                    chainDiv.innerHTML = `<p>Cadena: ${chain}</p>`;

                    // Mostrar reglas asociadas a la cadena
                    const rules = chains[chain].rules;
                    const rulesList = document.createElement('ul');
                    rules.forEach((rule, index) => {
                        const ruleItem = document.createElement('li');
                        ruleItem.textContent = rule;
                        rulesList.appendChild(ruleItem);
                    });
                    chainDiv.appendChild(rulesList);

                    // Botón para eliminar la cadena
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Eliminar Cadena';
                    deleteButton.onclick = () => deleteChain(table, chain);
                    chainDiv.appendChild(deleteButton);

                    // Agregar cadenas al div de la tabla
                    tableDiv.appendChild(chainDiv);
                }

                // Formulario para añadir nueva cadena
                const addChainForm = document.createElement('form');
                addChainForm.innerHTML = `
                    <label for="chainName-${table}">Nombre de la Cadena:</label>
                    <input type="text" id="chainName-${table}" required>

                    <label for="chainType-${table}">Tipo de Cadena:</label>
                    <select id="chainType-${table}">
                        <option value="filter">filter</option>
                        <option value="nat">nat</option>
                        <option value="route">route</option>
                    </select>

                    <label for="chainHook-${table}">Hook:</label>
                    <input type="text" id="chainHook-${table}" required>

                    <label for="chainPriority-${table}">Prioridad:</label>
                    <input type="text" id="chainPriority-${table}" required>

                    <button type="button" onclick="addChain('${table}')">Añadir Cadena</button>
                `;

                // Agregar el formulario al div de la tabla
                tableDiv.appendChild(addChainForm);
                rulesetDiv.appendChild(tableDiv);
            }
        })
        .catch(error => {
            console.error('Error al obtener las reglas:', error);
        });
}

function addChain(tableName) {
    const name = document.getElementById(`chainName-${tableName}`).value;
    const type = document.getElementById(`chainType-${tableName}`).value;
    const hook = document.getElementById(`chainHook-${tableName}`).value;
    const priority = document.getElementById(`chainPriority-${tableName}`).value;

    if (name && type && hook && priority) {
        axios.post(`http://localhost:5000/tables/${tableName}/chains`, {
            name: name,
            type: type,
            hook: hook,
            priority: priority,
        })
        .then(response => {
            alert(response.data.message);
            getRuleset();  // Actualiza las reglas después de crear la cadena
            document.getElementById(`chainName-${tableName}`).value = ''; // Reinicia el campo
            document.getElementById(`chainHook-${tableName}`).value = ''; // Reinicia el campo
            document.getElementById(`chainPriority-${tableName}`).value = ''; // Reinicia el campo
        })
        .catch(error => {
            console.error('Error al añadir la cadena:', error);
        });
}
}

function deleteChain(tableName, chainName) {
    axios.delete(`http://localhost:5000/tables/${tableName}/chains/${chainName}`)
        .then(response => {
            alert(response.message);
            getRuleset(); // Actualiza las reglas después de eliminar
        })
        .catch(error => {
            console.error('Error al eliminar la cadena:', error);
        });
}

function createTable() {
    // Implementa la lógica para crear una tabla
    const tableName = prompt("Ingrese el nombre de la tabla:");
    if (tableName) {
        axios.post('http://localhost:5000/tables', { name: tableName })
            .then(response => {
                alert(response.data.message);
                getRuleset();  // Actualiza las reglas después de crear
            })
            .catch(error => {
                console.error('Error al crear la tabla:', error);
            });
    }
}

function deleteTable() {
    // Implementa la lógica para eliminar una tabla
    const tableName = prompt("Ingrese el nombre de la tabla a eliminar:");
    if (tableName) {
        axios.delete(`http://localhost:5000/tables/${tableName}`)
            .then(response => {
                alert(response.data.message);
                getRuleset();  // Actualiza las reglas después de eliminar
            })
            .catch(error => {
                console.error('Error al eliminar la tabla:', error);
            });
    }
}
