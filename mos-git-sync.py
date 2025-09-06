import argparse
import json
import os
import subprocess
from typing import List, Dict

def setup_ssh_agent():
    """Inicia el ssh-agent y agrega la clave SSH."""
    try:
        # Verifica si ssh-agent ya está corriendo
        if 'SSH_AUTH_SOCK' not in os.environ:
            print("Iniciando ssh-agent...")
            # Iniciar ssh-agent y capturar su salida
            result = subprocess.run(['ssh-agent', '-s'], capture_output=True, text=True, check=True)
            # Parsear la salida para obtener SSH_AUTH_SOCK y SSH_AGENT_PID
            env_vars = {}
            for line in result.stdout.splitlines():
                if line.startswith('SSH_AUTH_SOCK') or line.startswith('SSH_AGENT_PID'):
                    key, value = line.split('=', 1)
                    env_vars[key.split('=')[0]] = value.split(';')[0]
            # Actualizar variables de entorno
            os.environ.update(env_vars)
        else:
            print("ssh-agent ya está corriendo.")

        # Agregar la clave SSH (asegúrate de que ~/.ssh/id_rsa existe o especifica tu clave)
        print("Agregando clave SSH...")
        subprocess.run(['ssh-add', os.path.expanduser('~/.ssh/id_rsa')], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error al configurar ssh-agent o ssh-add: {e.stderr}")

def run_git_command(cmd: List[str], cwd: str) -> str:
    """Run a git command in the specified working directory."""
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command failed: {' '.join(cmd)}\nError: {e.stderr}")

def ensure_dir_exists(path: str):
    """Ensure the directory exists, create if not."""
    if not os.path.exists(path):
        print(f"Creating directory: {path}")
        os.makedirs(path)

def has_remote(cwd: str, remote_name: str) -> bool:
    """Check if a remote exists."""
    print(f"Checking for remote '{remote_name}' in {cwd}")
    remotes = run_git_command(['git', 'remote', '-v'], cwd)
    return remote_name in [line.split()[0] for line in remotes.splitlines()]

def has_local_branch(cwd: str, branch: str) -> bool:
    """Check if a local branch exists."""
    print(f"Checking for local branch '{branch}' in {cwd}")
    branches = run_git_command(['git', 'branch', '--list'], cwd)
    return branch in [b.strip('* ') for b in branches.splitlines()]

def sync_repo(repo: Dict, management_dir: str):
    """Sync the repository branches in sync and dev folders."""
    name = repo['name']
    url_origen = repo['url-origen']
    url_fork = repo['url-fork']
    branches = repo['branches']

    repo_sync_path = os.path.join(management_dir, 'sync', name)
    repo_dev_path = os.path.join(management_dir, 'dev', name)

    skip_sync = (url_origen == url_fork)

    if not skip_sync:
        print(f"Starting sync phase for repository: {name}")
        # Handle sync folder
        if not os.path.exists(repo_sync_path):
            print(f"Cloning fork to sync folder: {repo_sync_path}")
            ensure_dir_exists(os.path.dirname(repo_sync_path))
            run_git_command(['git', 'clone', url_fork, name], os.path.join(management_dir, 'sync'))
        else:
            print(f"Fetching origin for sync folder: {repo_sync_path}")
            run_git_command(['git', 'fetch', 'origin'], repo_sync_path)

        # Add upstream if not exists
        if not has_remote(repo_sync_path, 'upstream'):
            print(f"Adding upstream remote: {url_origen}")
            run_git_command(['git', 'remote', 'add', 'upstream', url_origen], repo_sync_path)

        # Fetch upstream
        print(f"Fetching upstream for sync folder: {repo_sync_path}")
        run_git_command(['git', 'fetch', 'upstream'], repo_sync_path)

        # Sync each branch
        for branch in branches:
            print(f"Processing branch '{branch}' in sync folder")
            if not has_local_branch(repo_sync_path, branch):
                print(f"Creating branch '{branch}' from upstream/{branch}")
                run_git_command(['git', 'checkout', '-b', branch, f'upstream/{branch}'], repo_sync_path)
            else:
                print(f"Checking out branch '{branch}'")
                run_git_command(['git', 'checkout', branch], repo_sync_path)
                print(f"Merging upstream/{branch} into '{branch}'")
                run_git_command(['git', 'merge', f'upstream/{branch}'], repo_sync_path)
            print(f"Pushing branch '{branch}' to origin")
            run_git_command(['git', 'push', 'origin', branch], repo_sync_path)

    print(f"Starting dev phase for repository: {name}")
    # Handle dev folder
    if not os.path.exists(repo_dev_path):
        print(f"Cloning fork to dev folder: {repo_dev_path}")
        ensure_dir_exists(os.path.dirname(repo_dev_path))
        run_git_command(['git', 'clone', url_fork, name], os.path.join(management_dir, 'dev'))
    else:
        print(f"Fetching origin for dev folder: {repo_dev_path}")
        run_git_command(['git', 'fetch', 'origin'], repo_dev_path)
    
    # Update each branch in dev
    for branch in branches:
        print(f"Processing branch '{branch}' in dev folder")
        remote_branches = run_git_command(['git', 'branch', '-r'], repo_dev_path)
        if has_local_branch(repo_dev_path, branch):
            print(f"Checking out branch '{branch}'")
            run_git_command(['git', 'checkout', branch], repo_dev_path)
            print(f"Merging origin/{branch} into '{branch}'")
            run_git_command(['git', 'merge', f'origin/{branch}'], repo_dev_path)
        elif f'origin/{branch}' in remote_branches:
            print(f"Creating branch '{branch}' from origin/{branch}")
            run_git_command(['git', 'checkout', '-b', branch, f'origin/{branch}'], repo_dev_path)
        else:
            print(f"Skipping branch '{branch}' in dev folder (not found in origin)")

def main():
    # Configurar ssh-agent al inicio
    setup_ssh_agent()

    # Get script directory and construct config file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.basename(__file__)
    config_file = os.path.join(script_dir, os.path.splitext(script_name)[0] + '.json')

    # Load config
    print(f"Loading configuration from: {config_file}")
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file {config_file} not found.")
    with open(config_file, 'r') as f:
        config = json.load(f)

    management_dir = config.get('management_dir')
    if not management_dir:
        raise ValueError("management_dir not specified in config file.")
    
    repos = config.get('repositories', [])

    # Parse arguments
    parser = argparse.ArgumentParser(description='Automate repo branch syncing.')
    parser.add_argument('--repo', type=str, default=None, help='Specific repository name to sync (optional).')
    args = parser.parse_args()

    specific_repo = args.repo

    # Ensure management dir and subdirs exist
    print(f"Ensuring management directory exists: {management_dir}")
    ensure_dir_exists(management_dir)
    print(f"Ensuring sync directory exists: {os.path.join(management_dir, 'sync')}")
    ensure_dir_exists(os.path.join(management_dir, 'sync'))
    print(f"Ensuring dev directory exists: {os.path.join(management_dir, 'dev')}")
    ensure_dir_exists(os.path.join(management_dir, 'dev'))

    # Filter repos if specific one is given
    if specific_repo:
        print(f"Filtering for specific repository: {specific_repo}")
        repos = [r for r in repos if r['name'] == specific_repo]
        if not repos:
            raise ValueError(f"Repository {specific_repo} not found in config.")

    for repo in repos:
        print(f"\nProcessing repository: {repo['name']}")
        sync_repo(repo, management_dir)

if __name__ == '__main__':
    main()