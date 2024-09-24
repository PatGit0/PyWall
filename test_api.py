import requests
import unittest
from flask import jsonify
ENDPOINT = "http://localhost:5000"

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.table_name = "pre_test_table"
        self.empty_table = {self.table_name: {"chains": {}, "family": "inet"}}
        self.ruleset = requests.get(f"{ENDPOINT}/ruleset")
        self.test_chain = {
            "name": "chain_name",
            "type": "filter",
            "hook": "input",
            "priority": "0",
            "policy": "accept",
            "comment": "Test chain"
        }
        requests.post(ENDPOINT + "/tables", json={"name": self.table_name})

    def tearDown(self):
        requests.delete(f"{ENDPOINT}/tables/{self.table_name}")

    def test_create_table(self):
        payload = {"name": "new_test_table"}
        response = requests.post(f"{ENDPOINT}/tables, json=payload")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": f"Tabla '{payload['name']}' añadida"})

    def test_get_tables(self):
        response = requests.get(f"{ENDPOINT}/tables")
        self.assertEqual(response.status_code, 200)
        tables = response.json()['tables']
        self.assertIn(f'table inet {self.table_name}', tables)

    def test_delete_table(self):
        response = requests.delete(f"{ENDPOINT}/tables/{self.table_name}")
        self.assertEqual(response.status_code, 204)

        response = requests.get(f"{ENDPOINT}/tables")
        self.assertEqual(response.status_code, 200)
        tables = response.json()['tables']
        self.assertNotIn(self.table_name, tables)

    def test_flush_table(self):
        response = requests.post(f"{ENDPOINT}/tables/{self.table_name}/flush")
        self.assertEquals(response.status_code, 204)

        response = requests.get(f"{ENDPOINT}/ruleset")
        self.assertEqual(response.status_code, 200)
        tableValue = response.json()['tables'][self.table_name]
        self.assertEqual(tableValue, self.empty_table[self.table_name])

    def test_create_chain(self):

        response = requests.post(f"{ENDPOINT}/tables/{self.table_name}/chains",json=(self.test_chain),headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = requests.get(f"{ENDPOINT}/ruleset")
        self.assertEqual(response.status_code, 200)
        chains = response.json()['tables'][self.table_name]['chains']
        self.assertIn(self.test_chain, chains)

    def test_delete_chain(self):

        response = requests.post(f"{ENDPOINT}/tables/{self.table_name}/chains", json=(self.test_chain),
                                 headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        response = requests.delete(f"{ENDPOINT}/tables/{self.table_name}/chains/{self.test_chain['name']}")
        self.assertEqual(response.status_code,204)
        response = requests.get(f"{ENDPOINT}/ruleset")
        self.assertEqual(response.status_code, 200)
        chains = response.json()['tables'][self.table_name]['chains']
        self.assertEqual(chains, {})

if __name__ == '__main__':
    unittest.main()
