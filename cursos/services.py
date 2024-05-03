from .models import Profesor, Curso, Estudiante, Direccion, CursoProfesor

class CursoServices:
    def __init__(self):
        self.curso = Curso.objects.all()

    def crear_curso(codigo, nombre, version, profesor_id):
        try:
            profesor = Profesor.objects.get(pk=profesor_id)
            curso = Curso.objects.create(
                codigo=codigo,
                nombre=nombre,
                version=version,
                profesor=profesor
            )
            curso.save()
            return True  # Indicar éxito
        except Profesor.DoesNotExist:
            print(f"Profesor con ID {profesor_id} no encontrado.")
            return False
        except Exception as e:  # Considerar un manejo de excepciones más específico
            print(f"Error creando curso: {e}")
            return False
        
    @staticmethod  # Marcar el método como estático
    def crear_profesor(rut, nombre, apellido, activo):
        try:
            profesor = Profesor.objects.create(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                activo=activo
            )
            profesor.save()
            return True  # Indicar éxito
        except Exception as e:
            print(f"Error creando profesor: {e}")
            return False

    def crear_estudiante(rut, nombre, apellido, fecha_nac, activo, curso_id):
        try:
            curso = Curso.objects.get(pk=curso_id)
            estudiante = Estudiante.objects.create(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                fecha_nac=fecha_nac,
                activo=activo,
                curso=curso
            )
            estudiante.save()
            return True  # Indicar éxito
        except Curso.DoesNotExist:
            print(f"Curso con ID {curso_id} no encontrado.")
            return False
        except Exception as e:
            print(f"Error creando estudiante: {e}")
            return False

    def crear_direccion(calle, numero, depto, comuna, ciudad, region, estudiante_id):
        try:
            estudiante = Estudiante.objects.get(pk=estudiante_id)
            direccion = Direccion.objects.create(
                calle=calle,
                numero=numero,
                depto=depto,
                comuna=comuna,
                ciudad=ciudad,
                region=region,
                estudiante=estudiante
            )
            direccion.save()
            return True  # Indicar éxito
        except Estudiante.DoesNotExist:
            print(f"Estudiante con ID {estudiante_id} no encontrado.")
            return False
        except Exception as e:
            print(f"Error creando dirección: {e}")
            return False

    def obtener_estudiante(rut):
        try:
            estudiante = Estudiante.objects.get(rut=rut)
            direccion = estudiante.direccion  # Obtiene la dirección asociada al estudiante
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

    def obtener_profesor(rut):
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

    def obtener_curso(codigo):
        try:
            curso = Curso.objects.get(codigo=codigo)
            profesor = curso.profesor
            return {
                'codigo': curso.codigo,
                'nombre': curso.nombre,
                'version': curso.version,
                'nombre_profesor': f"{profesor.nombre} {profesor.apellido}",
                'estudiantes': [
                    {
                        'rut': estudiante.rut,
                        'nombre': estudiante.nombre,
                        'apellido': estudiante.apellido
                    } for estudiante in curso.estudiantes.all()
                ]
            }
        except Curso.DoesNotExist:
            return None

    def agregar_profesor_a_curso(codigo_curso, rut_profesor):
        try:
            curso = Curso.objects.get(codigo=codigo_curso)
            profesor = Profesor.objects.get(rut=rut_profesor)
            curso.profesor = profesor
            curso.save()
            return True  # Asignación exitosa
        except (Curso.DoesNotExist, Profesor.DoesNotExist):
            print(f"Curso con código {codigo_curso} o profesor con RUT {rut_profesor} no encontrado.")
            return False
        except Exception as e:
            print(f"Error agregando profesor a curso: {e}")
            return False
