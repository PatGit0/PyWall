import unittest
from flask import Flask, jsonify
from pyWall.api import app  # Importa tu aplicación Flask

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Configuración antes de cada prueba
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # Limpieza después de cada prueba
        pass

    def test_get_tables(self):
        # Prueba para el endpoint de listar tablas
        response = self.app.get('/tables')
        self.assertEqual(response.status_code, 200)
        self.assertIn('filter', response.json['message'])  # Verifica que 'filter' esté en la respuesta

    def test_create_table(self):
        # Prueba para el endpoint de crear una tabla
        response = self.app.post('/new_table', json={'name': 'test_table'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Tabla \'test_table\' añadida', response.json['message'])

    def test_create_chain(self):
        # Prueba para el endpoint de crear una cadena en una tabla
        response = self.app.post('/tables/test_table/chains', json={
            'name': 'test_chain',
            'type': 'filter',
            'hook': 'input',
            'priority': '0',
            'policy': 'drop',
            'comment': 'Cadena de prueba'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Cadena \'test_chain\' añadida', response.json['message'])

    def test_error_on_missing_parameters(self):
        # Prueba para verificar el manejo de errores
        response = self.app.post('/tables/test_table/chains', json={
            'name': 'test_chain',
            'type': 'filter'
            # Falta 'hook' y 'priority'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Faltan parámetros necesarios para crear la cadena', response.json['error'])

if __name__ == '__main__':
    unittest.main()
