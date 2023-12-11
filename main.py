import requests
import unittest


class LoanTests(unittest.TestCase):
    username = "szatma"
    password = "123456789"

    def setUp(self) -> None:
        URL = "http://api.finuncle.com/api/v1/loans/"
        response = requests.post(URL, auth=(self.username, self.password))

    def test_get_loan_transactions_returns_200(self):
        URL = "https://api.finuncle.com/api/v1/loan_transactions/"
        response = requests.get(URL, auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)

    def test_get_loan_by_id_by_other_user_should_return_401(self):
        URL = "http://api.finuncle.com/api/v1/loans/1"
        response = requests.get(URL, auth=(self.username, self.password))
        self.assertEqual(response.status_code, 401)

    def test_post_loan_by_id_by_other_user_should_return_401(self):
        URL = "http://api.finuncle.com/api/v1/loans/1"
        response = requests.post(URL, auth=(self.username, self.password))
        self.assertEqual(response.status_code, 401)

    def test_get_loan_by_id_without_authorization(self):
        URL = "http://api.finuncle.com/api/v1/loans/1"
        response = requests.get(URL)
        self.assertEqual(response.status_code, 401)

    def test_post_loan_by_id_without_authorization(self):
        URL = "http://api.finuncle.com/api/v1/loans/1"
        response = requests.post(URL)
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
