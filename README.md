# Monit
Esta aplicación es un trabajo para la materia Monitoreo y Gestión de Redes de la carrera de Ingeniería en Infomática de la Universidad de Mendoza.
Bajo ningún concepto se debe utilizar esta aplicación en producción, ya que puede generar grandes problemas en un servidor al matar procesos, repriorizarlos o crear nuevos.

# Instalación
Esta aplicación esta hecha en Flask (python)
Se debe tener instalado python 2.7.x

Además se debe contar con la librería Flask y psutil

```bash
> pip install Flask
> pip install psutil
```

Para correr el servidor

```bash
> python moniy.py
```

#Aplicación
El sistema es una API RESTful que trabaja con formato JSON.
Presenta funcionalidades para controlar los procesos corriendo en el sistema.
El sistema está preparado para sistema UNIX. Es posible ampliar la funcionalidad a Windows sin mayores inconvenientes.

# Rutas
La aplicación cuenta con 5 rutas

## GET /ps
La misma devuelve todos los procesos corriendo en el sistema. Los campos devueltos son los siguientes:

Nombre | Explicación
------------ | ------------- | -------------
cmdline | Comando de la linea de comando con que fue llamado
connections | Sockets abiertos por este procesos
cpu_percent | Porcentaje de procesamiento ocupado
cpu_times |  Arreglo con [segundos en espacio de usuario, segundos en espacio de sistema]
create_time | Tiempo de creación
cwd | Directorio absoluto de trabajo
exe | El ejecutable de este proceso
gids | Arreglo con los valores de los ids de grupo para **real**, **effective** and **saved**
memory_info | Arreglo con RSS (Resident Set Size) y VMS (Virtual Memory Size) en bytes. Cambia según OS ver psutil
memory_info_ex | Ver [psutil#memory_info_ex](http://pythonhosted.org/psutil/#psutil.Process.memory_info_ex)
memory_maps | Mapas de memoria
memory_percent | Porcentaje de la memoria fisica utilizada, en relación al RSS
name | Nombre del proceso
nice | Prioridad
num_ctx_switches | Numero de cambio de contexto
num_fds | Número de file descriptors
num_threads | Número de hilos
open_files | Número de archivos abiertos, y su file descriptor. En windows el fd siempre es -1
pid | El id del proceso
ppid | El id del proceso padre
status | El estado del proceso como un string
terminal | El terminal asociado con este proceso, si hay
threads | Los threads the proceso
uids | Arreglo con los valores de los ids de grupo para **real**, **effective** and **saved**
username | El usuario dueño de este proceso

Dependiendo de la plataforma puede aparecer algunos campos más, para más información dirigirse a [psutil#Process](http://pythonhosted.org/psutil/#process-class)

## GET /users
Devuelve los usuarios que están corriendo procesos en el sistema.

Nombre | Explicación
------------ | -------------
username | Nombre del usuario
running | Cantidad de procesos que está corriendo

## GET /users/:username/tasks
Devuelve la información sobre los procesos que está corriendo el usuario con el nombre :username

Para más información sobre los campos vea [GET /ps](#GET-/ps)

## POST /ps
Esta ruta corre el comando que se pasa como parametro *cmd*. Es una funcionalidad peligrosa ya que se puede correr virtualmente cualquier comando.

### Parametros

Nombre | Explicación
------------ | -------------
cmd | El comando a correr
args | Arreglo con los argumentos

#### Ejemplo:

```json
{
    "cmd": "echo",
    "args": ["hola"]
}
```
Como no sabemos de antemano el tiempo que va a llevar el proceso y no podemos utilizar el stream debido a que no estamos usando streaming, solo se devuelve el *pid*

## DELETE /ps
Esta ruta envia un *SIGKILL* al proceso bajo con el *pid* enviado como argumento.
Para evitar problemas si el *pid* es el mismo proceso o es padre del proceso del servidor no se puede matar.

### Parametros

Nombre | Explicación
------------ | -------------
pid | Id del proceso

#### Ejemplo:

```json
{
    "pid": "8802"
}
```


## PATCH /ps
Esta ruta simplemente corre el comando **renice**.

### Parametros

Nombre | Explicación
------------ | -------------
pid | Id del proceso
priority | Nueva prioridad. Valor en -20 y 20

#### Ejemplo:

```json
{
    "pid": "8802",
    "priority": 10
}
```

El comando **renice** requiere permisos especiales, por lo tanto solo podrá ser utilizado si el proceso del servidor tiene permisos para hacerlo.
