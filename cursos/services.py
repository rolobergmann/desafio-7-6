from .models import Profesor, Curso, Estudiante, Direccion, CursoProfesor

class CursoServices:
    def __init__(self):
        self.curso = Curso.objects.all()

    def crear_curso(self,codigo, nombre, version, profesor=None):
        try:
            if profesor:  # Only attempt to fetch profesor if it's not None
                profesor = Profesor.objects.get(pk=profesor.rut)
                curso = Curso.objects.create(
                    codigo=codigo,
                    nombre=nombre,
                    version=version,
                    profesor=profesor
                )
            else:
                    curso = Curso.objects.create(
                    codigo=codigo,
                    nombre=nombre,
                    version=version
                )   
            curso.save()
            return True  # Indicar éxito
        except Profesor.DoesNotExist:
            print(f"Profesor con ID {profesor.rut} no encontrado.")
            return False
        except Exception as e:  # Considerar un manejo de excepciones más específico
            print(f"Error creando curso: {e}")
            return False
        
    def crear_profesor(self, rut, nombre, apellido, activo,creado_por):
        try:
            profesor = Profesor.objects.create(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                activo=activo,
                creado_por=creado_por
            )
            profesor.save()
            return True  # Indicar éxito
        except Exception as e:
            print(f"Error creando profesor: {e}")
            return False

    def crear_estudiante(self, rut, nombre, apellido, fecha_nac, activo,creado_por):
        try:
            estudiante = Estudiante.objects.create(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                fecha_nac=fecha_nac,
                activo=activo,
                creado_por=creado_por
            )
            estudiante.save()
            return estudiante  # Return the created object
        except Exception as e:
            print(f"Error creando estudiante: {e}")
            return False


    def crear_direccion(self,calle, numero, depto, comuna, ciudad, region, estudiante_id):
        try:
            estudiante = Estudiante.objects.get(pk=estudiante_id)
            direccion = Direccion.objects.create(
                calle=calle,
                numero=numero,
                depto=depto,
                comuna=comuna,
                ciudad=ciudad,
                region=region,
                estudiante_id=estudiante
            )
            direccion.save()
            return True  # Indicar éxito
        except Estudiante.DoesNotExist:
            print(f"Estudiante con ID {estudiante_id} no encontrado.")
            return False
        except Exception as e:
            print(f"Error creando dirección: {e}")
            return False
        
    def obtener_estudiante(self,rut):
        try:
            estudiante = Estudiante.objects.get(rut=rut)
            direccion = estudiante.direccion  # Obtener la dirección del estudiante
            return {
                'rut': estudiante.rut,
                'nombre': estudiante.nombre,
                'apellido': estudiante.apellido,
                'fecha_nac': estudiante.fecha_nac.strftime('%Y-%m-%d'),
                'activo': estudiante.activo,
                'curso_id': estudiante.curso_id,
                'direccion': {
                    'calle': direccion.calle,
                    'numero': direccion.numero,
                    'depto': direccion.depto,
                    'comuna': direccion.comuna,
                    'ciudad': direccion.ciudad,
                    'region': direccion.region
                }
            }
        except Estudiante.DoesNotExist:
            return None

    def obtener_profesor(self,rut):
        try:
            profesor = Profesor.objects.get(rut=rut)
            return {
                'rut': profesor.rut,
                'nombre': profesor.nombre,
                'apellido': profesor.apellido,
                'activo': profesor.activo,
                'cursos': [curso.nombre for curso in profesor.cursos.all()]  # Obtiene la lista de nombres de cursos
            }
        except Profesor.DoesNotExist:
            return None

    def obtener_curso(self, codigo):
        try:
            curso = Curso.objects.get(codigo=codigo)
            profesores = curso.profesores.all()  # Get all related Profesor objects

            if profesores:  # Check if there are any Profesor objects
                profesor = profesores[0]  # Assume one profesor for simplicity
                nombre_profesor = f"{profesor.nombre} {profesor.apellido}"
            else:
                nombre_profesor = "Sin profesor asignado"

            estudiantes = [
                {
                    'rut': estudiante.rut,
                    'nombre': estudiante.nombre,
                    'apellido': estudiante.apellido
                } for estudiante in curso.estudiantes.all()
            ]

            return {
                'codigo': curso.codigo,
                'nombre': curso.nombre,
                'version': curso.version,
                'nombre_profesor': nombre_profesor,
                'estudiantes': estudiantes
            }
        except Curso.DoesNotExist:
            return None


    def agregar_profesor_a_curso(self, codigo_curso, rut_profesor):
        try:
            curso = Curso.objects.get(codigo=codigo_curso)
            profesor = Profesor.objects.get(pk=rut_profesor)
            curso.profesores.add(profesor)
            curso.save()
            return True  # Indicate success
        except Curso.DoesNotExist:
            print(f"Curso con codigo {codigo_curso} no encontrado.")
            return False
        except Profesor.DoesNotExist:
            print(f"Profesor con rut {rut_profesor} no encontrado.")
            return False
        except Exception as e:  # Consider more specific exception handling
            print(f"Error agregando profesor al curso: {e}")
            return False
    
    def agregar_estudiante_a_curso(self, codigo_curso, rut_estudiante):
        try:
            curso = Curso.objects.get(codigo=codigo_curso)
            estudiante = Estudiante.objects.get(pk=rut_estudiante)

            # Associate the student with the course
            estudiante.curso = curso
            estudiante.save()

            return True  # Indicate success
        except Curso.DoesNotExist:
            print(f"Curso con codigo {codigo_curso} no existe.")
            return False
        except Estudiante.DoesNotExist:
            print(f"Estudiante con rut {rut_estudiante} no existe")
            return False

    def imprimir_profesores(self):
        profesores = Profesor.objects.all()
        for profesor in profesores:
            print(f"Nombre: {profesor.nombre} Apellido: {profesor.apellido} Rut: {profesor.rut}")

    def imprimir_cursos(self):
        cursos = Curso.objects.all()
        for curso in cursos:
            profesores_lista = []  # Empty list to store profesor names
            if curso.profesores.all():
                for profesor in curso.profesores.all():
                    profesores_lista.append(f"{profesor.nombre} {profesor.apellido}")
                    profesores_str = ", ".join(profesores_lista)  # Create a comma-separated string of names
            else:
                profesores_str = "Sin profesor asignado"

            print(f"Codigo: {curso.codigo} Nombre: {curso.nombre} Profesor: {profesores_str} Version: {curso.version}")

            estudiante_lista = []  # Empty list to store student names
            estudiantes = curso.estudiantes.all()  # Use the related manager 'estudiantes'
            if estudiantes:  # Check if there are any students
                for estudiante in estudiantes:
                    estudiante_lista.append(f"{estudiante.nombre} {estudiante.apellido}")
                    estudiantes_str = ", ".join(estudiante_lista)  # Create a comma-separated string of names
            else:
                estudiantes_str = "Sin estudiante asignado"

            print(f"Estudiantes: {estudiantes_str}")


    def imprimir_estudiantes(self):
        estudiantes = Estudiante.objects.all()
        for estudiante in estudiantes:
            print(f"Nombre: {estudiante.nombre} Apellido: {estudiante.apellido} rut: {estudiante.rut}")