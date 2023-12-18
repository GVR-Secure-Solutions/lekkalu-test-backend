import requests
import unittest
import json
import uuid
from datetime import datetime


class LoanTests(unittest.TestCase):
    username1 = "szatma"
    password1 = "123456789"
    token1 = ""
    username2 = "QAuser"
    password2 = "123456789"
    token2 = ""
    global loan_id

    @classmethod
    def setUpClass(cls) -> None:
        URL = "https://api.finuncle.com/token/"
        response = requests.post(URL, json={"username": cls.username1,
                                            "password": cls.password1})
        response_body = json.loads(response.text)
        cls.token1 = response_body["access"]

        response = requests.post(URL, json={"username": cls.username2,
                                            "password": cls.password2})
        response_body = json.loads(response.text)
        cls.token2 = response_body["access"]

    def test_get_loan_returns_200(self):
        URL = "https://api.finuncle.com/api/v1/loans/"
        headers = {
            'Authorization': f'Bearer {self.token1}',
        }
        response = requests.get(URL, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_post_loan_returns_201(self):
        global loan_id
        URL = "https://api.finuncle.com/api/v1/loans/"
        headers = {
            'Authorization': f'Bearer {self.token1}',
        }
        data = {
            "name": f"Test loan {uuid.uuid4()}",
            "balance":5,
            "principal": 1,
            "tenure": 1,
            "closure_charges": 10,
            "emi":3,
            "interest_rate":5,
            "emi_day": 1,
            "disbursement_date": datetime.today().strftime('%Y-%m-%d')
        }
        response = requests.post(URL, headers=headers, data=data)
        response_text = json.loads(response.text)
        loan_id = response_text["data"]["id"]
        print(loan_id)
        self.assertEqual(response.status_code, 201)


    def test_unauthorized_loan_get_by_id_should_return_401(self):
        global loan_id
        URL = "http://api.finuncle.com/api/v1/loans/"+str(loan_id)
        print(URL)
        headers = {
            'Authorization': f'Bearer {self.token2}',
        }
        response = requests.get(URL, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_loan_id_should_not_be_in_response(self):
        global loan_id
        is_another_accounts_loan_id_in_response = False
        URL = "http://api.finuncle.com/api/v1/loans/"
        headers = {
            'Authorization': f'Bearer {self.token2}',
        }
        response = requests.get(URL, headers=headers)
        response_text = json.loads(response.text)
        for loan in response_text:
            if loan_id == loan["id"]:
                is_another_accounts_loan_id_in_response = True
        #loan_id = response_text["data"]["id"]
        self.assertEqual(is_another_accounts_loan_id_in_response, False)

    def test_get_loan_by_id_without_authorization(self):
        URL = "http://api.finuncle.com/api/v1/loans/1"
        response = requests.get(URL)
        self.assertEqual(response.status_code, 401)

    def test_post_loan_by_id_without_authorization(self):
        URL = "http://api.finuncle.com/api/v1/loans/1"
        response = requests.post(URL)
        self.assertEqual(response.status_code, 401)

    @classmethod
    def tearDownClass(cls) -> None:
        global loan_id
        URL = f"https://api.finuncle.com/api/v1/loans/{loan_id}"
        headers = {
            'Authorization': f'Bearer {cls.token1}',
        }
        requests.delete(URL, headers=headers)

if __name__ == "__main__":
    unittest.main()
