# Iterative Assessed Activity XBlock

## Presentación

Este XBlock de desarrollo iterativo asesorado (IAA por sus siglas en inglés), permite construir actividades en que se pueda responder varias veces la misma pregunta a lo largo de un curso, recibiendo feedback personalizado para cada respuesta.

## Instalación

Para instalar en Devstack (o cualquier instancia de edX):

1. Instalar tanto en el LMS como en Studio:

```bash
$ pip install -e /path/to/iaaxblock
```

2. Aplicar las migraciones (desde el LMS):

```bash
$ python manage.py lms migrate iaaxblock
```

3. Agregar a los cursos mediante el nombre 'iaaxblock'.

## Licencia

Desarrollado para el CMMEdu.