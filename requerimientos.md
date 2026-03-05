# Sistema de Evaluación APGAR para Neonatología

## Descripción

Este software es una aplicación web que permite calcular el puntaje del Test APGAR para evaluar el estado de salud de un recién nacido.  
El sistema recibe los cinco parámetros del test, calcula el puntaje total y muestra una clasificación del estado del bebé.

La aplicación también guarda cada evaluación en una base de datos para mantener un registro.

---

## Stack de Tecnologías

El sistema fue desarrollado utilizando:

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite

---

## Requerimientos Funcionales

- Ingresar el nombre del recién nacido.
- Registrar los cinco parámetros del Test APGAR.
- Calcular automáticamente el puntaje total.
- Mostrar el estado del recién nacido según el puntaje.
- Guardar los resultados en una base de datos.

---

## Requerimientos No Funcionales

- El sistema debe ejecutarse en un navegador web.
- Debe funcionar en un servidor local con Flask.
- Debe validar que los valores estén entre 0 y 2.
- Debe almacenar los registros en SQLite.

---

## Funcionalidades Futuras

- Generar reportes en PDF.
- Mostrar historial de evaluaciones.
- Agregar autenticación de usuarios.
- Incluir estadísticas de resultados.