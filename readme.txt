El proyecto SIDeporte se encuentra realizado en Django y Python3

--version Django: 1.8.4
--version Python: 3.4

************************************************************************

CONSIDERACIONES GENERALES Y AVANCE DEL PROYECTO

* El logueo de usuarios está completamente funcional
* El menú de opciones del sistema cambia en función del usuario que se encuentra logueado
* Tipos de usuario:
	* Grupo coldeportes:
		* Usuario: coldeportes
			* Todos los permisos
	* Grupo entidad:
		* Usuario: todas las entidades registradas
			* Permisos para registrar deportistas y escenarios (no implementados aún)
			* Permisos para modificar la información de sí mismo (no implementado aún)
	* Grupo invitado:
		* Usuario: usuarios que no hayan iniciado sesión
			* Puede ver las noticias
			* Puede ver la información general de Coldeportes
* Las páginas con información "sensible" pueden ser accesidas si se conoce el código del objeto el cual es 
PK en la base de datos, y que es usado mediante URL para un acceso único (Sin embargo, no se puede hacer ningún 
tipo de modificación. Ejemplo: se puede acceder a la información de una entidad con todos sus detalles mas no 
modificarlos). Se espera implementar un error 403 (prohibido) e impedir el acceso si no está logueado con 
el usuario al que accede por información.
* CRUD gestionado:
	* Noticias:
		* Registro
		* Lectura
		* Actualización
		* Eliminación (borrado lógico)
	* Entidades: 
		* Registro (formulario casi completo, no funcional)
		* Lectura
* Reportes:
	* Gráficos: en plantilla
	* Tablas: en plantilla
* Geolocalización: Se muestra el mapa sin geolocalización
* Interfaces: responsivas
