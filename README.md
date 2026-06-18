# MediStock Pro

MediStock Pro is a Django full stack application for medical consumables that combines a simple e-commerce shop with Stripe test payments and a per-location stock tracker with low-stock alerts and movement logging.

## User Experience (UX)

### Value

Smaller clinics, wards, and care providers can:

- Purchase consumables such as gloves, syringes, and dressings via a cart and Stripe Checkout in test mode
- Track stock per Organisation Location such as Ward 3 or Clinic A
- Log stock movements with server-side validation
- See low-stock items and reorder quickly
- Leave product reviews

### User stories

1. As a user, I can register and log in so my cart and orders persist.
2. As a user, I can browse products and add them to a basket.
3. As a user, I can pay via Stripe test checkout and see a confirmation.
4. As a user, I gain access to the inventory dashboard after a successful payment.
5. As an organisation admin, I can create locations and choose which products to track for each location.
6. As a user, I can log stock movements and the system prevents invalid usage entries.

### Design

The interface is intentionally practical and operational. The goal is to make shopping, ordering, and stock control easy to understand and quick to use.

### Wireframes and mockups

The repository includes SVG mockups demonstrating product, cart, and inventory screens across device sizes.

- Product card + location stock example: [static/images/product_design_1.svg](static/images/product_design_1.svg)
- Low-stock + product details mockup: [static/images/product_design_2.svg](static/images/product_design_2.svg)
- Product list desktop: [static/images/mockups/product_list_desktop.svg](static/images/mockups/product_list_desktop.svg)
- Product list tablet: [static/images/mockups/product_list_tablet.svg](static/images/mockups/product_list_tablet.svg)
- Product list mobile: [static/images/mockups/product_list_mobile.svg](static/images/mockups/product_list_mobile.svg)
- Product detail desktop: [static/images/mockups/product_detail_desktop.svg](static/images/mockups/product_detail_desktop.svg)
- Cart mobile: [static/images/mockups/cart_mobile.svg](static/images/mockups/cart_mobile.svg)
- Inventory dashboard tablet: [static/images/mockups/inventory_dashboard_tablet.svg](static/images/mockups/inventory_dashboard_tablet.svg)

For more context and design notes see [docs/design_notes.md](docs/design_notes.md) and the visual index [docs/visuals.md](docs/visuals.md).

## Features

- Django full stack project with multiple reusable apps: accounts, catalog, cart, checkout, inventory, reviews
- Relational database support with SQLite locally and PostgreSQL via DATABASE_URL in production
- Custom models beyond the course examples, including Organisation, Location, UserProfile, StockItem, StockMovement, ReceivedLot, Orders, and related records
- Authentication and authorization for cart persistence, orders, and inventory access
- Form validation that prevents negative stock quantities and blocks consuming more than the available on-hand amount
- Stripe test payments that create an Order and unlock the Inventory Dashboard via paid_access
- JavaScript UX for a live cart count badge and a low-stock-only filter on the inventory table
- Heroku-ready deployment with Procfile, requirements.txt, runtime.txt, and Whitenoise
- Environment-variable based configuration for secrets and keys, with DEBUG=False supported

## Technologies Used

### Frameworks, libraries, and tools

- Django
- Bootstrap 5 via CDN
- Stripe Checkout and the Stripe Python SDK
- Whitenoise
- PostgreSQL via DATABASE_URL
- SQLite for local development

### Project structure

- accounts, catalog, cart, checkout, inventory, reviews as reusable Django apps
- config for project settings, URL routing, and context processors
- static for CSS, JavaScript, and images
- templates for shared and app-specific templates

## Setup (local)

1. Create a virtualenv and install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a .env from .env.example and add your Stripe test keys.

3. Run migrations and start the server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

4. Optional: load starter Categories and Products:

```bash
python manage.py loaddata catalog/fixtures/starter_catalog.json
```

5. Login to Django admin at /admin/ to manage Categories, Products, and Orders.

If you do not load the fixture, you can create Categories and Products manually in admin.

## Database schema

- Organisation -> Locations (1-to-many)
- UserProfile -> Organisation (many users per org)
- Category -> Products (1-to-many)
- Cart -> CartItems (1-to-many)
- Order -> OrderLineItems (1-to-many)
- Location -> StockItems (1-to-many)
- StockItem -> StockMovements (1-to-many)
- Product -> Reviews (1-to-many)

## Testing

Run the test suite with:

```bash
python manage.py test
```

### Manual test checklist

- Register user and log in
- Add products to cart and confirm the cart updates
- Complete checkout with Stripe test payment and confirm the success page
- Confirm the Inventory Dashboard becomes accessible after payment
- Verify stock movement OUT consumes stock and cannot exceed on-hand

### Stripe test cards

- Success: 4242 4242 4242 4242 with any future expiry and any CVC

### Demo mode

Set MOCK_STRIPE_SUCCESS=True to simulate a successful checkout without calling Stripe.
This bypass only works when DEBUG=True; Heroku and production should keep DEBUG=False so Stripe Checkout is always used.

### Test login credentials

- Admin email: Admin@nhs.net
- Password: not set (create via createsuperuser)

## Deployment

### Heroku

Set the following config vars in Heroku:

- SECRET_KEY
- DEBUG=False
- ALLOWED_HOSTS to your Heroku app domain
- DATABASE_URL for Heroku Postgres
- STRIPE_PUBLIC_KEY
- STRIPE_SECRET_KEY

Then run migrations and create a superuser:

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Credits

- Bootstrap 5 via CDN
- Stripe Checkout integration uses Stripe's documented Python SDK patterns

## How the payment unlock works

After Stripe Checkout returns with a paid session, the app:

- creates OrderLineItem snapshots
- sets Order.status = paid
- sets UserProfile.paid_access = True

The Inventory Dashboard requires paid_access.

## What's New

- Improved inventory UX with a live low-stock filter and per-location stock insights
- Added server-side validations to stock movements to prevent negative on-hand and over-consumption
- UI polish for product listing and inventory table with clearer low-stock alerts
- Added product design mockups to help with future UI iterations
