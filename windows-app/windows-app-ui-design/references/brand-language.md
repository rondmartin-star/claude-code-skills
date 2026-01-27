# Brand Language Reference

Load this file when establishing brand identity from a logo.

---

## Logo Analysis Process

When a logo is provided:

1. **Extract Primary Colors**
   - Dominant color → Primary brand color
   - Secondary color → Accent color
   - Background color (if any) → Base tones

2. **Derive Color Palette**
   ```
   From logo colors, generate:
   ├── Primary: Main brand color (buttons, links, headers)
   ├── Primary Light: Hover states, backgrounds
   ├── Primary Dark: Active states, emphasis
   ├── Secondary: Accent elements, highlights
   ├── Neutral: Text, borders, backgrounds
   └── Semantic: Success (green), Warning (amber), Danger (red), Info (blue)
   ```

3. **Determine Typography Style**
   - Logo has serif font → Consider serif for headings
   - Logo has sans-serif → Use modern sans-serif throughout
   - Logo has geometric shapes → Consider geometric fonts (e.g., Inter, Poppins)
   - Logo has organic shapes → Consider humanist fonts (e.g., Open Sans, Lato)

4. **Identify Visual Motifs**
   - Rounded corners vs sharp edges
   - Heavy vs light stroke weights
   - Spacing density (compact vs airy)

---

## Brand Language Document Template

```markdown
# [Application Name] Brand Language

## Logo Reference
[Describe key logo characteristics]

## Color Palette

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Primary | #XXXXXX | Buttons, links, active states |
| Primary Light | #XXXXXX | Hover backgrounds, highlights |
| Primary Dark | #XXXXXX | Active states, headers |

### Secondary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Secondary | #XXXXXX | Accents, icons, badges |
| Secondary Light | #XXXXXX | Background tints |

### Neutral Colors
| Name | Hex | Usage |
|------|-----|-------|
| Text Primary | #XXXXXX | Main body text |
| Text Secondary | #XXXXXX | Muted text, labels |
| Background | #XXXXXX | Page background |
| Surface | #XXXXXX | Cards, modals |
| Border | #XXXXXX | Dividers, input borders |

### Semantic Colors
| Name | Hex | Usage |
|------|-----|-------|
| Success | #XXXXXX | Confirmations, positive actions |
| Warning | #XXXXXX | Cautions, pending states |
| Danger | #XXXXXX | Errors, destructive actions |
| Info | #XXXXXX | Informational messages |

## Typography

### Font Stack
- **Headings:** [Font name], [fallbacks]
- **Body:** [Font name], [fallbacks]
- **Monospace:** [Font name], [fallbacks]

### Scale
| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 2rem | 700 | 1.2 |
| H2 | 1.5rem | 600 | 1.3 |
| H3 | 1.25rem | 600 | 1.4 |
| Body | 1rem | 400 | 1.5 |
| Small | 0.875rem | 400 | 1.5 |

## Component Styling

### Buttons
- Border radius: [Xpx]
- Padding: [X Y]
- Primary: bg-[primary], text-white
- Secondary: bg-transparent, border-[primary], text-[primary]
- Danger: bg-[danger], text-white

### Cards
- Border radius: [Xpx]
- Shadow: [shadow definition]
- Border: [if any]

### Form Inputs
- Border radius: [Xpx]
- Border color: [neutral]
- Focus ring: [primary]

## Dark Theme Mapping

| Light Theme | Dark Theme |
|-------------|------------|
| Background #XXXXXX | Background #XXXXXX |
| Surface #XXXXXX | Surface #XXXXXX |
| Text Primary #XXXXXX | Text Primary #XXXXXX |
| Primary #XXXXXX | Primary #XXXXXX (adjust if needed) |
```

---

## CSS Variables Template

```css
:root {
    /* Brand Colors - derived from logo */
    --brand-primary: #XXXXXX;
    --brand-primary-light: #XXXXXX;
    --brand-primary-dark: #XXXXXX;
    --brand-secondary: #XXXXXX;
    
    /* Neutral Colors */
    --color-text: #212529;
    --color-text-muted: #6c757d;
    --color-background: #f8f9fa;
    --color-surface: #ffffff;
    --color-border: #dee2e6;
    
    /* Semantic Colors */
    --color-success: #198754;
    --color-warning: #ffc107;
    --color-danger: #dc3545;
    --color-info: #0dcaf0;
    
    /* Typography */
    --font-heading: 'Inter', system-ui, sans-serif;
    --font-body: 'Inter', system-ui, sans-serif;
    --font-mono: 'Fira Code', monospace;
    
    /* Spacing & Sizing */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 1rem;
}

[data-bs-theme="dark"] {
    --color-text: #f8f9fa;
    --color-text-muted: #adb5bd;
    --color-background: #121212;
    --color-surface: #1e1e1e;
    --color-border: #404040;
    
    /* Adjust brand colors for dark mode if needed */
    --brand-primary: #XXXXXX;
}
```

---

## Default Palette (No Logo)

Use when no logo is provided:

```css
:root {
    --brand-primary: #0d6efd;      /* Bootstrap blue */
    --brand-primary-light: #3d8bfd;
    --brand-primary-dark: #0a58ca;
    --brand-secondary: #6c757d;
}
```

Note in documentation: "Customize --brand-* variables in app.css to match your organization's branding."

---

*End of Brand Language Reference*
