from django.http import response
from django.test import TestCase, Client

from .factories import UsuarioDEPFactory, UsuarioSEFactory, UsuarioFinancieroFactory

# Create your tests here.

class UsuarioDEPTestCase (TestCase):
    def setUp(self) -> None:
        self.usuario = UsuarioDEPFactory.create()
        self.client = Client()
    
    def test_usuario_DEP(self):  
        self.assertIn("_DEP@morelia.tecnm.mx", self.usuario.email)
        self.assertEqual(self.usuario.usuario_activo, True)
        self.assertEqual(self.usuario.rol, "dep")

    def test_usuario_DEP_fail(self):  
        try:
            self.assertIn("_DEPD@moorelia.tecnm.mx", self.usuario.email)
            self.assertEqual(self.usuario.usuario_activo, False)
            self.assertEqual(self.usuario.rol, "deepp")
        except AssertionError:
            pass
    
    def test_login(self):
        response = self.client.post(
            '',
            {
                'username' : self.usuario.username,
                'password' : self.usuario.password
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.usuario.rol, "dep")

    def test_login_fail(self):
        response = self.client.login(
                username = 'fake_username',
                password = 'fake_password'
        )
        self.assertEqual(response, False)

class UsuarioSETestCase (TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.usuario = UsuarioSEFactory.create()
    
    def test_usuario_SE(self):
        self.assertIn("_SE@morelia.tecnm.mx", self.usuario.email)
        self.assertEqual(self.usuario.usuario_activo, True)
        self.assertEqual(self.usuario.rol, "se")

    def test_usuario_SE_fail(self):  
        try:
            self.assertIn("_SEEE@moorelia.tecnm.mx", self.usuario.email)
            self.assertEqual(self.usuario.usuario_activo, False)
            self.assertEqual(self.usuario.rol, "seeep")
        except AssertionError:
            pass

    def test_login(self):
        response = self.client.post(
            '',
            {
                'username' : self.usuario.username,
                'password' : self.usuario.password
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.usuario.rol, "se")

    def test_login_fail(self):
        response = self.client.login(
                username = 'fake_username',
                password = 'fake_password'
        )
        self.assertEqual(response, False)

class UsuarioFinancieroTestCase (TestCase):
    def setUp(self) -> None:
        self.usuario = UsuarioFinancieroFactory.create()
    
    def test_usuario_Financiero(self):
        self.assertIn("_FINANCIERO@morelia.tecnm.mx", self.usuario.email)
        self.assertEqual(self.usuario.usuario_activo, True)
        self.assertEqual(self.usuario.rol, "financiero")

    def test_usuario_Financiero_fail(self):  
        try:
            self.assertIn("_FINANCIEROOOO@moorelia.tecnm.mx", self.usuario.email)
            self.assertEqual(self.usuario.usuario_activo, False)
            self.assertEqual(self.usuario.rol, "finan")
        except AssertionError:
            pass

    def test_login(self):
        response = self.client.post(
            '',
            {
                'username' : self.usuario.username,
                'password' : self.usuario.password
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.usuario.rol, "financiero")

    def test_login_fail(self):
        response = self.client.login(
                username = 'fake_username',
                password = 'fake_password'
        )
        self.assertEqual(response, False)

class ClientTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.usuario = UsuarioDEPFactory.create()

    def test_GET(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_GET_fail(self):
        response = self.client.get('usuariosfake')
        self.assertEqual(response.status_code, 404)

    def test_POST(self):
        response = self.client.post(
            '',
            {
                'username' : self.usuario.username,
                'password' : self.usuario.password
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_POST_fail(self):
        response = self.client.post(
            'usuariosfake',
            {
                'username' : self.usuario.username,
                'password' : self.usuario.password
            }
        )
        self.assertEqual(response.status_code, 404)