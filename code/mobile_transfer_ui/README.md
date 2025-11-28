# Mobile Fund Transfer UI Prototype (F010)

This folder contains a static HTML/CSS/JS prototype for the Mobile Fund Transfer feature (F010). It implements Story S010 and related validation/accessibility goals.

## Contents
- `index.html` – Markup for the form & confirmation
- `styles.css` – Responsive + accessible styling
- `app.js` – Client-side validation + confirmation toggle
- Spec references: `specs/features/F010-fund-transfer-ui.md`, `specs/featurefiles/F010-fund-transfer-ui.feature`

## Running
Open `index.html` locally in any modern browser. No build step required.

## Form Fields
| Field | Type | Validation |
|-------|------|------------|
| From Account | select | Required |
| Beneficiary Account | text | Pattern [A-Za-z0-9]{10,14} |
| Amount (USD) | text | Numeric >0 ≤10000, formatted to 2 decimals |
| Transfer Date | date | Required (defaults to today) |
| Description | textarea | Optional, max 140 chars, sanitized |

## Validation Behavior
- Inline error under each field
- Summary banner lists all current issues
- Confirmation view only appears if validation passes

## Accessibility Checklist
- Labels associated with inputs via `for`/`id`
- Error messages use `role="alert"` and summary uses `aria-live="polite"`
- Keyboard focus visible; no removal of outline
- Sufficient color contrast for text and buttons
- Semantic landmarks: `<main>` and headings hierarchy

## Security (Prototype Level)
- Basic client-side sanitization for description & displayed values
- Future: integrate server-side validation, CSRF, audit logging

## Responsive Design
- <600px: single column
- ≥600px: two-column layout for key fields

## Future Enhancements (Not in Prototype)
- Real account list fetched from API
- Multi-factor confirmation (OTP)
- Transfer scheduling beyond current date
- Currency selection and FX computation
- Beneficiary management / nickname storage

## Traceability
- Feature: F010
- Story: S010 (primary)
- Additional Stories (planned): S011 validation refinement, S012 accessibility optimization, S013 confirmation enhancements, S014 test documentation

## Testing References
Manual test case docs added under `tests/stories/` (see `S010_FUNC_TC001_Valid_Form_Submission.md` etc.).