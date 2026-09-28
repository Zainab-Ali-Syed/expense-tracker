# Spec: Login and Logout

## Overview
This feature implements the authentication flow for Spendly. It allows registered users to authenticate themselves using their email and password, establishing a session that persists across requests. It also provides a way to securely terminate that session. This is a critical foundation for all subsequent features, as almost all remaining routes require a logged-in user to function.

## Depends on
- Registration (Step 02)

## Routes
- POST /login — Authenticates user and starts session — public
- GET /logout — Terminates session and redirects to login — logged-in

## Database changes
No database changes.

## Templates
- Modify: `login.html` — Add form handling and error messages.

## Files to change
- `app.py` — Implement `/login` (POST) and `/logout` logic.
- `database/db.py` — Add a helper function to fetch a user by email.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use Flask `session` to store the `user_id`

## Definition of done
- [ ] User can log in with valid credentials and is redirected to the profile page (even if it is currently a stub).
- [ ] User sees an error message when attempting to log in with an invalid email or password.
- [ ] User can click a logout link/button and is redirected back to the login page.
- [ ] Accessing a logged-in route (like `/profile`) while logged out redirects the user to the login page.
