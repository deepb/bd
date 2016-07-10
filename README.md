bd Clone
==

¡Intenta escapar del fuego!

Hay una salida cerca, si puedes alcanzarla.
Si te quemas, reduces la posibilidad de alcanzar la salida.

INSTALACION
--

Instala _mysqld_

Ejecuta:

	mysql -u root -p

En la consola de mysql teclea:

	CREATE DATABASE BD;

	GRANT ALL ON BD.* TO 'BD'@'localhost' IDENTIFIED BY 'BD';

	CREATE TABLE Top (

		id INT NOT NULL AUTO_INCREMENT, 

		Nombre VARCHAR(5) NOT NULL, 

		Puntos INT NOT NULL, 

		TimeStamp DATETIME NOT NULL DEFAULT NOW(),

		PRIMARY KEY (id)

	);

	QUIT;


Ejecuta:

	python2 bd.py
	
