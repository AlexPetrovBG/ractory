# Metronic Base Components

[Back to Metronic Guide Index](index.md)

---

## 3. Base Components

### 3.1. Accordion (`KTAccordion`)

*   **Description:** A collapsible UI element allowing users to expand/collapse content sections.
*   **HTML Structure:**
    *   Main wrapper `div` with `data-accordion="true"` (or `false` for manual JS init).
    *   Each item wrapper `div` with `data-accordion-item="true"` and a unique `id`.
    *   Toggle `button` with `data-accordion-toggle="#content_id"` targeting the content div ID.
    *   Content `div` with a unique `id` and initially the `hidden` class (unless default open).
*   **Key Data Attributes (on main wrapper `div`):**
    *   `data-accordion="true|false"`: Auto-initialize (`true`) or manual (`false`).
    *   `data-accordion-expand-all="true|false"`: If `true`, allows multiple items to be open simultaneously (default `false`).
    *   `data-accordion-hidden-class="class-name"`: Specifies the class for hidden content (default `"hidden"`).
    *   `data-accordion-active-class="class-name"`: Specifies the class added to the item wrapper when active (default `"active"`).
*   **Key Classes:**
    *   Apply `active` class to an `accordion-item` div to make it open by default.
    *   The `hidden` class (or custom `data-accordion-hidden-class`) is toggled on the content `div`.
*   **JS Initialization:**
    *   **Auto:** Use `data-accordion="true"` on the main wrapper. Global `KTComponents.init()` handles it.
    *   **Manual:** Use `data-accordion="false"`. Instantiate with `new KTAccordion(element, options)`.
*   **JS Options:**
    *   `expandAll` (boolean, default `false`): Corresponds to `data-accordion-expand-all`.
    *   `hiddenClass` (string, default `"hidden"`): Corresponds to `data-accordion-hidden-class`.
    *   `activeClass` (string, default `"active"`): Corresponds to `data-accordion-active-class`.
*   **JS Static Methods:**
    *   `KTAccordion.init()`: Initializes all accordions with `data-accordion="true"`.
    *   `KTAccordion.createInstances()`: Initializes dynamically added accordions.
    *   `KTAccordion.getInstance(element)`: Get instance for a specific element.
    *   `KTAccordion.getOrCreateInstance(element)`: Get or create instance.
*   **JS Instance Methods:**
    *   `show(itemElement)`: Show a specific item.
    *   `hide(itemElement)`: Hide a specific item.
    *   `toggle(itemElement)`: Toggle a specific item.
    *   `getOption(name)`: Get an option value.
    *   `getElement()`: Get the main wrapper DOM element.
    *   `on(eventName, handler)`: Attach event listener.
    *   `off(eventName, eventId)`: Remove event listener.
    *   `dispose()`: Remove instance.
*   **JS Events:**
    *   `show`: Before an item is shown.
    *   `shown`: After an item is shown.
    *   `hide`: Before an item is hidden (can be cancelled by setting `detail.cancel = true` in handler).
    *   `hidden`: After an item is hidden.
    *   `toggle`: Before an item is toggled.

---

### 3.2. Avatar

*   **Description:** A custom avatar component to display user avatar images in various styles with customizable options.
*   **Variants:**
    *   **Default Avatar:** Basic avatar using a standard `img` element with the `rounded-full` class.
        ```html
        <img alt="" class="size-20 rounded-full" src="/assets/media/avatars/300-2.png"/>
        ```
    *   **Background:** Using the avatar image as a background image.
        ```html
        <div class="inline-flex size-20 rounded-full bg-no-repeat bg-cover" 
             style="background-image: url('/assets/media/avatars/300-2.png')">
        </div>
        ```
    *   **Square:** Non-circular avatar using `rounded` instead of `rounded-full`.
        ```html
        <img alt="" class="size-12 rounded" src="/assets/media/avatars/300-2.png"/>
        ```
    *   **Fallback Text:** Text-based avatar for when images aren't available.
        ```html
        <div class="size-20 rounded-full inline-flex items-center justify-center text-2.5xl font-semibold border border-primary-clarity bg-primary-light text-primary">
          A
        </div>
        ```
*   **Key Features:**
    *   **Dot Badge:** Small indicator dot to show status (online/offline).
        ```html
        <div class="relative">
          <img alt="" class="size-20 rounded-full" src="/assets/media/avatars/300-1.png"/>
          <span class="absolute bottom-2 right-2 transform translate-y-1/2 size-2.5 rounded-full ring-2 ring-light bg-success">
          </span>
        </div>
        ```
    *   **Stacked:** Group multiple avatars in a compact, overlapping arrangement.
        ```html
        <div class="inline-flex -space-x-2">
          <img class="hover:z-5 relative size-7.5 shrink-0 rounded-full ring-2 ring-light-light" 
               src="/assets/media/avatars/300-1.png"/>
          <!-- Additional avatars... -->
          <span class="relative inline-flex items-center justify-center size-7.5 shrink-0 text-xs rounded-full ring-2 font-semibold leading-none text-success-inverse ring-success-light bg-success">
            +3
          </span>
        </div>
        ```
    *   **Sizes:** Various size options using Tailwind's size utility classes.
        ```html
        <!-- Examples -->
        <img alt="" class="rounded-full size-10" src="/assets/media/avatars/300-2.png"/>
        <img alt="" class="rounded-full size-14" src="/assets/media/avatars/300-2.png"/>
        <img alt="" class="rounded-full size-20" src="/assets/media/avatars/300-2.png"/>
        ```
*   **Key Classes:**
    *   `size-{value}`: Controls the avatar size (e.g., `size-10`, `size-14`, `size-20`).
    *   `rounded-full`: Creates a circular avatar.
    *   `rounded`: Creates a slightly rounded square avatar.
    *   Color-specific classes for text avatars:
        *   `border-{color}-clarity bg-{color}-light text-{color}`: Styling for text avatars (e.g., `border-primary-clarity bg-primary-light text-primary`).
        *   Available colors: `primary`, `success`, `info`, `danger`, `warning`.
    *   Status indicator classes:
        *   `bg-success`: Online/active status.
        *   `bg-gray-400`: Offline/inactive status.
*   **Usage Notes:**
    *   For responsive designs, use different size classes for different breakpoints (e.g., `size-10 md:size-14 lg:size-20`).
    *   For stacked avatars, adjust the `-space-x-{n}` class to control the overlap amount.
    *   Combine with other Tailwind utility classes for custom styling (borders, shadows, etc.).

---

### 3.3. Badge

*   **Description:** A badge component for highlighting and labeling elements with various styles and indicators. ([Metronic Badge Docs](https://keenthemes.com/metronic/tailwind/docs/components/badge))
*   **Variants:**
    *   **Default Badge:** Basic badge with `.badge` and color variants.
        ```html
        <span class="badge">Default</span>
        <span class="badge badge-primary">Primary</span>
        <span class="badge badge-success">Success</span>
        <span class="badge badge-info">Info</span>
        <span class="badge badge-danger">Danger</span>
        <span class="badge badge-warning">Warning</span>
        <span class="badge badge-dark">Dark</span>
        ```
    *   **Outline:** Use `.badge-outline` for outline style.
        ```html
        <span class="badge badge-outline">Default</span>
        <span class="badge badge-outline badge-primary">Primary</span>
        <span class="badge badge-outline badge-success">Success</span>
        <span class="badge badge-outline badge-info">Info</span>
        <span class="badge badge-outline badge-danger">Danger</span>
        <span class="badge badge-outline badge-warning">Warning</span>
        <span class="badge badge-outline badge-dark">Dark</span>
        ```
    *   **Pill:** Use `.badge-pill` to create pill-shaped badges.
        ```html
        <span class="badge badge-pill badge-primary">Default</span>
        <span class="badge badge-pill badge-outline badge-primary">Outline</span>
        ```
    *   **Sizes:** `.badge-xs`, `.badge-sm`, `.badge-lg` adjust badge size.
        ```html
        <span class="badge badge-xs badge-outline badge-primary">Extra small</span>
        <span class="badge badge-sm badge-outline badge-primary">Small</span>
        <span class="badge badge-outline badge-primary">Default</span>
        <span class="badge badge-lg badge-outline badge-primary">Large</span>
        ```
    *   **With Dot:** Embeds a dot indicator inside a pill badge.
        ```html
        <span class="badge badge-primary badge-pill gap-1.5">
          <span class="badge badge-dot badge-light size-1.5"></span> New
        </span>
        <span class="badge badge-primary badge-pill badge-outline gap-1.5">
          <span class="badge badge-dot badge-primary size-1.5"></span> New
        </span>
        ```
    *   **Dot Only:** Small dot badges without text.
        ```html
        <span class="badge badge-dot size-2.5 badge-primary"></span>
        <span class="badge badge-dot size-2.5 badge-success"></span>
        <span class="badge badge-dot size-2.5 badge-info"></span>
        <span class="badge badge-dot size-2.5 badge-danger"></span>
        <span class="badge badge-dot size-2.5 badge-warning"></span>
        <span class="badge badge-dot size-2.5 badge-dark"></span>
        <span class="badge badge-dot size-2.5 bg-gray-400"></span>
        ```
    *   **Hexagon:** Custom SVG hexagon badge with KeenIcons.
        ```html
        <div class="relative size-[50px] shrink-0">
          <svg class="w-full h-full stroke-primary-clarity fill-primary-light" ...>...</svg>
          <div class="absolute leading-none left-2/4 top-2/4 -translate-y-2/4 -translate-x-2/4">
            <i class="ki-outline ki-abstract-39 text-1.5xl ps-px text-success"></i>
          </div>
        </div>
        ```
*   **Key Classes:**
    *   `badge`, `badge-{color}` (e.g., `badge-primary`, `badge-success`, etc.)
    *   `badge-outline`, `badge-pill`, `badge-dot`
    *   Size modifiers: `badge-xs`, `badge-sm`, `badge-lg`, and `size-{value}` for dot sizes
    *   `gap-{n}` to control spacing when embedding dot indicators
*   **Usage Notes:**
    *   Dot badges are ideal for status indicators (online/offline).
    *   Combine with `.badge-pill` and icons for enhanced labels.
    *   For SVG hexagon badges, maintain aspect ratio with `.relative` and `.size-[px]`.

---

### 3.4. Button

*   **Description:** Versatile button component with various styles, sizes, and icon support for primary and secondary actions. ([Metronic Button Docs](https://keenthemes.com/metronic/tailwind/docs/components/button))
*   **Variants:**
    *   **Default Button:** Basic button with `.btn` and color modifiers.
        ```html
        <button class="btn">Default</button>
        <button class="btn btn-primary">Primary</button>
        <button class="btn btn-success">Success</button>
        <button class="btn btn-info">Info</button>
        <button class="btn btn-danger">Danger</button>
        <button class="btn btn-warning">Warning</button>
        <button class="btn btn-dark">Dark</button>
        ```
    *   **Outline:** Apply `.btn-outline-{color}` for outline styles.
        ```html
        <button class="btn btn-outline-primary">Primary Outline</button>
        <button class="btn btn-outline-success">Success Outline</button>
        ```
    *   **Pill:** Rounded edges using `.btn-pill`.
        ```html
        <button class="btn btn-primary btn-pill">Pill Button</button>
        ```
    *   **Link:** Hyperlink-style button with `.btn-link`.
        ```html
        <button class="btn btn-link">Link Button</button>
        ```
    *   **Icon Button:** Use `.btn-icon` for icon-only buttons.
        ```html
        <button class="btn btn-icon btn-primary">
          <i class="ki-outline ki-add"></i>
        </button>
        ```
    *   **Sizes:** `.btn-xs`, `.btn-sm`, `.btn-lg` to adjust dimensions.
        ```html
        <button class="btn btn-primary btn-sm">Small</button>
        <button class="btn btn-primary btn-lg">Large</button>
        ```
    *   **Block:** Full-width using `.w-full`.
        ```html
        <button class="btn btn-primary w-full">Block Button</button>
        ```
    *   **Disabled:** Add the `disabled` attribute.
        ```html
        <button class="btn btn-primary" disabled>Disabled</button>
        ```
*   **Key Classes:**
    *   `btn`, `btn-{color}`, `btn-outline-{color}`
    *   `btn-pill`, `btn-icon`, `btn-link`
    *   Size modifiers: `btn-xs`, `btn-sm`, `btn-lg`
    *   Utility: `w-full` for block buttons
*   **Usage Notes:**
    *   Place icons (`<i>`) before or after text for mixed button content.
    *   Use `.btn-icon` alone for toolbar actions.
    *   Outline and link buttons are suitable for secondary or tertiary actions.

---

### 3.5. Button Group

*   **Description:** Container for grouping related buttons with cohesive styling and alignment. ([Metronic Button Group Docs](https://keenthemes.com/metronic/tailwind/docs/components/button-group))
*   **HTML Structure:**
    ```html
    <div class="btn-group" role="group">
      <button class="btn btn-primary">Left</button>
      <button class="btn btn-primary">Middle</button>
      <button class="btn btn-primary">Right</button>
    </div>
    ```
*   **Variants:**
    *   **Horizontal Group:** Default inline alignment.
    *   **Vertical Group:** Add `.btn-group-vertical`.
        ```html
        <div class="btn-group btn-group-vertical" role="group">
          <button class="btn btn-primary">Top</button>
          <button class="btn btn-primary">Middle</button>
          <button class="btn btn-primary">Bottom</button>
        </div>
        ```
*   **Key Classes:**
    *   `btn-group`, `btn-group-vertical`
    *   Size modifiers: `btn-group-sm`, `btn-group-lg` (where supported)
*   **Usage Notes:**
    *   Use for segmented controls or action sets.
    *   Include `role="group"` for a11y semantics.
    *   Mix outline and solid buttons within a group if needed.

---

### 3.6. Card

*   **Description:** A flexible content container with header, body, and footer sections for information grouping and layout organization. ([Metronic Card Docs](https://keenthemes.com/metronic/tailwind/docs/components/card))
*   **HTML Structure:**
    ```html
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">Card Title</h3>
      </div>
      <div class="card-body">
        Content goes here...
      </div>
      <div class="card-footer justify-center">
        <a class="btn btn-link" href="#">Example link</a>
      </div>
    </div>
    ```
*   **Variants:**
    *   **Default Card:** Complete card with header, body, and footer.
    *   **Basic Card:** Simple card with just a body section.
        ```html
        <div class="card">
          <div class="card-body">
            Content goes here...
          </div>
        </div>
        ```
    *   **Scrollable Card:** Content area with scrolling capability.
        ```html
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Card Title</h3>
          </div>
          <div class="card-body scrollable h-[200px] py-0 my-4 pr-4 mr-2">
            <div class="mb-4">Content part 1...</div>
            <div>Content part 2...</div>
          </div>
          <div class="card-footer justify-center">
            <a class="btn btn-link" href="#">Example link</a>
          </div>
        </div>
        ```
    *   **Card with Toolbar:** Header with action controls.
        ```html
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Card Title</h3>
            <div class="flex gap-3">
              <label class="switch switch-sm">
                <input checked="" class="order-2" name="check" type="checkbox" value="1"/>
                <span class="switch-label order-1">Auto refresh: On</span>
              </label>
            </div>
          </div>
          <!-- card-body and card-footer -->
        </div>
        ```
    *   **Card with Groups:** Organized content sections.
        ```html
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Card Title</h3>
          </div>
          <div class="card-group">Group content goes here</div>
          <div class="card-group">Group content goes here</div>
          <div class="card-footer justify-center">
            <a class="btn btn-link" href="#">Example link</a>
          </div>
        </div>
        ```
    *   **Card with Table:** Content as a structured table.
        ```html
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Card Title</h3>
          </div>
          <div class="card-table scrollable-x-auto">
            <div class="scrollable-auto">
              <table class="table align-middle text-gray-700 font-medium text-sm">
                <!-- table contents -->
              </table>
            </div>
          </div>
          <div class="card-footer justify-center">
            <a class="btn btn-link" href="#">Example link</a>
          </div>
        </div>
        ```
    *   **Grid Card:** Table with pagination.
        ```html
        <div class="card card-grid">
          <!-- Similar to Card with Table, but adds pagination in footer -->
          <div class="card-footer justify-center md:justify-between flex-col md:flex-row gap-3 text-gray-600 text-2sm font-medium">
            <div class="flex items-center gap-2">
              Show
              <select class="select select-sm w-16" name="perpage">
                <option value="5">5</option>
                <option value="10">10</option>
              </select>
              per page
            </div>
            <div class="flex items-center gap-4">
              <span>1-10 of 52</span>
              <div class="pagination">
                <!-- pagination buttons -->
              </div>
            </div>
          </div>
        </div>
        ```
*   **Key Classes:**
    *   `card`: Main container
    *   `card-header`, `card-body`, `card-footer`: Sectional elements
    *   `card-title`: For header headings
    *   `card-group`: Content group sections
    *   `card-table`: For table content
    *   `scrollable`: For scrollable content
    *   `card-grid`: For card with pagination
    *   Utility modifiers: `card-border`, `card-rounded`, `card-rounded-t`, `card-rounded-b`
*   **Usage Notes:**
    *   Use `justify-center` or other flex utilities on `card-footer` to position footer content.
    *   For responsive layouts, add breakpoint modifiers to flex classes (e.g., `md:justify-between`).
    *   Combine with `scrollable` component for long content sections.

---

### 3.7. Collapse

*   **Description:** A component that toggles the visibility of content, useful for accordion-like structures and showing/hiding information. ([Metronic Collapse Docs](https://keenthemes.com/metronic/tailwind/docs/components/collapse))
*   **HTML Structure:**
    ```html
    <button id="toggle_target" class="btn btn-primary" 
            data-collapse-trigger="true" data-collapse-target="#collapseTarget">
        Toggle Collapse
    </button>
    
    <div id="collapseTarget" data-collapse="true" class="collapse mt-3">
        <div class="bg-light rounded p-5">
            Collapse content here...
        </div>
    </div>
    ```
*   **Key Data Attributes:**
    *   **On trigger element:**
        *   `data-collapse-trigger="true"`: Marks element as a collapse trigger.
        *   `data-collapse-target="#id"`: Target collapse element ID.
        *   `data-collapse-active-class="class"`: Custom class for active state.
    *   **On collapsible element:**
        *   `data-collapse="true|false"`: Enable auto-initialization.
        *   `data-collapse-show="true|false"`: Show on page load (default `false`).
        *   `data-collapse-toggle="true|false"`: If `true`, clicking again collapses it (default `true`).
*   **Key Classes:**
    *   `collapse`: Base class for collapsible element.
    *   `collapse-active`: Applied when content is shown (customizable with `data-collapse-active-class`).
*   **JS Initialization:**
    *   **Auto:** Use `data-collapse="true"` on the collapsible element.
    *   **Manual:** Set `data-collapse="false"` and use JavaScript to initialize:
        ```javascript
        const collapseEl = document.querySelector('#collapseTarget');
        const options = { toggle: true, showOnInit: false };
        const collapse = new KTCollapse(collapseEl, options);
        ```
*   **JS Methods:**
    *   `show()`: Expands the collapse element.
    *   `hide()`: Collapses the element.
    *   `toggle()`: Toggles between show/hide.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `expand`: Before showing (cancelable).
    *   `expanded`: After showing.
    *   `collapse`: Before hiding (cancelable).
    *   `collapsed`: After hiding.
    *   `toggle`: Before toggling.
    *   Event handling example:
        ```javascript
        const collapse = KTCollapse.getInstance(collapseEl);
        collapse.on('collapse', (detail) => {
          detail.cancel = true; // prevent collapse
          console.log('collapse action canceled');
        });
        ```
*   **Usage Notes:**
    *   Multiple triggers can target the same collapse element.
    *   Add styling to the wrapper inside the collapse for visual effects.
    *   Use `data-collapse-show="true"` to have content expanded on load.

---

### 3.8. Container

*   **Description:** A layout component that centers content and applies consistent horizontal padding, with responsive width constraints. ([Metronic Container Docs](https://keenthemes.com/metronic/tailwind/docs/components/container))
*   **HTML Structure:**
    ```html
    <div class="container">
        <!-- Content goes here -->
    </div>
    ```
*   **Variants:**
    *   **Default Container:** Centers content with max-width at various breakpoints.
    *   **Fluid Container:** Full-width container with padding.
        ```html
        <div class="container-fluid">
            <!-- Content goes here -->
        </div>
        ```
    *   **Fixed Container:** Maintains constant width regardless of viewport.
        ```html
        <div class="container-fixed">
            <!-- Content goes here -->
        </div>
        ```
    *   **Breakpoint-Specific:** Fluid until the specified breakpoint.
        ```html
        <div class="container-sm"><!-- Fluid below sm, container above --></div>
        <div class="container-md"><!-- Fluid below md, container above --></div>
        <div class="container-lg"><!-- Fluid below lg, container above --></div>
        <div class="container-xl"><!-- Fluid below xl, container above --></div>
        <div class="container-xxl"><!-- Fluid below xxl, container above --></div>
        ```
*   **Key Classes:**
    *   `container`: Responsive container with max-width at breakpoints
    *   `container-fluid`: 100% width at all breakpoints
    *   `container-fixed`: Fixed-width container regardless of viewport
    *   `container-{breakpoint}`: Fluid until specified breakpoint then contained
*   **Default Breakpoints:**
    *   `sm`: 576px
    *   `md`: 768px
    *   `lg`: 992px
    *   `xl`: 1200px
    *   `xxl`: 1400px
*   **Usage Notes:**
    *   Use `container` for standard responsive layouts.
    *   `container-fluid` works well for full-width sections.
    *   Nest containers for complex layouts, but avoid unnecessary nesting.
    *   Customize container max-widths in `tailwind.config.js` if needed.

---

### 3.9. DataTable

*   **Description:** An enhanced table component with sorting, filtering, pagination, and row selection capabilities for data-heavy interfaces. ([Metronic DataTable Docs](https://keenthemes.com/metronic/tailwind/docs/components/datatable))
*   **HTML Structure:**
    ```html
    <div class="datatable" id="my_datatable" data-datatable="true">
        <div class="datatable-header">
            <!-- Search, filters, etc. -->
            <div class="datatable-search">
                <input type="search" class="form-control" placeholder="Search...">
            </div>
        </div>
        
        <div class="datatable-body">
            <table class="table">
                <thead>
                    <tr>
                        <th data-column-sort="true" data-column-name="name">Name</th>
                        <th data-column-sort="true" data-column-name="position">Position</th>
                        <!-- More headers... -->
                    </tr>
                </thead>
                <tbody>
                    <!-- Table rows populated by DataTable -->
                </tbody>
            </table>
        </div>
        
        <div class="datatable-footer">
            <!-- Pagination controls -->
            <div class="datatable-pagination">
                <!-- Pagination elements -->
            </div>
        </div>
    </div>
    ```
*   **Key Data Attributes:**
    *   `data-datatable="true"`: Enable auto-initialization
    *   `data-datatable-url="/api/data"`: Data source URL (Ajax)
    *   `data-datatable-pagination="true"`: Enable pagination
    *   `data-datatable-page-size="10"`: Rows per page
    *   `data-datatable-page-sizes="[5,10,25,50]"`: Available page sizes
    *   `data-datatable-search="true"`: Enable search input
    *   `data-column-sort="true"`: Enable column sorting
    *   `data-column-name="fieldName"`: Field to sort by
*   **Key Classes:**
    *   `datatable`: Main wrapper container
    *   `datatable-header`, `datatable-body`, `datatable-footer`: Structural sections
    *   `datatable-search`: Search input container
    *   `datatable-pagination`: Pagination controls container
    *   `datatable-info`: Shows info like "Showing 1-10 of 50 entries"
*   **JS Initialization:**
    *   **Auto:** Use `data-datatable="true"` on the wrapper element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const datatableEl = document.querySelector('#my_datatable');
        const options = {
            url: '/api/data',
            pagination: true,
            pageSize: 10,
            pageSizes: [5, 10, 25, 50],
            search: true
        };
        const datatable = new KTDataTable(datatableEl, options);
        ```
*   **JS Methods:**
    *   `load()`: Load/reload data.
    *   `search(query)`: Execute search.
    *   `sort(field, direction)`: Sort by column.
    *   `page(pageIndex)`: Go to specific page.
    *   `selectRow(rowEl)`, `deselectRow(rowEl)`: Selection methods.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `datatable-on-init`: After initialization.
    *   `datatable-on-load`: After data loaded.
    *   `datatable-on-sort`: When sorted.
    *   `datatable-on-search`: When searched.
    *   `datatable-on-page`: When page changed.
    *   `datatable-on-select`: Row selection events.
*   **Usage Notes:**
    *   For simple tables, use `data-datatable-local="true"` to work with HTML table data.
    *   For complex data, configure Ajax loading with `data-datatable-url`.
    *   Customize render functions via JavaScript for advanced cell formatting.
    *   Enable responsive mode with `data-datatable-responsive="true"`.

---

### 3.10. Dismiss

*   **Description:** A utility component to dismiss/close parent elements, commonly used for alerts and notifications. ([Metronic Dismiss Docs](https://keenthemes.com/metronic/tailwind/docs/components/dismiss))
*   **HTML Structure:**
    ```html
    <div class="alert alert-primary">
        <div class="alert-content">
            This is an alert that can be dismissed.
        </div>
        <button class="btn btn-light btn-icon btn-sm ms-auto" data-dismiss="true">×</button>
    </div>
    ```
*   **Key Data Attributes:**
    *   `data-dismiss="true"`: Marks element as a dismiss trigger.
    *   `data-dismiss-target="#id"`: Optional target to dismiss (defaults to parent).
    *   `data-dismiss-effect="fade"`: Animation effect (options: `fade`, `slide`).
    *   `data-dismiss-delay="500"`: Delay in milliseconds before removing element.
*   **Key Classes:**
    *   No specific classes required for the dismiss functionality itself.
    *   Typically used with components like alerts, toasts, or modals.
*   **JS Initialization:**
    *   **Auto:** Use `data-dismiss="true"` on the trigger element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const dismissEl = document.querySelector('#dismiss_button');
        const options = {
            target: '#element_to_dismiss',
            effect: 'fade',
            delay: 500
        };
        const dismiss = new KTDismiss(dismissEl, options);
        ```
*   **JS Methods:**
    *   `dismiss()`: Programmatically dismiss the target element.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `dismiss`: Before the element is dismissed (cancelable).
    *   `dismissed`: After the element is dismissed.
    *   Event handling example:
        ```javascript
        const dismiss = KTDismiss.getInstance(dismissEl);
        dismiss.on('dismiss', (detail) => {
          detail.cancel = true; // prevent dismissal
          console.log('dismiss action canceled');
        });
        ```
*   **Usage Notes:**
    *   Position the dismiss button appropriately with utility classes (e.g., `ms-auto` for right alignment).
    *   For custom dismiss buttons, style as needed but keep the `data-dismiss="true"` attribute.
    *   Common use: alerts, toasts, modals, popups, and other temporary UI elements.

---

### 3.11. Drawer

*   **Description:** A sliding panel that appears from the edge of the screen, providing supplementary content or navigation without leaving the current page. ([Metronic Drawer Docs](https://keenthemes.com/metronic/tailwind/docs/components/drawer))
*   **HTML Structure:**
    ```html
    <!-- Trigger button -->
    <button id="drawer_trigger" class="btn btn-primary" 
            data-drawer-trigger="true" data-drawer-target="#my_drawer">
        Open Drawer
    </button>
    
    <!-- Drawer element -->
    <div id="my_drawer" class="drawer" data-drawer="true">
        <div class="drawer-overlay" data-drawer-dismiss="true"></div>
        <div class="drawer-content bg-light">
            <div class="drawer-header">
                <h3 class="drawer-title">Drawer Title</h3>
                <div class="drawer-toolbar">
                    <button class="btn btn-icon btn-light" data-drawer-dismiss="true">×</button>
                </div>
            </div>
            <div class="drawer-body">
                <!-- Drawer content here -->
                Drawer content goes here...
            </div>
            <div class="drawer-footer">
                <button class="btn btn-primary">Submit</button>
                <button class="btn btn-light" data-drawer-dismiss="true">Cancel</button>
            </div>
        </div>
    </div>
    ```
*   **Key Data Attributes:**
    *   **On trigger element:**
        *   `data-drawer-trigger="true"`: Marks element as a drawer trigger.
        *   `data-drawer-target="#id"`: Target drawer element ID.
    *   **On drawer element:**
        *   `data-drawer="true"`: Enable auto-initialization.
        *   `data-drawer-direction="end"`: Direction (options: `start`, `end`, `top`, `bottom`, default: `end`).
        *   `data-drawer-overlay="true"`: Show overlay (default: `true`).
        *   `data-drawer-permanent-breakpoint="lg"`: Convert to permanent at breakpoint (options: `sm`, `md`, `lg`, `xl`, `xxl`).
    *   **On dismissal elements:**
        *   `data-drawer-dismiss="true"`: Marks elements that close the drawer when clicked.
*   **Key Classes:**
    *   `drawer`: Main wrapper container.
    *   `drawer-overlay`: Background overlay that covers the page.
    *   `drawer-content`: Container for drawer's content.
    *   `drawer-header`, `drawer-body`, `drawer-footer`: Structural sections.
    *   `drawer-title`: Title element.
    *   `drawer-toolbar`: Container for actions in header.
*   **JS Initialization:**
    *   **Auto:** Use `data-drawer="true"` on the drawer element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const drawerEl = document.querySelector('#my_drawer');
        const options = {
            direction: 'end',
            overlay: true,
            closeButton: true,
            permanentBreakpoint: 'lg'
        };
        const drawer = new KTDrawer(drawerEl, options);
        ```
*   **JS Methods:**
    *   `show()`: Open the drawer.
    *   `hide()`: Close the drawer.
    *   `toggle()`: Toggle drawer visibility.
    *   `update()`: Update drawer layout after content changes.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `show`: Before drawer is shown (cancelable).
    *   `shown`: After drawer is fully shown.
    *   `hide`: Before drawer is hidden (cancelable).
    *   `hidden`: After drawer is fully hidden.
    *   Event handling example:
        ```javascript
        const drawer = KTDrawer.getInstance(drawerEl);
        drawer.on('show', (detail) => {
          console.log('drawer is about to show');
        });
        ```
*   **Usage Notes:**
    *   Use `drawer-direction-{position}` classes for directional styling.
    *   At `permanentBreakpoint` and above, drawer becomes permanently visible (sidebar mode).
    *   For mobile-friendly drawers, consider `direction: 'end'` or `'start'` with full height.
    *   Use with `scrollable` component if drawer content is lengthy.

---

### 3.12. Dropdown

*   **Description:** A versatile component that displays overlay content like menus, providing a layered navigation experience without leaving the current page. ([Metronic Dropdown Docs](https://keenthemes.com/metronic/tailwind/docs/components/dropdown))
*   **HTML Structure:**
    ```html
    <div class="dropdown" data-dropdown="true" data-dropdown-trigger="click">
      <button class="dropdown-toggle btn btn-light">
        Show Dropdown
      </button>
      <div class="dropdown-content w-full max-w-56 p-4">
        Dropdown content goes here...
      </div>
    </div>
    ```
*   **Variants:**
    *   **Basic Dropdown:** Simple dropdown toggled by a button.
    *   **With Arrow Indicator:** Animated arrow showing open/closed state.
        ```html
        <div class="dropdown" data-dropdown="true" data-dropdown-trigger="click">
          <button class="dropdown-toggle btn btn-light btn-icon-xs">
            Show Dropdown
            <i class="ki-outline ki-down dropdown-open:hidden"></i>
            <i class="ki-outline ki-up hidden dropdown-open:block"></i>
          </button>
          <div class="dropdown-content w-full max-w-56 p-4">
            Dropdown content goes here...
          </div>
        </div>
        ```
    *   **With Menu:** Dropdown containing a navigation menu.
        ```html
        <div class="dropdown" data-dropdown="true" data-dropdown-trigger="click">
          <button class="dropdown-toggle btn btn-light">
            Show Dropdown
          </button>
          <div class="dropdown-content w-full max-w-56 py-2">
            <div class="menu menu-default flex flex-col w-full">
              <div class="menu-item">
                <a class="menu-link" href="#">
                  <span class="menu-icon"><i class="ki-outline ki-badge"></i></span>
                  <span class="menu-title">Menu item 1</span>
                </a>
              </div>
              <!-- More menu items... -->
            </div>
          </div>
        </div>
        ```
    *   **With Separators:** Sections separated by dividers.
        ```html
        <div class="dropdown" data-dropdown="true" data-dropdown-trigger="click">
          <button class="dropdown-toggle btn btn-light">
            Show Dropdown
          </button>
          <div class="dropdown-content w-full max-w-56">
            <div class="p-4 text-sm text-gray-900 font-medium">Dropdown Heading</div>
            <div class="border-b border-b-gray-200"></div>
            <div class="p-4">Content section 1...</div>
            <div class="border-b border-b-gray-200"></div>
            <div class="p-4">Content section 2...</div>
          </div>
        </div>
        ```
    *   **Scrollable Content:** Dropdown with scrolling capabilities.
        ```html
        <div class="dropdown" data-dropdown="true" data-dropdown-trigger="click">
          <button class="dropdown-toggle btn btn-light">
            Show Dropdown
          </button>
          <div class="dropdown-content w-full max-w-56">
            <div class="p-4 text-sm text-gray-900 font-medium">Dropdown Heading</div>
            <div class="border-b border-b-gray-200"></div>
            <div class="scrollable-y m-2 p-2 h-[150px]">
              Long content that will scroll...
            </div>
          </div>
        </div>
        ```
*   **Key Data Attributes:**
    *   `data-dropdown="true"`: Enable auto-initialization.
    *   `data-dropdown-trigger="click|hover"`: Trigger method (default: `click`).
    *   `data-dropdown-placement="bottom-start"`: Position relative to toggle (options: `top-start`, `top`, `top-end`, `right-start`, `right`, `right-end`, `bottom-start`, `bottom`, `bottom-end`, `left-start`, `left`, `left-end`).
    *   `data-dropdown-offset="0,0"`: X,Y offset in pixels.
    *   `data-dropdown-dismiss="true"`: When added to dropdown content, closes dropdown on click.
    *   `data-dropdown-permanent="true"`: Prevents dropdown from being closed by outside clicks.
*   **Key Classes:**
    *   `dropdown`: Main container.
    *   `dropdown-toggle`: Toggle element that shows/hides dropdown.
    *   `dropdown-content`: Container for dropdown content.
    *   `dropdown-open:block`, `dropdown-open:hidden`: Utility classes for toggle state.
*   **JS Initialization:**
    *   **Auto:** Use `data-dropdown="true"` on the main element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const dropdownEl = document.querySelector('#my_dropdown');
        const options = {
          trigger: 'click',
          placement: 'bottom-start',
          offset: [0, 0]
        };
        const dropdown = new KTDropdown(dropdownEl, options);
        ```
*   **JS Methods:**
    *   `show()`: Open the dropdown.
    *   `hide()`: Close the dropdown.
    *   `toggle()`: Toggle dropdown visibility.
    *   `getToggleElement()`: Get toggle element.
    *   `disable()`, `enable()`: Manage dropdown state.
    *   `isOpen()`: Check if dropdown is open.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `show`: Before dropdown is shown (cancelable).
    *   `shown`: After dropdown is shown.
    *   `hide`: Before dropdown is hidden (cancelable).
    *   `hidden`: After dropdown is hidden.
*   **Usage Notes:**
    *   Combine with the Menu component for navigation dropdowns.
    *   Use `max-w-{size}` to control dropdown width.
    *   For long content, combine with the Scrollable component.
    *   Custom dropdown positioning with `data-dropdown-placement`.

---

### 3.13. Modal

*   **Description:** A dialog component that displays content in a layer over the page, requiring user interaction before returning to the main interface. ([Metronic Modal Docs](https://keenthemes.com/metronic/tailwind/docs/components/modal))
*   **HTML Structure:**
    ```html
    <!-- Trigger button -->
    <button class="btn btn-primary" data-modal-trigger="true" data-modal-target="#my_modal">
      Open Modal
    </button>
    
    <!-- Modal element -->
    <div id="my_modal" class="modal" data-modal="true">
      <div class="modal-overlay" data-modal-dismiss="true"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">Modal Title</h3>
          <div class="modal-toolbar">
            <button class="btn btn-icon btn-sm btn-light" data-modal-dismiss="true">×</button>
          </div>
        </div>
        <div class="modal-body">
          Modal content goes here...
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary">Save</button>
          <button class="btn btn-light" data-modal-dismiss="true">Cancel</button>
        </div>
      </div>
    </div>
    ```
*   **Variants:**
    *   **Default Modal:** Standard centered dialog.
    *   **Size Variants:** Use size modifiers for different dimensions.
        ```html
        <div id="sm_modal" class="modal" data-modal="true" data-modal-size="sm">
          <!-- Modal content -->
        </div>
        
        <div id="lg_modal" class="modal" data-modal="true" data-modal-size="lg">
          <!-- Modal content -->
        </div>
        
        <div id="xl_modal" class="modal" data-modal="true" data-modal-size="xl">
          <!-- Modal content -->
        </div>
        ```
    *   **Fullscreen Modal:** Covers the entire viewport.
        ```html
        <div id="fs_modal" class="modal" data-modal="true" data-modal-size="fullscreen">
          <!-- Modal content -->
        </div>
        ```
    *   **Scrollable Content:** For lengthy modal content.
        ```html
        <div id="scroll_modal" class="modal" data-modal="true">
          <div class="modal-overlay" data-modal-dismiss="true"></div>
          <div class="modal-content">
            <div class="modal-header">
              <!-- Header content -->
            </div>
            <div class="modal-body scrollable-y">
              <!-- Long scrollable content -->
            </div>
            <div class="modal-footer">
              <!-- Footer content -->
            </div>
          </div>
        </div>
        ```
    *   **Static Backdrop:** Prevents closing on backdrop click.
        ```html
        <div id="static_modal" class="modal" data-modal="true" data-modal-static="true">
          <!-- Modal content -->
        </div>
        ```
*   **Key Data Attributes:**
    *   **On trigger element:**
        *   `data-modal-trigger="true"`: Marks element as a modal trigger.
        *   `data-modal-target="#id"`: Target modal element ID.
    *   **On modal element:**
        *   `data-modal="true"`: Enable auto-initialization.
        *   `data-modal-size="sm|md|lg|xl|fullscreen"`: Size variant (default: `md`).
        *   `data-modal-static="true"`: Prevent closing on backdrop click or escape key.
        *   `data-modal-overlay="true"`: Show backdrop overlay (default: `true`).
        *   `data-modal-placement="center|top"`: Vertical alignment (default: `center`).
    *   **On dismissal elements:**
        *   `data-modal-dismiss="true"`: Marks elements that close the modal when clicked.
*   **Key Classes:**
    *   `modal`: Main wrapper container.
    *   `modal-overlay`: Background overlay that covers the page.
    *   `modal-content`: Container for modal's content.
    *   `modal-header`, `modal-body`, `modal-footer`: Structural sections.
    *   `modal-title`: Title element.
    *   `modal-toolbar`: Container for actions in header.
*   **JS Initialization:**
    *   **Auto:** Use `data-modal="true"` on the modal element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const modalEl = document.querySelector('#my_modal');
        const options = {
          size: 'md',
          placement: 'center',
          static: false,
          overlay: true
        };
        const modal = new KTModal(modalEl, options);
        ```
*   **JS Methods:**
    *   `show()`: Display the modal.
    *   `hide()`: Close the modal.
    *   `toggle()`: Toggle modal visibility.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `show`: Before modal is shown (cancelable).
    *   `shown`: After modal is shown.
    *   `hide`: Before modal is hidden (cancelable).
    *   `hidden`: After modal is hidden.
*   **Usage Notes:**
    *   Modal header and footer are optional; can use just the body.
    *   For long content, add the `scrollable-y` class to the modal body.
    *   Add unique IDs to modals when using multiple on the same page.
    *   Place modals at the end of the document body for proper stacking.

---

### 3.14. Progress

*   **Description:** A visual indicator showing the completion status of a task or process, with various styles and animations. ([Metronic Progress Docs](https://keenthemes.com/metronic/tailwind/docs/components/progress))
*   **HTML Structure:**
    ```html
    <!-- Basic Progress Bar -->
    <div class="progress h-4">
      <div class="progress-bar" role="progressbar" style="width: 75%" 
           aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
    </div>
    ```
*   **Variants:**
    *   **Default Progress:** Basic horizontal progress bar.
    *   **Color Variants:** Different contextual colors.
        ```html
        <div class="progress h-4">
          <div class="progress-bar bg-primary" style="width: 25%"></div>
        </div>
        <div class="progress h-4">
          <div class="progress-bar bg-success" style="width: 50%"></div>
        </div>
        <div class="progress h-4">
          <div class="progress-bar bg-info" style="width: 75%"></div>
        </div>
        <div class="progress h-4">
          <div class="progress-bar bg-danger" style="width: 100%"></div>
        </div>
        ```
    *   **Striped Progress:** Adds diagonal stripes for emphasis.
        ```html
        <div class="progress h-4">
          <div class="progress-bar bg-primary progress-bar-striped" style="width: 50%"></div>
        </div>
        ```
    *   **Animated Stripes:** Animated diagonal stripes.
        ```html
        <div class="progress h-4">
          <div class="progress-bar bg-primary progress-bar-striped progress-bar-animated" 
               style="width: 50%"></div>
        </div>
        ```
    *   **With Label:** Text inside the progress bar.
        ```html
        <div class="progress h-6">
          <div class="progress-bar bg-primary" style="width: 75%">
            75%
          </div>
        </div>
        ```
    *   **Multiple Bars:** Combined progress segments.
        ```html
        <div class="progress h-4">
          <div class="progress-bar bg-success" style="width: 30%"></div>
          <div class="progress-bar bg-info" style="width: 20%"></div>
          <div class="progress-bar bg-danger" style="width: 15%"></div>
        </div>
        ```
    *   **Custom Height:** Size variants.
        ```html
        <div class="progress h-1">
          <div class="progress-bar bg-primary" style="width: 75%"></div>
        </div>
        <div class="progress h-3">
          <div class="progress-bar bg-primary" style="width: 75%"></div>
        </div>
        <div class="progress h-6">
          <div class="progress-bar bg-primary" style="width: 75%"></div>
        </div>
        ```
*   **Key Classes:**
    *   `progress`: Container element.
    *   `progress-bar`: The actual progress indicator.
    *   `h-{size}`: Progress height (e.g., `h-1`, `h-4`, `h-6`).
    *   `bg-{color}`: Color variants (e.g., `bg-primary`, `bg-success`).
    *   `progress-bar-striped`: Adds diagonal stripes.
    *   `progress-bar-animated`: Animates the stripes.
*   **ARIA Attributes:**
    *   `role="progressbar"`: Semantic role.
    *   `aria-valuenow`: Current value.
    *   `aria-valuemin`: Minimum value (typically 0).
    *   `aria-valuemax`: Maximum value (typically 100).
*   **JS Integration:**
    *   Progress bars are typically static HTML, but can be dynamically updated:
        ```javascript
        // Update progress value
        const progressBar = document.querySelector('.progress-bar');
        progressBar.style.width = '60%';
        progressBar.setAttribute('aria-valuenow', 60);
        ```
*   **Usage Notes:**
    *   Set width using inline style or Tailwind width utilities (e.g., `w-1/4` for 25%).
    *   Add sufficient height (minimum `h-3`) if including text inside the bar.
    *   For responsive progress, use percent-based widths.
    *   Add appropriate ARIA attributes for accessibility.

---

### 3.15. Rating

*   **Description:** An interactive component for collecting user feedback through star ratings, with customizable visuals and behavior. ([Metronic Rating Docs](https://keenthemes.com/metronic/tailwind/docs/components/rating))
*   **HTML Structure:**
    ```html
    <div class="rating" data-rating="true" data-rating-value="3">
      <div class="rating-items">
        <span class="rating-item" data-rating-value="1"></span>
        <span class="rating-item" data-rating-value="2"></span>
        <span class="rating-item" data-rating-value="3"></span>
        <span class="rating-item" data-rating-value="4"></span>
        <span class="rating-item" data-rating-value="5"></span>
      </div>
      <div class="rating-input">
        <input type="hidden" name="rating" value="3">
      </div>
    </div>
    ```
*   **Variants:**
    *   **Default Rating:** Basic five-star rating.
    *   **Custom Initial Value:** Set with `data-rating-value`.
        ```html
        <div class="rating" data-rating="true" data-rating-value="4">
          <!-- Rating items -->
        </div>
        ```
    *   **Read-Only Mode:** Non-interactive display.
        ```html
        <div class="rating" data-rating="true" data-rating-value="3" data-rating-readonly="true">
          <!-- Rating items -->
        </div>
        ```
    *   **Custom Icons:** Using SVG or other icon libraries.
        ```html
        <div class="rating" data-rating="true" data-rating-value="3" 
             data-rating-icon-default="ki-outline ki-star"
             data-rating-icon-active="ki-solid ki-star">
          <!-- Rating items -->
        </div>
        ```
    *   **Color Variants:** Custom colors for the rating stars.
        ```html
        <div class="rating" data-rating="true" data-rating-value="3" 
             data-rating-color-default="text-gray-400"
             data-rating-color-active="text-warning">
          <!-- Rating items -->
        </div>
        ```
    *   **Size Variants:** Different sizes for the rating stars.
        ```html
        <div class="rating rating-sm" data-rating="true" data-rating-value="3">
          <!-- Rating items -->
        </div>
        <div class="rating rating-md" data-rating="true" data-rating-value="3">
          <!-- Rating items -->
        </div>
        <div class="rating rating-lg" data-rating="true" data-rating-value="3">
          <!-- Rating items -->
        </div>
        ```
*   **Key Data Attributes:**
    *   `data-rating="true"`: Enable auto-initialization.
    *   `data-rating-value="3"`: Initial rating value.
    *   `data-rating-min="1"`: Minimum value (default: `1`).
    *   `data-rating-max="5"`: Maximum value (default: `5`).
    *   `data-rating-readonly="true|false"`: Set to read-only mode (default: `false`).
    *   `data-rating-icon-default="class"`: CSS class for default state.
    *   `data-rating-icon-active="class"`: CSS class for active state.
    *   `data-rating-color-default="class"`: CSS class for default color.
    *   `data-rating-color-active="class"`: CSS class for active color.
*   **Key Classes:**
    *   `rating`: Main container.
    *   `rating-items`: Container for rating items.
    *   `rating-item`: Individual rating item.
    *   `rating-input`: Container for hidden input.
    *   Size modifiers: `rating-sm`, `rating-md`, `rating-lg`.
*   **JS Initialization:**
    *   **Auto:** Use `data-rating="true"` on the main element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const ratingEl = document.querySelector('#my_rating');
        const options = {
          min: 1,
          max: 5,
          value: 3,
          readonly: false,
          iconDefault: 'ki-outline ki-star',
          iconActive: 'ki-solid ki-star',
          colorDefault: 'text-gray-400',
          colorActive: 'text-warning'
        };
        const rating = new KTRating(ratingEl, options);
        ```
*   **JS Methods:**
    *   `getValue()`: Get current rating value.
    *   `setValue(value)`: Set rating value.
    *   `enable()`, `disable()`: Enable/disable interaction.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `rating-change`: When rating value changes.
    *   Event handling example:
        ```javascript
        const rating = KTRating.getInstance(ratingEl);
        rating.on('rating-change', (detail) => {
          console.log('New rating:', detail.value);
        });
        ```
*   **Usage Notes:**
    *   Always include hidden input for form submissions.
    *   Custom icons can use any icon library (e.g., KeenIcons, FontAwesome).
    *   Use read-only mode for displaying existing ratings.
    *   Adjust spacing with margin/padding utilities.

---

### 3.16. Reparent

*   **Description:** A utility component that dynamically moves DOM elements to different parent containers based on viewport size, enabling responsive layouts without duplicating content. ([Metronic Reparent Docs](https://keenthemes.com/metronic/tailwind/docs/components/reparent))
*   **HTML Structure:**
    ```html
    <!-- Source element -->
    <div id="source_parent" class="card">
      <div class="card-header">Source Container</div>
      <div class="card-body">
        <!-- Element to be moved -->
        <div id="reparent_element" data-reparent="true" 
             data-reparent-target="#target_parent" 
             data-reparent-breakpoint="lg" 
             data-reparent-animation="fade">
          This content will move to the target at the lg breakpoint
        </div>
        
        <!-- Other content that stays -->
        <div>This content remains in the source</div>
      </div>
    </div>
    
    <!-- Target container -->
    <div id="target_parent" class="card mt-5">
      <div class="card-header">Target Container</div>
      <div class="card-body">
        Initial target content
        <!-- Reparented element will appear here at lg breakpoint -->
      </div>
    </div>
    ```
*   **Key Data Attributes:**
    *   `data-reparent="true"`: Enable auto-initialization.
    *   `data-reparent-target="#id"`: Target container selector.
    *   `data-reparent-breakpoint="lg"`: Viewport breakpoint when reparenting occurs (options: `xs`, `sm`, `md`, `lg`, `xl`, `xxl`).
    *   `data-reparent-animation="none|fade"`: Animation effect (default: `none`).
    *   `data-reparent-placement="append|prepend"`: Placement within target (default: `append`).
*   **JS Initialization:**
    *   **Auto:** Use `data-reparent="true"` on the element to be moved.
    *   **Manual:** Use JavaScript:
        ```javascript
        const reparentEl = document.querySelector('#reparent_element');
        const options = {
          target: '#target_parent',
          breakpoint: 'lg',
          animation: 'fade',
          placement: 'append'
        };
        const reparent = new KTReparent(reparentEl, options);
        ```
*   **JS Methods:**
    *   `move()`: Manually trigger the move to target.
    *   `reset()`: Move element back to original position.
    *   `update()`: Update based on current viewport.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `reparent`: Before element is moved (cancelable).
    *   `reparented`: After element is moved.
    *   `reset`: Before element is moved back (cancelable).
    *   `resetted`: After element is moved back.
*   **Breakpoint Values:**
    *   `xs`: 0px and up
    *   `sm`: 576px and up
    *   `md`: 768px and up
    *   `lg`: 992px and up
    *   `xl`: 1200px and up
    *   `xxl`: 1400px and up
*   **Usage Notes:**
    *   Great for responsive designs without duplicating content.
    *   Common uses: moving sidebar content to a dropdown on mobile.
    *   Use `overflow: hidden` on containers for clean fade animations.
    *   Multiple elements can target the same container with different breakpoints.

---

### 3.17. Scrollable

*   **Description:** Enhances scrollable areas with custom styling, keeping scrollbars consistent across browsers and providing additional functionality like tracking scroll position. ([Metronic Scrollable Docs](https://keenthemes.com/metronic/tailwind/docs/components/scrollable))
*   **HTML Structure:**
    ```html
    <!-- Vertical scrolling -->
    <div class="scrollable-y h-[300px]" data-scrollable="true">
      <!-- Content that overflows the container height -->
      Long vertical content goes here...
    </div>
    
    <!-- Horizontal scrolling -->
    <div class="scrollable-x w-[300px]" data-scrollable="true">
      <!-- Content that overflows the container width -->
      <div class="min-w-[500px]">
        Long horizontal content goes here...
      </div>
    </div>
    
    <!-- Both directions -->
    <div class="scrollable h-[300px] w-[300px]" data-scrollable="true">
      <!-- Content that overflows in both dimensions -->
      <div class="min-w-[500px] min-h-[500px]">
        Content that requires scrolling in both directions...
      </div>
    </div>
    ```
*   **Variants:**
    *   **Vertical Scrolling:** Use `.scrollable-y` for vertical-only scrollbars.
    *   **Horizontal Scrolling:** Use `.scrollable-x` for horizontal-only scrollbars.
    *   **Both Directions:** Use `.scrollable` for both vertical and horizontal scrollbars.
    *   **With Overlay Scrollbars:** Modern look with overlay scrollbars.
        ```html
        <div class="scrollable-y scrollable-overlay h-[300px]" data-scrollable="true">
          <!-- Scrollable content -->
        </div>
        ```
    *   **Visible Scrollbars:** Always visible scrollbars.
        ```html
        <div class="scrollable-y scrollable-visible h-[300px]" data-scrollable="true">
          <!-- Scrollable content -->
        </div>
        ```
    *   **Auto Mode:** Scrollbars appear only when needed.
        ```html
        <div class="scrollable-auto h-[300px]" data-scrollable="true">
          <!-- Scrollable content (may or may not overflow) -->
        </div>
        ```
*   **Key Data Attributes:**
    *   `data-scrollable="true"`: Enable auto-initialization.
    *   `data-scrollable-always-visible="true|false"`: Scrollbars always visible (default: `false`).
    *   `data-scrollable-height="300px"`: Container height (alternative to CSS).
    *   `data-scrollable-width="300px"`: Container width (alternative to CSS).
    *   `data-scrollable-x="true|false"`: Enable horizontal scrolling (default: `true` for `.scrollable` and `.scrollable-x`).
    *   `data-scrollable-y="true|false"`: Enable vertical scrolling (default: `true` for `.scrollable` and `.scrollable-y`).
*   **Key Classes:**
    *   `scrollable`: Both vertical and horizontal scrolling.
    *   `scrollable-y`: Vertical scrolling only.
    *   `scrollable-x`: Horizontal scrolling only.
    *   `scrollable-auto`: Scrollbars appear only when needed.
    *   `scrollable-overlay`: Modern overlay scrollbars.
    *   `scrollable-visible`: Always visible scrollbars.
*   **JS Initialization:**
    *   **Auto:** Use `data-scrollable="true"` on the element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const scrollableEl = document.querySelector('#my_scrollable');
        const options = {
          height: '300px',
          width: 'auto',
          alwaysVisible: false,
          scrollX: true,
          scrollY: true
        };
        const scrollable = new KTScrollable(scrollableEl, options);
        ```
*   **JS Methods:**
    *   `update()`: Recalculate scrollbars after content changes.
    *   `scroll(top, left)`: Scroll to specific position.
    *   `scrollTop(value)`: Scroll vertically to position.
    *   `scrollLeft(value)`: Scroll horizontally to position.
    *   `getScrollTop()`, `getScrollLeft()`: Get current scroll position.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `scroll`: When scrolling occurs.
    *   `update`: After scrollbars are updated.
*   **Usage Notes:**
    *   Always specify container dimensions with height/width.
    *   Use Tailwind's `h-[size]` and `w-[size]` utilities for custom dimensions.
    *   For dynamic content, call `update()` after content changes.
    *   Combine with other components like Modals, Drawers, or Cards.
    *   For tables, wrap with `.scrollable-x-auto` for responsive behavior.

---

### 3.18. Table

*   **Description:** A flexible component for displaying data in a tabular format, with various styling options and customization capabilities. ([Metronic Table Docs](https://keenthemes.com/metronic/tailwind/docs/components/table))
*   **HTML Structure:**
    ```html
    <table class="table align-middle text-gray-700 font-medium text-sm">
      <thead>
        <tr>
          <th>Customer</th>
          <th>Order Amount</th>
          <th>Order Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Customer 1</td>
          <td>$100.00</td>
          <td>5 Jan, 2024</td>
          <td>Pending</td>
        </tr>
        <!-- Additional rows... -->
      </tbody>
    </table>
    ```
*   **Variants:**
    *   **Default Table:** Basic table with clean styling.
    *   **Card Table:** Table integrated into a card component.
        ```html
        <div class="card min-w-full">
          <div class="card-table">
            <table class="table align-middle text-gray-700 font-medium text-sm">
              <!-- Table content -->
            </table>
          </div>
        </div>
        ```
    *   **With Heading:** Card table with a header title.
        ```html
        <div class="card min-w-full">
          <div class="card-header">
            <h3 class="card-title">Latest Orders</h3>
          </div>
          <div class="card-table">
            <table class="table align-middle text-gray-700 font-medium text-sm">
              <!-- Table content -->
            </table>
          </div>
        </div>
        ```
    *   **Bordered:** Table with cell borders.
        ```html
        <table class="table table-border align-middle text-gray-700 font-medium text-sm">
          <!-- Table content -->
        </table>
        ```
    *   **Horizontal Scroll:** For tables with many columns.
        ```html
        <div class="scrollable-x-auto">
          <div class="scrollable-auto">
            <table class="table align-middle text-gray-700 font-medium text-sm">
              <!-- Table content with many columns -->
            </table>
          </div>
        </div>
        ```
    *   **Sortable Columns:** Interactive column sorting.
        ```html
        <table class="table align-middle text-gray-700 font-medium text-sm">
          <thead>
            <tr>
              <th data-column-sort="true" data-column-name="customer">Customer</th>
              <th data-column-sort="true" data-column-name="amount">Order Amount</th>
              <!-- More sortable headers -->
            </tr>
          </thead>
          <tbody>
            <!-- Table rows -->
          </tbody>
        </table>
        ```
    *   **With Row Selection:** Checkboxes for selecting rows.
        ```html
        <table class="table align-middle text-gray-700 font-medium text-sm">
          <thead>
            <tr>
              <th>
                <input class="checkbox checkbox-sm" data-datatable-check-all="true" type="checkbox"/>
              </th>
              <!-- Other headers -->
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <input class="checkbox checkbox-sm" data-datatable-row-check="true" type="checkbox" value="1"/>
              </td>
              <!-- Other cells -->
            </tr>
            <!-- More rows -->
          </tbody>
        </table>
        ```
*   **Key Classes:**
    *   `table`: Basic table styling.
    *   `table-border`: Adds borders to cells.
    *   `table-row-border`: Adds borders only between rows.
    *   `table-col-border`: Adds borders only between columns.
    *   `table-sm`, `table-md`, `table-lg`: Size variants.
    *   `table-hover`: Highlight rows on hover.
    *   `table-striped`: Alternate row background colors.
*   **Integration with Card:**
    *   Place table inside `card-table` div to properly integrate with Card component.
    *   Can combine with card header, footer, and other card features.
*   **Integration with DataTable:**
    *   Enhance with DataTable component for sorting, filtering, and pagination.
    *   Add a grid footer with pagination:
        ```html
        <div class="card-footer justify-center md:justify-between flex-col md:flex-row gap-3">
          <div class="flex items-center gap-2">
            Show
            <select class="select select-sm w-16" name="perpage">
              <option value="5">5</option>
              <option value="10">10</option>
            </select>
            per page
          </div>
          <div class="flex items-center gap-4">
            <span>1-10 of 52</span>
            <div class="pagination">
              <!-- Pagination buttons -->
            </div>
          </div>
        </div>
        ```
*   **Key Data Attributes (when used with DataTable):**
    *   `data-column-sort="true"`: Enable column sorting.
    *   `data-column-name="field"`: Field name for sorting.
    *   `data-datatable-check-all="true"`: Header checkbox to select all rows.
    *   `data-datatable-row-check="true"`: Individual row checkbox.
*   **Usage Notes:**
    *   Combine with Scrollable component for tables with many columns or rows.
    *   Use `align-middle` to vertically center cell content.
    *   For responsive tables, wrap in `scrollable-x-auto` container.
    *   For data-heavy tables, consider the DataTable component instead.

---

### 3.19. Theme

*   **Description:** A utility component for managing theme mode (light/dark) with persistent settings and system preference detection. ([Metronic Theme Docs](https://keenthemes.com/metronic/tailwind/docs/components/theme))
*   **HTML Structure:**
    ```html
    <!-- Theme toggle button -->
    <button class="btn" data-theme-toggle="true">
      <i class="ki-outline ki-night-day"></i> Toggle Theme
    </button>
    
    <!-- Theme mode selector -->
    <div class="menu menu-default">
      <div class="menu-item">
        <a class="menu-link active" data-theme-mode="light" href="#">
          <span class="menu-icon">
            <i class="ki-outline ki-sun"></i>
          </span>
          <span class="menu-title">Light</span>
        </a>
      </div>
      <div class="menu-item">
        <a class="menu-link" data-theme-mode="dark" href="#">
          <span class="menu-icon">
            <i class="ki-outline ki-moon"></i>
          </span>
          <span class="menu-title">Dark</span>
        </a>
      </div>
      <div class="menu-item">
        <a class="menu-link" data-theme-mode="system" href="#">
          <span class="menu-icon">
            <i class="ki-outline ki-screen"></i>
          </span>
          <span class="menu-title">System</span>
        </a>
      </div>
    </div>
    ```
*   **Initialization Script (include early in `<head>` or `<body>`):**
    ```html
    <script>
      // Theme mode setup
      var mode = localStorage['theme'] || document.documentElement.getAttribute('data-theme-mode') || 'light';
      
      if (mode === 'system') {
        mode = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      
      document.documentElement.classList.add(mode);
    </script>
    ```
*   **Key Data Attributes:**
    *   `data-theme-toggle="true"`: Marks element as a theme toggle button.
    *   `data-theme-mode="light|dark|system"`: Sets specific theme mode when clicked.
*   **Theme Modes:**
    *   `light`: Light theme (default).
    *   `dark`: Dark theme.
    *   `system`: Follows OS preference via `prefers-color-scheme` media query.
*   **HTML Attributes:**
    *   Set `data-theme-mode="mode"` on the `<html>` tag for initial/default mode.
*   **JS Initialization:**
    *   Automatic with global `KTComponents.init()`.
    *   Manual initialization:
        ```javascript
        const themeEl = document.querySelector('[data-theme-toggle="true"]');
        const theme = new KTTheme(themeEl);
        ```
*   **JS Methods:**
    *   `getMode()`: Get current theme mode.
    *   `setMode(mode)`: Set theme mode (`light`, `dark`, or `system`).
    *   `getSystemMode()`: Get system preference.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `theme-change`: When theme mode changes.
    *   Event handling example:
        ```javascript
        const theme = KTTheme.getInstance(themeEl);
        theme.on('theme-change', (detail) => {
          console.log('Theme changed to:', detail.mode);
        });
        ```
*   **CSS Variables:**
    *   Theme uses CSS variables for colors, shadows, and other properties.
    *   Variables are defined with light/dark variations.
    *   Access in custom styles: `var(--kt-... )`.
*   **Usage Notes:**
    *   Include the initialization script as early as possible to avoid FOUC (Flash of Unstyled Content).
    *   Store user preference in `localStorage['theme']`.
    *   Combine with dropdown/menu for a theme selector UI.
    *   CSS dark mode is applied via the `.dark` class on the `<html>` element.

---

### 3.20. Toggle

*   **Description:** A switch component that allows users to toggle between two states, offering a visually appealing alternative to checkboxes. ([Metronic Toggle Docs](https://keenthemes.com/metronic/tailwind/docs/components/toggle))
*   **HTML Structure:**
    ```html
    <div class="toggle" data-toggle="true">
      <div class="toggle-track">
        <div class="toggle-indicator"></div>
      </div>
      <input type="hidden" name="toggle" value="0"/>
    </div>
    ```
*   **Variants:**
    *   **Default Toggle:** Basic switch with default styling.
    *   **With Label:** Toggle with descriptive text.
        ```html
        <label class="toggle-with-label">
          <div class="toggle" data-toggle="true">
            <div class="toggle-track">
              <div class="toggle-indicator"></div>
            </div>
            <input type="hidden" name="toggle" value="0"/>
          </div>
          <span class="toggle-label">Enable feature</span>
        </label>
        ```
    *   **Colors:** Contextual color variants.
        ```html
        <div class="toggle toggle-primary" data-toggle="true">
          <!-- Toggle structure -->
        </div>
        <div class="toggle toggle-success" data-toggle="true">
          <!-- Toggle structure -->
        </div>
        <div class="toggle toggle-info" data-toggle="true">
          <!-- Toggle structure -->
        </div>
        <div class="toggle toggle-danger" data-toggle="true">
          <!-- Toggle structure -->
        </div>
        <div class="toggle toggle-warning" data-toggle="true">
          <!-- Toggle structure -->
        </div>
        ```
    *   **Sizes:** Different size options.
        ```html
        <div class="toggle toggle-sm" data-toggle="true">
          <!-- Toggle structure -->
        </div>
        <div class="toggle toggle-md" data-toggle="true">
          <!-- Toggle structure -->
        </div>
        <div class="toggle toggle-lg" data-toggle="true">
          <!-- Toggle structure -->
        </div>
        ```
    *   **Disabled State:** Non-interactive toggle.
        ```html
        <div class="toggle" data-toggle="true" data-toggle-disabled="true">
          <!-- Toggle structure -->
        </div>
        ```
    *   **Initial State:** Set initial checked state.
        ```html
        <div class="toggle" data-toggle="true" data-toggle-checked="true">
          <!-- Toggle structure -->
        </div>
        ```
*   **Key Data Attributes:**
    *   `data-toggle="true"`: Enable auto-initialization.
    *   `data-toggle-checked="true|false"`: Initial state (default: `false`).
    *   `data-toggle-disabled="true|false"`: Disabled state (default: `false`).
    *   `data-toggle-on-value="value"`: Value when toggled on (default: `1`).
    *   `data-toggle-off-value="value"`: Value when toggled off (default: `0`).
*   **Key Classes:**
    *   `toggle`: Main container.
    *   `toggle-track`: The track the indicator slides on.
    *   `toggle-indicator`: The sliding indicator.
    *   Color variants: `toggle-primary`, `toggle-success`, etc.
    *   Size modifiers: `toggle-sm`, `toggle-md`, `toggle-lg`.
    *   Positioning: `toggle-with-label` for label integration.
*   **JS Initialization:**
    *   **Auto:** Use `data-toggle="true"` on the main element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const toggleEl = document.querySelector('#my_toggle');
        const options = {
          checked: false,
          disabled: false,
          onValue: '1',
          offValue: '0'
        };
        const toggle = new KTToggle(toggleEl, options);
        ```
*   **JS Methods:**
    *   `check()`: Set toggle to checked state.
    *   `uncheck()`: Set toggle to unchecked state.
    *   `toggle()`: Toggle between states.
    *   `disable()`, `enable()`: Control interactivity.
    *   `isChecked()`: Get current state.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `toggle`: Before state change (cancelable).
    *   `toggled`: After state change.
    *   Event handling example:
        ```javascript
        const toggle = KTToggle.getInstance(toggleEl);
        toggle.on('toggled', (detail) => {
          console.log('Toggle state:', detail.value);
        });
        ```
*   **Usage Notes:**
    *   Use hidden input to capture state for form submissions.
    *   For accessibility, add `role="switch"` and `aria-checked` attributes.
    *   Group toggles with labels using `toggle-with-label` class.
    *   Can replace checkboxes in forms for a more modern UI.

---

### 3.21. Tooltip

*   **Description:** A small popup that displays informative text when the user hovers over, focuses on, or taps an element. ([Metronic Tooltip Docs](https://keenthemes.com/metronic/tailwind/docs/components/tooltip))
*   **HTML Structure:**
    ```html
    <!-- Element with tooltip -->
    <button class="btn btn-primary" data-tooltip="true" data-tooltip-content="This is a tooltip">
      Hover Me
    </button>
    
    <!-- Or using a separate element for tooltip content -->
    <button class="btn btn-primary" data-tooltip="true" data-tooltip-target="#my_tooltip_content">
      Hover Me
    </button>
    <div id="my_tooltip_content" class="hidden">
      Complex <strong>formatted</strong> tooltip content
    </div>
    ```
*   **Variants:**
    *   **Default Tooltip:** Simple text tooltip.
    *   **HTML Content:** Tooltip with formatted content.
    *   **Placement Options:** Different positioning relative to the trigger.
        ```html
        <button class="btn btn-primary" data-tooltip="true" 
                data-tooltip-placement="top" data-tooltip-content="Top tooltip">
          Top
        </button>
        <button class="btn btn-primary" data-tooltip="true" 
                data-tooltip-placement="right" data-tooltip-content="Right tooltip">
          Right
        </button>
        <button class="btn btn-primary" data-tooltip="true" 
                data-tooltip-placement="bottom" data-tooltip-content="Bottom tooltip">
          Bottom
        </button>
        <button class="btn btn-primary" data-tooltip="true" 
                data-tooltip-placement="left" data-tooltip-content="Left tooltip">
          Left
        </button>
        ```
    *   **Custom Animation:** Different animation effects.
        ```html
        <button class="btn btn-primary" data-tooltip="true" 
                data-tooltip-animation="fade" data-tooltip-content="Fade animation">
          Fade
        </button>
        <button class="btn btn-primary" data-tooltip="true" 
                data-tooltip-animation="zoom" data-tooltip-content="Zoom animation">
          Zoom
        </button>
        ```
    *   **Interactive Tooltip:** Allow interaction with tooltip content.
        ```html
        <button class="btn btn-primary" data-tooltip="true" data-tooltip-interactive="true"
                data-tooltip-content="<a href='#'>Click me</a>">
          Interactive
        </button>
        ```
    *   **Custom Width:** Control tooltip width.
        ```html
        <button class="btn btn-primary" data-tooltip="true" 
                data-tooltip-max-width="300px" data-tooltip-content="Wide tooltip content...">
          Wide Tooltip
        </button>
        ```
*   **Key Data Attributes:**
    *   `data-tooltip="true"`: Enable auto-initialization.
    *   `data-tooltip-content="text"`: Direct tooltip text.
    *   `data-tooltip-target="#id"`: Target element containing tooltip content.
    *   `data-tooltip-placement="top|right|bottom|left"`: Position (default: `top`).
    *   `data-tooltip-animation="fade|zoom"`: Animation effect (default: `fade`).
    *   `data-tooltip-trigger="hover|click|focus"`: Activation method (default: `hover focus`).
    *   `data-tooltip-interactive="true|false"`: Allow interaction with tooltip (default: `false`).
    *   `data-tooltip-max-width="width"`: Maximum tooltip width (default: `200px`).
    *   `data-tooltip-offset="x,y"`: Pixel offset from default position.
*   **Key Classes:**
    *   No specific classes required - all configuration is via data attributes.
    *   Tooltip container and arrow are generated dynamically.
*   **JS Initialization:**
    *   **Auto:** Use `data-tooltip="true"` on the trigger element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const tooltipEl = document.querySelector('#my_tooltip_trigger');
        const options = {
          content: 'Tooltip text',
          // or target: '#tooltip_content_id',
          placement: 'top',
          animation: 'fade',
          trigger: 'hover focus',
          interactive: false,
          maxWidth: '200px',
          offset: [0, 0]
        };
        const tooltip = new KTTooltip(tooltipEl, options);
        ```
*   **JS Methods:**
    *   `show()`: Display the tooltip.
    *   `hide()`: Hide the tooltip.
    *   `toggle()`: Toggle tooltip visibility.
    *   `update()`: Update tooltip position.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `show`: Before tooltip is shown (cancelable).
    *   `shown`: After tooltip is shown.
    *   `hide`: Before tooltip is hidden (cancelable).
    *   `hidden`: After tooltip is hidden.
*   **Usage Notes:**
    *   Keep tooltip content concise - ideally 1-2 short sentences.
    *   Use HTML tooltips for formatted content or interactive elements.
    *   Consider accessibility - ensure tooltips are keyboard accessible.
    *   For complex interactive popups, consider using Dropdown component instead.
    *   Position tooltips to avoid obscuring important content.


</rewritten_file> 