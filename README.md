![Gz8I3WjW4AAcjE2](https://github.com/user-attachments/assets/a2de167a-816c-4931-a483-f1cce591707d)

# mos-git-sync

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

#### Requisitos

- **Python**: Versión 3.6 o superior.
- **Git**: Instalado y configurado con acceso SSH a los repositorios (por ejemplo, claves SSH para GitHub).
- **Sistema Operativo**: Compatible con Linux, macOS o Windows (con Git Bash o similar).

#### Instalación

1. **Clonar el Repositorio**:
   ```bash
   git clone git@github.com:metsuke/mos-git-sync.git
   cd mos-git-sync
   ```

2. **Verificar Python y Git**:
   - Verifica Python: `python3 --version`
   - Verifica Git: `git --version`
   - Configura claves SSH para GitHub u otros hosts de Git según sea necesario.

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
Esto procesa todos los repositorios listados en `mos-git-sync.json`.

##### Sincronizar un Repositorio Específico
```bash
python /path/to/mos-git-sync.py --repo <nombre-repositorio>
```
Sustituye `<nombre-repositorio>` por el `name` del JSON (por ejemplo, `zx-game-maker-metsuos`).

##### Ejemplo de Salida
```plaintext
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
El script crea la siguiente estructura bajo `management_dir`:
```
/Volumes/WDBOOK_2411/MetsuOS/data/dev-git/
├── sync/
│   ├── zx-game-maker-metsuos/
│   └── mos-retrotools-launcher/
├── dev/
│   ├── zx-game-maker-metsuos/
│   └── mos-retrotools-launcher/
```

- **`sync`**: Usada para sincronizar forks con repositorios originales.
- **`dev`**: Usada para copias locales de desarrollo, actualizadas desde el fork.

#### Resolución de Problemas

- **FileNotFoundError: Config file mos-git-sync.json not found**:
  - Asegúrate de que `mos-git-sync.json` esté en el mismo directorio que `mos-git-sync.py`.
- **ValueError: Repository <nombre> not found in config**:
  - Verifica que el argumento `--repo` coincida con un `name` en la configuración JSON.
- **Git command failed**:
  - Comprueba la configuración de claves SSH para GitHub u otros hosts.
  - Resuelve conflictos de fusión manualmente en la carpeta afectada.
- **Conflictos de Fusión**:
  - Si un `git merge` falla, navega a la carpeta del repositorio (por ejemplo, `/Volumes/WDBOOK_2411/MetsuOS/data/dev-git/sync/zx-game-maker-metsuos`), resuelve los conflictos y haz commit antes de volver a ejecutar el script.

#### Contribución

¡Las contribuciones son bienvenidas! Sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama de funcionalidad (`git checkout -b feature/mi-funcionalidad`).
3. Confirma tus cambios (`git commit -m "Añadir mi funcionalidad"`).
4. Sube la rama (`git push origin feature/mi-funcionalidad`).
5. Abre un pull request.

Todas las contribuciones deben cumplir con la **Licencia Pública General de GNU Affero v3.0**.

#### Licencia

Este proyecto está licenciado bajo la **Licencia Pública General de GNU Affero v3.0 (AGPL-3.0)**. Consulta el archivo [LICENSE](LICENSE) para más detalles. Esta licencia garantiza que el código fuente esté disponible libremente, y cualquier modificación o trabajo derivado debe también estar licenciado bajo AGPL-3.0, incluyendo la disponibilidad del código fuente si el software se usa en un entorno de red.

#### Acerca de MetsuOS

`mos-git-sync` forma parte del proyecto **MetsuOS**, una iniciativa enfocada en crear herramientas y entornos para entusiastas de la computación retro. MetsuOS busca proporcionar una experiencia fluida para gestionar y desarrollar software para sistemas vintage, con un enfoque en principios de código abierto.

Para problemas, sugerencias o contribuciones, visita el [repositorio en GitHub](git@github.com:metsuke/mos-git-sync.git).

---

## English

### mos-git-sync

`mos-git-sync` is a Python script designed to automate the synchronization of branches (including non-`main` branches) from upstream repositories to your forks, as well as maintain up-to-date local copies of your working repositories. The "mos" in `mos-git-sync` stands for **MetsuOS**, a project focused on retro computing tools and environments. This script is particularly useful for managing multiple Git repositories, ensuring that forks are synchronized with their upstream counterparts and that local development copies are kept current.

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**, ensuring that the source code is freely available and that any derivative works are also open source.

#### Features

- **Synchronize Forks**: Automatically sync specified branches from an upstream repository to your fork.
- **Local Development Copies**: Maintain up-to-date local clones of your repositories for development.
- **Configurable**: Uses a JSON configuration file to define repositories, their upstream and fork URLs, and branches to sync.
- **Dual Folder Structure**: Manages repositories in two folders:
  - `sync`: For synchronizing forks with upstream repositories.
  - `dev`: For maintaining local development copies updated from the fork.
- **Verbose Output**: Provides clear, concise feedback on each action (cloning, fetching, merging, pushing) for each repository and branch.
- **Support for Non-Fork Repositories**: Skips upstream synchronization for repositories where the origin and fork URLs are the same, only updating the `dev` copy.

#### Requirements

- **Python**: Version 3.6 or higher.
- **Git**: Installed and configured with SSH access to the repositories (e.g., GitHub SSH keys).
- **Operating System**: Compatible with Linux, macOS, or Windows (with Git Bash or similar).

#### Installation

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:metsuke/mos-git-sync.git
   cd mos-git-sync
   ```

2. **Ensure Python and Git are Installed**:
   - Verify Python: `python3 --version`
   - Verify Git: `git --version`
   - Configure SSH keys for GitHub or other Git hosts as needed.

3. **Place the Configuration File**:
   - Create a file named `mos-git-sync.json` in the same directory as `mos-git-sync.py` (e.g., `/Volumes/WDBOOK_2411/MetsuOS/system/tools/`).
   - See the [Configuration](#configuration-1) section for details.

#### Configuration

The script requires a JSON configuration file named `mos-git-sync.json`, located in the same directory as `mos-git-sync.py`. This file specifies the management directory for repositories and the list of repositories to process.

##### Example `mos-git-sync.json`
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

- **`management_dir`**: The root directory where repositories are stored. Subdirectories `sync` and `dev` will be created here.
- **`repositories`**: A list of repositories, each with:
  - `name`: A unique identifier for the repository.
  - `url-origen`: The upstream repository URL (for forks).
  - `url-fork`: Your fork's URL (or the same as `url-origen` for non-fork repositories).
  - `branches`: List of branches to synchronize.

For non-fork repositories (where `url-origen` equals `url-fork`), the script skips the `sync` phase and only updates the `dev` folder.

#### Usage

Run the script from any directory, specifying the full path to `mos-git-sync.py`. The script will automatically locate `mos-git-sync.json` in its own directory.

##### Sync All Repositories
```bash
python /path/to/mos-git-sync.py
```
This processes all repositories listed in `mos-git-sync.json`.

##### Sync a Specific Repository
```bash
python /path/to/mos-git-sync.py --repo <repository-name>
```
Replace `<repository-name>` with the `name` from the JSON (e.g., `zx-game-maker-metsuos`).

##### Example Output
```plaintext
Loading configuration from: /Volumes/WDBOOK_2411/MetsuOS/system/tools/mos-git-sync.json
Ensuring management directory exists: /Volumes/WDBOOK_2411/MetsuOS/data/dev-git
Ensuring sync directory exists: /Volumes/WDBOOK_2411/MetsuOS/data/dev-git/sync
Ensuring dev directory exists: /Volumes/WDBOOK_2411/MetsuOS/data/dev-git/dev

Processing repository: zx-game-maker-metsuos
Starting sync phase for repository: zx-game-maker-metsuos
Cloning fork to sync folder: /Volumes/WDBOOK_2411/MetsuOS/data/dev-git/sync/zx-game-maker-metsuos
...
```

#### Directory Structure
The script creates the following structure under `management_dir`:
```
/Volumes/WDBOOK_2411/MetsuOS/data/dev-git/
├── sync/
│   ├── zx-game-maker-metsuos/
│   └── mos-retrotools-launcher/
├── dev/
│   ├── zx-game-maker-metsuos/
│   └── mos-retrotools-launcher/
```

- **`sync`**: Used for synchronizing forks with upstream repositories.
- **`dev`**: Used for local development copies, updated from the fork.

#### Troubleshooting

- **FileNotFoundError: Config file mos-git-sync.json not found**:
  - Ensure `mos-git-sync.json` is in the same directory as `mos-git-sync.py`.
- **ValueError: Repository <name> not found in config**:
  - Verify that the `--repo` argument matches a `name` in the JSON configuration.
- **Git command failed**:
  - Check SSH key configuration for GitHub or other hosts.
  - Resolve merge conflicts manually in the affected repository folder.
- **Merge Conflicts**:
  - If a `git merge` fails, navigate to the repository folder (e.g., `/Volumes/WDBOOK_2411/MetsuOS/data/dev-git/sync/zx-game-maker-metsuos`), resolve conflicts, and commit changes before re-running the script.

#### Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -m "Add my feature"`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Open a pull request.

All contributions must comply with the **GNU Affero General Public License v3.0**.

#### License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. See the [LICENSE](LICENSE) file for details. This ensures that the source code is freely available, and any modifications or derivative works must also be licensed under AGPL-3.0, including making the source code available if the software is used in a networked environment.

#### About MetsuOS

`mos-git-sync` is part of the **MetsuOS** project, an initiative focused on creating tools and environments for retro computing enthusiasts. MetsuOS aims to provide a seamless experience for managing and developing software for vintage systems, with a focus on open-source principles.

For issues, suggestions, or contributions, please visit the [GitHub repository](git@github.com:metsuke/mos-git-sync.git).
