# Metronic 9 Tailwind HTML - Internal Guide

## Table of Contents
* [Getting Started](index.md#1-getting-started)
* [Customization](index.md#2-customization)
* [Base Components](base-components.md)
* [Navigation Components](navigation-components.md)
* [Form Components](form-components.md)
* [Plugins](plugins.md)

---

## 1. Getting Started

### 1.1. Introduction
*   Provides an overview of Metronic 9 as a Tailwind CSS toolkit for building web applications.
*   Highlights key features like UI components, demos, pages, etc.

### 1.2. File Structure (Based on Metronic Docs)
*   **`design/`**: Contains the complete Figma design file.
*   **`dist/`**: The destination folder for compiled assets and HTML templates.
    *   `assets/`: Contains all compiled asset files (CSS, JS, media, vendors).
    *   `html/`: Contains the final compiled HTML template files for different demos.
*   **`node_modules/`**: Folder containing installed Node.js dependencies via npm/yarn.
*   **`src/`**: The main theme folder containing source files. **Modifications should happen here.**
    *   `app/`: Contains application-specific code (layouts, pages, widgets).
    *   `core/`: Contains core theme files, including:
        *   `components/`: Core components (TypeScript, OOP based).
        *   `helpers/`: Helper functions and utilities.
        *   `plugins/`: Tailwind CSS components (custom plugins for Tailwind).
        *   `index.ts`: Main entry point file for the theme's JavaScript.
        *   `index.spa.ts`: Entry point for Single Page Application integration (React, Vue, Angular).
        *   `types.ts`: TypeScript type definitions.
    *   `css/`: Contains source CSS files, including `styles.css` (main input for Tailwind CLI).
    *   `vendors/`: Contains source files for 3rd-party vendor libraries.
*   **Root Files**: Configuration files for the project build and tooling:
    *   `.eslintrc.json`: ESLint configuration.
    *   `package.json` / `package-lock.json`: NPM package configuration and lock file.
    *   `postcss.config.js`: PostCSS configuration.
    *   `prettier.config.js`: Prettier configuration.
    *   `tailwind.config.js`: Tailwind CSS configuration.
    *   `tsconfig.json`: TypeScript configuration.
    *   `webpack.config.js`: Main Webpack configuration.
    *   `webpack.vendors.js`: Webpack configuration for vendor libraries.

### 1.3. Installation (Based on Metronic Docs)
*   **Prerequisites:**
    *   Latest LTS version of Node.js installed.
    *   Latest version of NPM installed (`npm install --global npm@latest`).
*   **Steps:**
    1.  **Download Metronic:** Obtain the package from Themeforest.
    2.  **Navigate to Directory:** Open a terminal and change to the package's root directory (e.g., `cd /home/alex/src/ractory/frontend/admin` for our setup).
    3.  **Install Dependencies:** Run `npm install` to download all dependencies specified in `package.json` into the `node_modules` folder. (Note: If installation fails, try `npm cache clean --force` and re-run `npm install`).
    4.  **Build Assets:** Use the following `npm` scripts to compile source files into the `dist/assets` directory:
        *   `npm run build`: Builds all assets (JavaScript, CSS, fonts, vendors) for development.
        *   `npm run build:js`: Builds only JavaScript files into `dist/assets/js`.
        *   `npm run build:css`: Builds only CSS files into `dist/assets/css` (using Tailwind CLI).
        *   `npm run build:css:watch`: Continuously watches source CSS/HTML for changes and recompiles CSS automatically. Necessary when adding/changing Tailwind classes in HTML.
        *   `npm run build:prod`: Builds production-ready, minified assets (JS and CSS) for optimal performance.
*   **Changing Build Output Path:**
    *   The default output directory is `dist/assets`.
    *   To change this:
        1.  Modify the `output` path in `webpack.vendors.js` (e.g., change `dist/assets` to `../my-project/www/assets`).
        2.  Modify the output paths in the `build:css`, `build:css:watch`, and `build:prod` scripts within `package.json` to match the new path.

### 1.4. Integration
*   (Likely discusses integrating Metronic into existing projects, less relevant for starting from scratch).

### 1.5. Multi-Demo Structure
*   Explains that Metronic provides multiple demos (Demo1, Demo2, etc.) showcasing different layouts and features.
*   Our project uses the HTML/JS version, likely based initially on one of these demos (e.g., Demo1).
*   The `dist/html/` directory contains the pre-built output for each demo.

### 1.6. License
*   Requires a license per end-product deployment (Regular License for non-SaaS, Extended License for SaaS).
*   Cannot be used for open-source projects where the code is distributed.
*   Includes lifetime free updates.

### 1.7. References
*   (Likely points to external libraries or resources used by Metronic).

---

## 2. Customization

### 2.1. Webpack Build Process (Based on Metronic Docs)
*   **Role:** Webpack manages, bundles, and optimizes assets (CSS, JS, TS, images, fonts) from `src/` to `dist/`.
*   **CSS Bundle:** Uses Tailwind CLI to compile `src/css/styles.css` into `dist/assets/css/styles.css`.
*   **Core JS Bundle:** Uses Webpack and Babel to compile TypeScript components from `src/core/index.ts` into `dist/assets/js/core.bundle.js`.
*   **App JS/TS Files:** Single `.js` and `.ts` files in `src/app/*` are processed (TS compiled to JS) and copied with original filenames to `dist/assets/js/*`.
*   **Vendor Bundling (`webpack.vendors.js`):**
    *   Defines how 3rd-party assets from `src/vendors/` or `node_modules/` are bundled or copied to `dist/assets/vendors/`.
    *   Examples configured by default: KeenIcons, @form-validation, Leaflet, ApexCharts, PrismJS, Clipboard.
    *   **Adding a New Vendor:**
        1.  Install the package via npm (e.g., `npm install new-vendor --save`).
        2.  Add an entry in `webpack.vendors.js` specifying the source (`src`) files (JS/CSS from `node_modules/new-vendor`) and the destination (`dist`) path within `dist/assets/vendors/new-vendor/`.
        3.  Set `bundle: true` if multiple source files should be combined into one output file.
        4.  Run `npm run build` (or `npm run build:js` if only JS).
        5.  Include the generated vendor CSS/JS files in your HTML (e.g., `dist/assets/vendors/new-vendor/styles.bundle.css`, `dist/assets/vendors/new-vendor/scripts.bundle.js`).
        6.  **Important Order:** Include vendor CSS *before* `dist/assets/css/styles.css` and vendor JS *after* `dist/assets/js/core.bundle.js`.

### 2.2. JavaScript Usage (Based on Metronic Docs)
*   **Required Includes:** HTML pages need to include the core CSS bundle (`dist/assets/css/styles.css`), the core JS bundle (`dist/assets/js/core.bundle.js`), and any necessary vendor CSS/JS bundles.
*   **Component Initialization:**
    *   **Method 1: Data Attributes (Automatic):**
        *   Add specific `data-*` attributes to HTML elements (e.g., `<button data-tooltip="#my_tooltip_content">`).
        *   Components are automatically initialized on page load by `KTComponents.init()` (called within `core.bundle.js`).
        *   Use `KTComponents.init()` manually to initialize components added dynamically after page load.
        *   Retrieve instance via `KTComponent.getInstance(element)`.
    *   **Method 2: Manual JavaScript/TypeScript:**
        *   Add `data-component="false"` to the HTML element to prevent auto-initialization.
        *   Use `new KTComponent(element, options)` in your custom JavaScript/TypeScript file.
        *   Example (`KTTooltip`):
            ```javascript
            // JS
            const tooltipEl = document.querySelector('#my_tooltip');
            const options = { target: '#my_tooltip_content' };
            const tooltip = new KTTooltip(tooltipEl, options);
            tooltip.show();
            ```
            ```typescript
            // TS (Example - requires importing types)
            import { KTTooltip, KTTooltipInterface, KTTooltipConfigInterface } from '../../core/components/tooltip';
            const tooltipEl: HTMLElement = document.querySelector('#my_tooltip');
            const options: KTTooltipConfigInterface = { target: '#my_tooltip_content' };
            const tooltip: KTTooltipInterface = new KTTooltip(tooltipEl, options);
            tooltip.show();
            ```
*   **TypeScript Support:**
    *   Metronic core components are written in TypeScript.
    *   Interfaces are available for configuration and component instances (e.g., `KTTooltipConfigInterface`, `KTTooltipInterface`).
    *   Custom TypeScript files placed in `src/app/` are compiled by Webpack into `dist/assets/js/app/` (likely as separate files).

### 2.3. Theming & Configuration (Based on Metronic Docs)
*   **Primary Configuration:** Customization is mainly done via `tailwind.config.js`.
*   **Areas:**
    *   **Base Styles:** Customize global settings like colors (gray palette, contextual colors like `primary`, `success`, `warning`, etc.), and box shadows. Modify within `theme.extend.colors` and `theme.extend.boxShadow` in `tailwind.config.js`.
    *   **Components & Layouts:** Specific styles for components and layouts are likely controlled through utility classes defined via Tailwind, potentially using custom theme colors or settings defined in `tailwind.config.js`.
*   **Extending Tailwind:** Use the `theme.extend` section in `tailwind.config.js` to add or override default Tailwind values for:
    *   `fontFamily`
    *   `fontSize`
    *   `colors` (adding new custom colors or shades)
    *   `lineHeight`
    *   `spacing` (margins, padding)
    *   `boxShadow`
    *   `zIndex`
    *   `borderWidth`
    *   `screens` (responsive breakpoints)

### 2.4. Dark Mode (Based on Metronic Docs)
*   **Mechanism:** Uses CSS variables mapped to custom Tailwind colors, allowing automatic dark mode switching without needing separate `dark:` utility classes for most styling.
*   **Initialization Script:** An inline script should be placed early in the `<body>` (or `<head>`) to set the theme mode (`light`, `dark`, or `system`) before rendering.
    *   It checks `localStorage['theme']`, then the `<html>` tag's `data-theme-mode` attribute, then a default variable (`light` by default).
    *   If mode is `system`, it uses `window.matchMedia` to detect OS preference.
    *   It adds the determined mode (`light` or `dark`) as a class to the `<html>` element.
*   **Switching:** The `KTTheme` component (part of `core.bundle.js`) handles theme mode switching via user interaction (e.g., a toggle button), presumably by updating the class on the `<html>` tag and saving the preference to `localStorage`.

### 2.5. RTL Support (Based on Metronic Docs)
*   **Global Setup:** Add `dir="rtl"` attribute to the `<html>` tag.
*   **Method 1 (Default): Logical CSS Properties:** Metronic primarily uses logical properties (e.g., `text-start`, `ps-5` for padding-start) which automatically adjust based on the `dir` attribute. This is the preferred method.
*   **Method 2 (Specific Cases): RTL Modifier:** For exceptions, Tailwind's `rtl:` modifier can be used (e.g., `text-left rtl:text-right`, `pl-5 rtl:pr-5`).

### 2.6. Optimization (Based on Metronic Docs)
*   **Purge CSS (Tailwind):**
    *   Configure the `content` array in `tailwind.config.js` to include paths to all files containing Tailwind classes (e.g., `src/app/**/*.ts`, `src/core/components/**/*.ts`, potentially HTML template files if not using TS exclusively for templates).
    *   This allows Tailwind to remove unused CSS classes during the build, reducing file size.
*   **Minify Assets:**
    *   Run `npm run build:prod`.
    *   This command uses Tailwind CLI with `--minify` for CSS and Webpack (likely with TerserPlugin) to minify the JS bundles.

### 2.7. Metronic Composer (Based on Metronic Docs)
*   **What it is:** An optional tool (HTML file-based mini-CMS built with Python/Flask/Jinja) provided by Metronic.
*   **Purpose:** Helps manage and assemble HTML code from structured partials, blocks, layouts, and page content, simplifying code browsing and extraction, especially for server-side integration.
*   **Features:** Dynamic serving of HTML, code organization, theme API (`theme.layout()`, `theme.block()`, `theme.page()`, `theme.partial()`) for use within Jinja templates.
*   **Relevance:** Primarily useful if generating HTML server-side (like with Flask/Django/PHP) rather than building a pure JS frontend or SPA. Might not be directly needed for our initial Admin/Operator UI setup if we focus on client-side rendering or static HTML+JS, but good to know it exists for managing complex HTML structures. Requires Python/Flask setup to run. 