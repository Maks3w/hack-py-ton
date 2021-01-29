# Albums

## Clone the repository with Git LFS

1. Install Git LFS, so we can retrieve binaries hosted outside of Git

    ```bash
    git lfs install
    ```

2. Clone the repo

    ```bash
    git lfs clone git@github.com:Maks3w/album.git
    ```

## Run

1. Start the application

    ```bash
    docker-compose up --build
    ```

2. Visit the web interface

    http://host.docker.internal:8000

## Cleanup everything

```bash
docker-compose down --volumes --remove-orphans --rmi all
```

Optionally you may cleanup your Docker from old resources (Warning: This may remove containers from other projects as well):

```bash
docker system prune
```

## Internal console

```bash
docker-compose exec app python manage.py shell
```

## Admin panel

http://host.docker.internal:8000/admin

User: `root`

Password: `root`
