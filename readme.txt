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
			* Todos los permisos (no todos implementados aún)
	* Grupo entidad:
		* Usuario: todas las entidades registradas
			* Permisos para registrar deportistas (no implementado aún)
			* Permisos para registrar, consultar, modificar y eliminar escenarios (100%)
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

* Permisos para gestión de información:
	* noticias:
		* Registra cualquier entidad (100%)
		* Consulta grupo entidad, coldeportes o invitado (100%)
		* Edita entidad que registra o coldeportes (100%)
		* Eliminar entidad que registra o coldeportes (100%)
	* Entidades:
		* Registra coldeportes (100%)
		* Consulta coldeportes (100%) y entidad a sí misma (no implementado)
		* Edita coldepotes (100%) y entidad a sí misma (no implementado aún)
		* Elimina coldeportes
	* Escenarios:
		* Registra entidad (100%) y coldeportes (no implementado)
		* Consulta entidad (100%) y coldeportes (no implementado)
		* Edita entidad (100%) y coldeportes (no implementado)
		* Elimina entidad (100%) y coldeportes (no implementado)
	* Deportistas
		* Registra entidad y coldeportes (no implementado)
		* Consulta entidad y coldeportes (no implementado)
		* Edita entidad y coldeportes (no implementado)
		* Elimina entidad y coldeportes (no implementado)

* Para tener en cuenta

	* Se debe tener un usuario creado en la bd del grupo coldeportes
	* Los usuarios para las entidades se crean al momento de registrarlas y se les asigna el grupo entidad
	* La gestión de la información mencionada en el ítem inmediatamente anterior deben ser realizados con el logueo del usuario correspondiente

* Librerías necesarias

	* Pillow: gestión de imágeges
	* Datatimepicker: calendario gráfico
	* Django-bootstrap3: gestional el css para el datatimepicker