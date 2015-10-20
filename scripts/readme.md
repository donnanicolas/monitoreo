# Scripts para KILL and RENICE

Estos dos comandos tiene problemas con los permisos

* **renice**: Solo puede reducir la prioridad de los procesos sin ser root
* **kill**: Solo puede matar procesos que son del usuario

Una posible solución es la creación de scripts que tiene algún tipo de seguridad (contraseña por ejemplo) y permitir que se corran como **root** sin password. Esto se puede hacer editando **/etc/sudoers** y agregar:
```
<server-user> ALL= NOPASSWD:/path/to/scripts/script-name.sh
```
Luego se correran en el servidorcon **sudo**

La contraseña tiene que estar hasheada para evitar que se pueda leer simplemente. Para evitar cambios en los scripts se deben setear los permisos para evitar escritura (máximo 555). Solo se debería poder escribir siendo root

Los scripts [sudo_renice](sudo_renice.sh) y [sudo_kill](sudo_kill.sh) son ejemplos de esta solución. El password en los mismos es **testpasswd**

## sudo_renice

El script recibe 3 argumentos : **pass**, **priority** and **pid**

### Ejemplo
```
sudo /path/to/script/sudo_renice.sh passwd -10 7300
```

Si la contraseña es correcta entonces cambia la prioridad.

## sudo_kill

El script recibe 2 argumentos: **pass** and **pid**

### Example
```
sudo /path/to/script/sudo_kill.sh passwd 7300
```

Este script también checkea la contraseña, pero además comprueba que el proceso no pertenezca a **root**
