# Pocket Aquarium

A small Django project with an animated fish tank. Every fish lives in the
database, swims across the screen, turns around at the edges, and grows when
you feed it.

## Run it

```bash
# 1. (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. install Django
pip install -r requirements.txt

# 3. create the database (this also adds 3 starter fish)
python manage.py migrate

# 4. start the server
python manage.py runserver
```

Open http://127.0.0.1:8000/

Optional: `python manage.py createsuperuser` and visit `/admin/` to edit fish.
Run the tests with `python manage.py test`.

## What to try

- Click a fish to feed it. It munches, shows +1, and grows. Levels: Tiny, Growing, Chunky, Legend.
- Add a fish in the panel (name, colour, size, swim speed). It splashes in.
- Release a fish from the list and it sinks away.

## How it works

| Piece | Where | Job |
|-------|-------|-----|
| `Fish` model | `tank/models.py` | name, colour, size, speed, depth, meals |
| Views | `tank/views.py` | `index` (tank + add form), `feed` and `release` (JSON endpoints) |
| Template | `tank/templates/tank/index.html` | draws the tank and one inline SVG per fish |
| Animation | `tank/static/tank/style.css` | swimming, turning, tail wag, bubbles, kelp, light rays, waves |
| Interaction | `tank/static/tank/app.js` | feeding effects, bubbles, release, panel toggle |

The swimming is pure CSS: each fish gets its own duration, depth and start
offset from the database as CSS variables (`--dur`, `--top`, `--delay`). The
fish flips at each edge with a second animation that runs in step with the swim.
Animations calm down automatically for people who prefer reduced motion.

## Ideas to extend it

- Add a `species` field with different fish shapes.
- Let fish get hungry over time (compare `now` to a `last_fed` timestamp).
- Add user accounts so each person has their own tank.
