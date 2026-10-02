---
name: spendly-ui-designer
description: Designs and builds production-ready UI pages and components for Spendly, a Flask + Jinja + vanilla-JS personal expense tracker (repo Zainab-Ali-Syed/expense-tracker). Use whenever the user says things like "design the ___ page", "create UI for ___", "build a component for ___", "redesign / improve ___", or asks for any Spendly screen such as dashboard, expenses list, add/edit expense form, profile, analytics, categories, empty states, modals or cards. Trigger even when the user doesn't say "UI" explicitly, as long as it's about how a Spendly page or component should look or be laid out. Outputs a brief UX structure plus Jinja template and CSS that match the existing warm paper/forest-green design.
---

# Spendly UI Designer

Generate clean, modern, fintech-style UI for Spendly that looks like it was always part of the app. Consistency with the existing design beats novelty.

## Inputs

- **Page/component name** (required), e.g. "dashboard", "expense card", "add-expense form"
- Optional: constraints, sample data, references, screenshots

If the name is vague ("make it look better"), ask one short question. If the request depends on existing screens you can't see, ask for screenshots (see Consistency below).

## Hard constraints (from the repo's CLAUDE.md)

- **Stack:** Flask + Jinja2 + vanilla JS. No React, jQuery, Tailwind, or npm packages. No new pip packages.
- New pages are a new `.html` file that `{% extends "base.html" %}`.
- Page-specific styles go in a **new CSS file** (`static/css/<page>.css`), loaded via `{% block head %}`. Never inline `<style>` tags or inline `style=""`.
- Every internal link uses `url_for()`. Never hardcode URLs.
- No DB logic in templates or routes. Design against a documented context shape (see Output).
- **Do not implement stub routes** (`/profile`, `/expenses/add`, etc.) unless the user explicitly asks. Deliver template + CSS, and state which route/context it expects.
- Currency is rupees: format as `₹{{ '{:,.2f}'.format(amount) }}` unless told otherwise.

## Design system (match, don't reinvent)

Read `references/design-tokens.md` before writing CSS. Short version:

- Use the existing CSS variables from `style.css` (`--paper`, `--paper-card`, `--ink*`, `--accent`, `--accent-light`, `--accent-2`, `--danger`, `--border`, `--radius-*`, `--font-*`). Never hardcode hex values that already have a variable.
- Warm paper background, white cards, forest-green accent, amber as secondary highlight, red only for danger/overspend.
- Headings use DM Serif Display (`--font-display`); everything else DM Sans.
- Cards: white, 1px `--border`, `--radius-md` (12px), soft shadow (`0 2px 10px rgba(0,0,0,0.03)`; hover/elevated `0 8px 40px rgba(0,0,0,0.06)`).
- Spacing on an **8px grid**: use multiples of `0.5rem` (0.5, 1, 1.5, 2, 3, 4rem).
- Reuse existing classes (`.btn-primary`, `.btn-ghost`, `.btn-submit`, `.form-group`, `.form-input`, `.auth-card`, `.auth-error`) before creating new ones. Prefix new classes with the page or component name (`.expense-card`, `.dash-summary`) to avoid collisions.

## Icons: Lucide via CDN

Spendly's current icons are Unicode glyphs; new UI uses Lucide.

1. Make sure `base.html` loads Lucide once, before `main.js`:
   ```html
   <script src="https://unpkg.com/lucide@0.469.0/dist/umd/lucide.min.js"></script>
   ```
   If it isn't there yet, include that one-line `base.html` change in your output and call it out.
2. Initialize once in `static/js/main.js`: `lucide.createIcons();` (and call it again after any JS that injects new icon markup).
3. Use icons as `<i data-lucide="wallet" class="icon"></i>`. Size via a CSS class (`.icon { width: 1.25rem; height: 1.25rem; stroke-width: 1.75; }`), colored with `currentColor`.
4. Icons carry meaning, not decoration. Good picks: `wallet`, `receipt`, `plus`, `pencil`, `trash-2`, `calendar`, `tag`, `utensils`, `car`, `shopping-bag`, `home`, `heart-pulse`, `trending-up`, `trending-down`, `filter`, `search`, `chevron-right`. Pair icon-only buttons with `aria-label`.

## Process

1. **Understand the screen's job.** Who uses it, what's the one primary action, what data does it show? Expense tracker pages are glanceable: lead with the number or action that matters most.
2. **Check existing design.** Read the repo files if available (`static/css/style.css`, `templates/base.html`, the closest existing template). If you can't see them and the request touches existing screens, ask for screenshots before designing.
3. **Plan layout + UX decisions** (brief).
4. **Write the Jinja template and CSS.**
5. **Self-check** against the checklist below before responding.

## Output format

Always produce these sections in order:

### 1. UI structure (brief)
- Layout in 3-6 lines: key sections top to bottom, and the grid behavior on desktop vs mobile.
- 2-4 important UX decisions, each one line with the reason (e.g. "Amount is right-aligned and bold so columns scan quickly").

### 2. Code
Deliver as files, each with its path as a heading:
- `templates/<page>.html`: extends `base.html`, sets `{% block title %}`, loads the page CSS in `{% block head %}`.
- `static/css/<page>.css`: clean, grouped by section with short comments.
- `static/js/main.js` additions only if interaction is needed (vanilla JS, minimal).
- Reusable pieces as **Jinja macros or `{% include %}` partials** (e.g. `templates/partials/_expense_row.html`) so they're modular, not copy-pasted.
- A short **"Expected context"** note listing the variables the template needs, with example values (e.g. `expenses: [{id, title, amount, category, date}]`). Never invent DB helpers.

Write files to the user's project when a workspace is available; otherwise give them as separate labeled code blocks. No giant undifferentiated dumps: every block is labeled and has a purpose.

### 3. Notes (only if needed)
Required `base.html` change, a stub route the page will need, or an open question. Keep it to a few lines.

## Quality bar

**Visual**
- Modern SaaS feel: clear hierarchy (one focal point per section), generous whitespace, card-based layout.
- Subtle color: accent for primary actions and positive states; muted ink for secondary text; never more than accent + one secondary on a screen.
- Rounded corners and soft shadows only. No heavy borders, gradients, or neon.
- Numbers use tabular figures (`font-variant-numeric: tabular-nums`) so amounts align.

**Usability**
- One obvious primary action per screen.
- Always design **empty, loading-free, and error states** (e.g. "No expenses yet" with an icon and a button to add the first one).
- Forms: visible labels (not placeholder-only), inline error text, sensible input types (`type="number" step="0.01"`, `type="date"`), large tap targets (min 44px high on mobile).
- Destructive actions (delete) use `--danger` and need confirmation.
- Accessible: semantic HTML (`<table>` for tabular data, `<button>` for actions), visible focus states, contrast that passes on the paper background.

**Responsive**
- Mobile-first CSS. Use the repo's breakpoints (`900px`, `600px`) via `@media (max-width: ...)`.
- Grids collapse to a single column on small screens; tables become stacked cards or scroll within their container, never the page.

**Code**
- Plain, readable CSS using variables. No `!important`, no inline styles, no utility-class soup.
- Minimal boilerplate. Semantic class names. No unused CSS.

## Avoid

- Generic or dated UI: default browser controls, Bootstrap-looking layouts, flat gray boxes.
- Random one-off colors, radii, or fonts that aren't in the design tokens.
- Cluttered screens. If a section isn't needed for the page's job, cut it.
- Unstructured code dumps or unlabeled snippets.
- Adding frameworks, packages, or new routes the user didn't ask for.

## Consistency rule

Match the existing project design. If you cannot see the current screens or styles and the request depends on them, **ask for screenshots** of the closest existing page rather than guessing. When the repo is available, read it instead of asking.

## Final self-check

- [ ] Extends `base.html`, uses `url_for()` everywhere
- [ ] Only existing CSS variables; spacing on the 8px grid
- [ ] Page CSS is in its own file, no inline styles
- [ ] Lucide icons present and meaningful, `lucide.createIcons()` handled
- [ ] Empty/error states and mobile layout covered
- [ ] Expected context documented; no stub routes implemented
- [ ] Output has the three sections: structure, code, (notes)