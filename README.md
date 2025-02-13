# Pokepedia

## Setup

> NOTE: project uses the "uv" package manager for python. [Install guide](https://docs.astral.sh/uv/#installation).

1. Clone repository

```
git clone https://github.com/p0tatoes/pokemon_exam.git <folder_name>
```

2. Change directory into project folder

```
cd <folder_name>
```

3. Install dependencies (i.e., `Django` and `requests`)

```
uv sync
```

4. Run migrations

```
./manage.py makemigrations 
./manage.py migrate 
```

5. Run server

```
./manage.py runserver
```

6. *(optional)* Generate data for database (data retrieved from [PokeAPI](https://pokeapi.co))

```
./manage.py addpokemon
```