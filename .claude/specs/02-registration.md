# Spec: Registration

## Overview
This feature implements the user registration process, allowing new users to create an account by providing their name, email, and password. This is a foundational step in the Spendly roadmap, enabling personalized expense tracking by associating data with specific user accounts.

## Depends on
- 01-database-setup ('users' table, 'get_db()')

## Routes
- 'GET /register' - render registration form - public (already exists as stub, upgrade it)
- 'POST /register' — process registration form, insert user, redirect to '/login' -public

## Database changes
No database changes (the `users` table already exists).

## Templates
- Modify: `templates/register.html` — Update the form to use `POST` method and include appropriate `name` attributes for inputs.

## Files to change
- `app.py` — Implement the `POST` handler for the `/register` route.
- `database/db.py` — Add a helper function to create a new user.
- `templates/register.html` — Ensure the form is correctly configured for submission.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html

## Definition of done
- [ ] Navigating to `/register` displays the registration form.
- [ ] Submitting the form with valid data successfully creates a user in the `users` table.
- [ ] Passwords are stored as hashes, not plain text.
- [ ] Attempting to register with an email that already exists results in a clear error message (handling the `UNIQUE` constraint).
- [ ] The user is redirected to the login page upon successful registration.
