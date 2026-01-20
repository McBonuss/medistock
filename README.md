# MediStock Pro

A Django full stack application for **medical consumables** that combines a simple e-commerce shop (Stripe test payments) with a **per-location stock tracker** (low-stock alerts + movement logging).

## Value
Smaller clinics, wards, and care providers can:

- Purchase consumables (gloves, syringes, dressings) via a cart and Stripe Checkout (test mode)
- Track stock per **Organisation Location** (e.g., "Ward 3", "Clinic A")
- Log stock movements (IN/OUT/ADJUST) with server-side validation
- See low-stock items and reorder quickly
- Leave product reviews

## Key features (assessment)

- **Django full stack** with **multiple reusable apps**: `accounts`, `catalog`, `cart`, `checkout`, `inventory`, `reviews`
- **Relational database**: SQLite locally; PostgreSQL via `DATABASE_URL` in production
- **Custom models** (beyond course examples): Organisation/Location/UserProfile, StockItem/StockMovement/ReceivedLot, Orders, etc.
- **Authentication & authorization**: register/login required for cart persistence, orders, and inventory access
- **Forms with validation**: stock movement form prevents negative quantities and prevents consuming more than on-hand
- **Stripe (test mode)**: successful payment creates an Order and unlocks the Inventory Dashboard (`paid_access`)
- **JavaScript UX**: live cart count badge and low-stock-only filter on inventory table
- **Deployment**: ready for Heroku (`Procfile`, `requirements.txt`, `runtime.txt`, Whitenoise)
- **Security**: uses environment variables for secrets/keys, `DEBUG=False` supported

## User stories

1. As a user, I can register and log in so my cart and orders persist.
2. As a user, I can browse products and add them to a basket.
3. As a user, I can pay via Stripe test checkout and see a confirmation.
4. As a user, I gain access to the inventory dashboard after a successful payment.
5. As an organisation admin, I can create locations and choose which products to track for each location.
6. As a user, I can log stock movements and the system prevents invalid usage entries.

## Database schema (high level)

- Organisation → Locations (1-to-many)
- UserProfile → Organisation (many users per org)
- Category → Products (1-to-many)
- Cart → CartItems (1-to-many)
- Order → OrderLineItems (1-to-many)
- Location → StockItems (1-to-many)
- StockItem → StockMovements (1-to-many)
- Product → Reviews (1-to-many)

## Setup (local)

1. Create a virtualenv and install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` from `.env.example` and add your Stripe **test** keys.

3. Run migrations and start the server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

4. (Optional) Load starter Categories and Products:

```bash
python manage.py loaddata catalog/fixtures/starter_catalog.json
```

5. Login to Django admin:

- `/admin/` – manage Categories, Products, Orders

If you do not load the fixture, you can create Categories and Products manually in admin.

## Stripe test cards

- Success: `4242 4242 4242 4242` (any future expiry, any CVC)

## Test login credentials

- Admin email: Admin@nhs.net
- Password: not set (create via `createsuperuser`)

## How the "payment unlock" works

After Stripe Checkout returns with a paid session, the app:

- creates `OrderLineItem` snapshots
- sets `Order.status = paid`
- sets `UserProfile.paid_access = True`

The Inventory Dashboard requires `paid_access`.

## Deployment (Heroku)

1. Set config vars in Heroku:

- `SECRET_KEY`
- `DEBUG` = `False`
- `ALLOWED_HOSTS` = your Heroku app domain
- `DATABASE_URL` (Heroku Postgres)
- `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`

2. Push to Heroku and run migrations:

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Testing

Run tests:

```bash
python manage.py test
```

### Manual test checklist

- Register user → login
- Add products to cart → cart updates
- Checkout → Stripe test payment → success page
- Inventory Dashboard accessible after success
- Stock movement OUT consumes stock and cannot exceed on-hand

## Credits / Attribution

- Bootstrap 5 via CDN
- Stripe Checkout integration uses Stripe's documented Python SDK patterns
