![Gz8I3WjW4AAcjE2](https://github.com/user-attachments/assets/a2de167a-816c-4931-a483-f1cce591707d)

**[Español](#español) | [English](#english)**

## Español

### mos-git-sync

`mos-git-sync` es un script en Python diseñado para automatizar la sincronización de ramas (incluidas las que no son `main`) desde repositorios originales (upstream) hacia tus forks, así como mantener copias locales actualizadas de tus repositorios de trabajo. El "mos" en `mos-git-sync` significa **MetsuOS**, un proyecto centrado en herramientas y entornos para computación retro. Este script es especialmente útil para gestionar múltiples repositorios Git, asegurando que los forks estén sincronizados con sus originales y que las copias locales de desarrollo estén al día.

Este proyecto está licenciado bajo la **Licencia Pública General de GNU Affero v3.0 (AGPL-3.0)**, garantizando que el código fuente esté disponible libremente y que cualquier trabajo derivado también sea de código abierto.

#### Características

- **Sincronización de Forks**: Sincroniza automáticamente las ramas especificadas desde un repositorio original hacia tu fork.
- **Copias Locales de Desarrollo**: Mantiene clones locales actualizados de tus repositorios para desarrollo.
- **Configurable**: Utiliza un archivo de configuración JSON para definir repositorios, sus URLs de origen y fork, y las ramas a sincronizar.
- **Estructura de Dos Carpetas**: Gestiona repositorios en dos carpetas:
  - `sync`: Para sincronizar forks con repositorios originales.
  - `dev`: Para mantener copias locales de desarrollo actualizadas desde el fork.
- **Salida Verbosa**: Proporciona información clara y concisa sobre cada acción (clonar, obtener, cambiar rama, fusionar, subir) para cada repositorio y rama.
- **Soporte para Repositorios No-Fork**: Omite la sincronización con upstream para repositorios donde las URLs de origen y fork son iguales, actualizando solo la carpeta `dev`.
- **Gestión de Claves SSH**: Utiliza `ssh-agent` para cargar claves SSH automáticamente, solicitando la contraseña solo una vez por ejecución.

#### Requisitos

- **Python**: Versión 3.6 o superior.
- **Git**: Instalado y configurado con acceso SSH a los repositorios (por ejemplo, claves SSH para GitHub).
- **SSH-Agent**: Requiere `ssh-agent` y `ssh-add` para gestionar claves SSH (incluidos en la mayoría de los sistemas Linux y macOS, o en Windows con Git Bash).
- **Sistema Operativo**: Compatible con Linux, macOS o Windows (con Git Bash o similar).

#### Instalación

1. **Clonar el Repositorio**:
   ```bash
   git clone git@github.com:metsuke/mos-git-sync.git
   cd mos-git-sync
   ```

2. **Verificar Python, Git y SSH**:
   - Verifica Python: `python3 --version`
   - Verifica Git: `git --version`
   - Configura claves SSH para GitHub u otros hosts de Git según sea necesario.
   - Asegúrate de que `ssh-agent` y `ssh-add` estén disponibles: `ssh-agent -v` y `ssh-add -l`.

3. **Colocar el Archivo de Configuración**:
   - Crea un archivo llamado `mos-git-sync.json` en el mismo directorio que `mos-git-sync.py` (por ejemplo, `/Volumes/WDBOOK_2411/MetsuOS/system/tools/`).
   - Consulta la sección [Configuración](#configuración) para más detalles.

#### Configuración

El script requiere un archivo de configuración JSON llamado `mos-git-sync.json`, ubicado en el mismo directorio que `mos-git-sync.py`. Este archivo especifica el directorio de gestión para los repositorios y la lista de repositorios a procesar.

##### Ejemplo de `mos-git-sync.json`
```json
{
  "management_dir": "/Volumes/WDBOOK_2411/MetsuOS/data/dev-git",
  "repositories": [
    {
      "name": "zx-game-maker-metsuos",
      "url-origen": "git@github.com:rtorralba/zx-game-maker.git",
      "url-fork": "git@github.com:metsuke/zx-game-maker-metsuos.git",
      "branches": ["main", "preview"]
    },
    {
      "name": "mos-retrotools-launcher",
      "url-origen": "git@github.com:metsuke/mos-retrotools-launcher.git",
      "url-fork": "git@github.com:metsuke/mos-retrotools-launcher.git",
      "branches": ["main"]
    }
  ]
}
```

- **`management_dir`**: El directorio raíz donde se almacenan los repositorios. Se crearán subdirectorios `sync` y `dev`.
- **`repositories`**: Una lista de repositorios, cada uno con:
  - `name`: Un identificador único para el repositorio.
  - `url-origen`: La URL del repositorio original (upstream).
  - `url-fork`: La URL de tu fork (o la misma que `url-origen` para repositorios no-fork).
  - `branches`: Lista de ramas a sincronizar.

Para repositorios no-fork (donde `url-origen` es igual a `url-fork`), el script omite la fase `sync` y solo actualiza la carpeta `dev`.

#### Uso

Ejecuta el script desde cualquier directorio, especificando la ruta completa a `mos-git-sync.py`. El script localizará automáticamente `mos-git-sync.json` en su propio directorio.

##### Sincronizar Todos los Repositorios
```bash
python /path/to/mos-git-sync.py
```
Esto procesa todos los repositorios listados en `mos-git-sync.json`. La primera vez, se pedirá la contraseña de la clave SSH, que se almacenará en memoria para el resto de la ejecución.

##### Sincronizar un Repositorio Específico
```bash
python /path/to/mos-git-sync.py --repo <nombre-repositorio>
```
Sustituye `<nombre-repositorio>` por el `name` del JSON (por ejemplo, `zx-game-maker-metsuos`).

##### Ejemplo de Salida
```plaintext
Iniciando ssh-agent...
Agregando clave SSH...
Cargando configuración desde: /Volumes/WDBOOK_2411/MetsuOS/system/tools/mos-git-sync.json
Asegurando que el directorio de gestión existe: /Volumes/WDBOOK_2411/MetsuOS/data/dev-git
Asegurando que el directorio sync existe: /Volumes/WDBOOK_2411/MetsuOS/data/dev-git/sync
Asegurando que el directorio dev existe: /Volumes/WDBOOK_2411/MetsuOS/data/dev-git/dev

Procesando repositorio: zx-game-maker-metsuos
Iniciando fase sync para el repositorio: zx-game-maker-metsuos
Clonando fork en la carpeta sync: /Volumes/WDBOOK_2411/MetsuOS/data/dev-git/sync/zx-game-maker-metsuos
...
```

#### Estructura de Directorios