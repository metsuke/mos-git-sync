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