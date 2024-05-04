import unittest
from django.test import TestCase
from .services import CursoServices
from .models import Curso, Profesor, Estudiante, Direccion, CursoProfesor

class CursoServicesTest(TestCase):

    def test_crear_curso_sin_profesor(self):
        curso_service = CursoServices()
        resultado = curso_service.crear_curso("MAT101", "Matemáticas", 1)
        self.assertTrue(resultado)

    def test_crear_curso_con_profesor(self):
        profesor_service = CursoServices()
        resultado_profesor = profesor_service.crear_profesor("44444444-1", "Juan", "Perez", True, "admin")
        self.assertTrue(resultado_profesor)

        curso_service = CursoServices()
        resultado_curso = curso_service.crear_curso("FIS101", "Física", 1, profesor_service.curso.first())
        self.assertTrue(resultado_curso)

    def test_crear_profesor(self):
        curso_service = CursoServices()
        resultado = curso_service.crear_profesor("55555555-2", "Pedro", "Gómez", False, "admin")
        self.assertTrue(resultado)

    def test_crear_estudiante(self):
        curso_service = CursoServices()
        resultado = curso_service.crear_estudiante("66666666-3", "María", "López", "2000-01-01", True, "admin")
        self.assertTrue(resultado)

    def test_crear_direccion(self):
        curso_service = CursoServices()
        resultado_estudiante = curso_service.crear_estudiante("77777777-4", "Ana", "Silva", "2001-02-02", True, "admin")
        self.assertTrue(resultado_estudiante)

        resultado_direccion = curso_service.crear_direccion("Los Alamos", 123, "Dpto. 4", "Melipilla", "Melipilla", "RM", resultado_estudiante.pk)
        self.assertTrue(resultado_direccion)

    def test_obtener_estudiante(self):
        curso_service = CursoServices()
        resultado_crear_estudiante = curso_service.crear_estudiante("88888888-5", "David", "Muñoz", "2002-03-03", True, "admin")
        self.assertTrue(resultado_crear_estudiante)

        resultado_direccion = curso_service.crear_direccion("Los Alamos", 123, "Dpto. 4", "Melipilla", "Melipilla", "RM", resultado_crear_estudiante.pk)  # Associate with the student
        self.assertTrue(resultado_direccion)

        resultado_obtener_estudiante = curso_service.obtener_estudiante("88888888-5")
        self.assertIsNotNone(resultado_obtener_estudiante)
        self.assertEqual(resultado_obtener_estudiante["rut"], "88888888-5")
        self.assertEqual(resultado_obtener_estudiante["nombre"], "David")
        self.assertEqual(resultado_obtener_estudiante["apellido"], "Muñoz")

    def test_obtener_profesor(self):
        curso_service = CursoServices()
        resultado_crear_profesor = curso_service.crear_profesor("99999999-6", "Sofia", "Martínez", True, "admin")
        self.assertTrue(resultado_crear_profesor)

        resultado_obtener_profesor = curso_service.obtener_profesor("99999999-6")
        self.assertIsNotNone(resultado_obtener_profesor)
        self.assertEqual(resultado_obtener_profesor["rut"], "99999999-6")
        self.assertEqual(resultado_obtener_profesor["nombre"], "Sofia")
        self.assertEqual(resultado_obtener_profesor["apellido"], "Martínez")

    def test_obtener_curso(self):
        curso_service = CursoServices()
        resultado_crear_curso = curso_service.crear_curso("QUIM101", "Química", 1)
        self.assertTrue(resultado_crear_curso)

        resultado_obtener_curso = curso_service.obtener_curso("QUIM101")
        self.assertIsNotNone(resultado_obtener_curso)
        self.assertEqual(resultado_obtener_curso["codigo"], "QUIM101")
        self.assertEqual(resultado_obtener_curso["nombre"], "Química")
