# Metronic Navigation Components

[Back to Metronic Guide Index](index.md)

---

## 3. Navigation Components

### 3.22. Menu

*   **Description:** A versatile navigation component with various styles, levels, and interactive features for organizing links and actions. ([Metronic Menu Docs](https://keenthemes.com/metronic/tailwind/docs/components/menu))
*   **HTML Structure:**
    ```html
    <div class="menu menu-default flex flex-col w-full">
      <!-- Simple menu item -->
      <div class="menu-item">
        <a class="menu-link" href="#">
          <span class="menu-icon"><i class="ki-outline ki-home"></i></span>
          <span class="menu-title">Dashboard</span>
        </a>
      </div>
      
      <!-- Menu item with badge -->
      <div class="menu-item">
        <a class="menu-link" href="#">
          <span class="menu-icon"><i class="ki-outline ki-notification"></i></span>
          <span class="menu-title">Notifications</span>
          <span class="menu-badge"><span class="badge badge-sm badge-primary">3</span></span>
        </a>
      </div>
      
      <!-- Menu item with submenu -->
      <div class="menu-item menu-accordion" data-accordion="true">
        <div class="menu-link" data-accordion-toggle="#submenu1">
          <span class="menu-icon"><i class="ki-outline ki-setting"></i></span>
          <span class="menu-title">Settings</span>
          <span class="menu-arrow"></span>
        </div>
        <div class="menu-sub" id="submenu1">
          <div class="menu-item">
            <a class="menu-link" href="#">
              <span class="menu-bullet"><i class="ki-outline ki-dot"></i></span>
              <span class="menu-title">General</span>
            </a>
          </div>
          <div class="menu-item">
            <a class="menu-link" href="#">
              <span class="menu-bullet"><i class="ki-outline ki-dot"></i></span>
              <span class="menu-title">Security</span>
            </a>
          </div>
        </div>
      </div>
    </div>
    ```
*   **Variants:**
    *   **Default Menu:** Standard vertical menu.
    *   **Horizontal Menu:** Inline horizontal layout.
        ```html
        <div class="menu menu-default menu-horizontal flex">
          <!-- Menu items -->
        </div>
        ```
    *   **Theme Variants:** Different visual styles.
        ```html
        <div class="menu menu-primary flex flex-col w-full">
          <!-- Menu items -->
        </div>
        <div class="menu menu-success flex flex-col w-full">
          <!-- Menu items -->
        </div>
        ```
    *   **With Accordion:** Expandable submenu sections.
        ```html
        <div class="menu menu-default flex flex-col w-full" data-menu-accordion="true">
          <!-- Menu items with submenus -->
        </div>
        ```
    *   **Custom Icons:** Different icon styles for menu items.
        ```html
        <!-- With bullet -->
        <div class="menu-item">
          <a class="menu-link" href="#">
            <span class="menu-bullet"><i class="ki-outline ki-dot"></i></span>
            <span class="menu-title">Item with bullet</span>
          </a>
        </div>
        
        <!-- With number -->
        <div class="menu-item">
          <a class="menu-link" href="#">
            <span class="menu-number">1</span>
            <span class="menu-title">Item with number</span>
          </a>
        </div>
        ```
    *   **Indentation Levels:** Nested submenu hierarchies.
        ```html
        <div class="menu-item menu-accordion" data-accordion="true">
          <!-- Level 1 -->
          <div class="menu-link" data-accordion-toggle="#submenu2">
            <span class="menu-title">Level 1</span>
            <span class="menu-arrow"></span>
          </div>
          <div class="menu-sub" id="submenu2">
            <!-- Level 2 -->
            <div class="menu-item menu-accordion" data-accordion="true">
              <div class="menu-link" data-accordion-toggle="#submenu3">
                <span class="menu-title">Level 2</span>
                <span class="menu-arrow"></span>
              </div>
              <div class="menu-sub" id="submenu3">
                <!-- Level 3 -->
                <div class="menu-item">
                  <a class="menu-link" href="#">
                    <span class="menu-title">Level 3</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        ```
*   **Key Classes:**
    *   **Main Container:**
        *   `menu`: Base class.
        *   Style variants: `menu-default`, `menu-primary`, `menu-success`, etc.
        *   Layout variants: `menu-horizontal`, `menu-vertical`.
    *   **Menu Structure:**
        *   `menu-item`: Individual menu item.
        *   `menu-link`: Link or clickable area within item.
        *   `menu-accordion`: Item with expandable submenu.
        *   `menu-sub`: Submenu container.
    *   **Item Components:**
        *   `menu-icon`: Icon preceding title.
        *   `menu-bullet`: Small bullet icon.
        *   `menu-number`: Numerical indicator.
        *   `menu-title`: Item text.
        *   `menu-badge`: Badge/counter.
        *   `menu-arrow`: Expand/collapse indicator.
*   **Key Data Attributes:**
    *   `data-menu-accordion="true"`: Enable accordion behavior for whole menu.
    *   `data-accordion="true"`: Mark item as accordion (with submenu).
    *   `data-accordion-toggle="#id"`: Target submenu element.
*   **JS Interaction:**
    *   **Auto:** Uses Accordion component for expand/collapse behavior.
    *   Manually manage state with Accordion API.
*   **State Classes:**
    *   `active`: Indicates current/selected item.
    *   `hover`: Applied during hover (can be styled).
    *   `here`: Indicates parent of active item.
    *   `show`: Expanded submenu state.
*   **Usage Notes:**
    *   For responsive designs, use a horizontal menu that becomes vertical on mobile.
    *   Limit nesting to 3 levels for better usability.
    *   Use badges sparingly - only for important counters or status indicators.
    *   Combine with Drawer component for slide-out navigation panels.
    *   For dropdown menus, combine with Dropdown component.

---

### 3.23. Pagination

*   **Description:** A component for navigating through multi-page content, providing links to specific pages and next/previous navigation. ([Metronic Pagination Docs](https://keenthemes.com/metronic/tailwind/docs/components/pagination))
*   **HTML Structure:**
    ```html
    <div class="pagination">
      <!-- Previous page button -->
      <button class="btn" disabled>
        <i class="ki-outline ki-black-left"></i>
      </button>
      
      <!-- Page buttons -->
      <button class="btn active">1</button>
      <button class="btn">2</button>
      <button class="btn">3</button>
      
      <!-- Next page button -->
      <button class="btn">
        <i class="ki-outline ki-black-right"></i>
      </button>
    </div>
    ```
*   **Variants:**
    *   **Default Pagination:** Basic page navigation.
    *   **With Disabled States:** Inactive navigation buttons.
        ```html
        <div class="pagination">
          <button class="btn" disabled>
            <i class="ki-outline ki-double-left"></i>
          </button>
          <button class="btn" disabled>
            <i class="ki-outline ki-black-left"></i>
          </button>
          <button class="btn active">1</button>
          <button class="btn">2</button>
          <button class="btn">3</button>
          <button class="btn">
            <i class="ki-outline ki-black-right"></i>
          </button>
          <button class="btn">
            <i class="ki-outline ki-double-right"></i>
          </button>
        </div>
        ```
    *   **With Ellipsis:** For large page ranges.
        ```html
        <div class="pagination">
          <button class="btn">
            <i class="ki-outline ki-black-left"></i>
          </button>
          <button class="btn">1</button>
          <button class="btn">2</button>
          <button class="btn active">3</button>
          <button class="btn">4</button>
          <button class="btn">5</button>
          <span class="pagination-ellipsis">...</span>
          <button class="btn">20</button>
          <button class="btn">
            <i class="ki-outline ki-black-right"></i>
          </button>
        </div>
        ```
    *   **Sizes:** Different pagination sizing.
        ```html
        <div class="pagination pagination-sm">
          <!-- Small pagination -->
        </div>
        <div class="pagination">
          <!-- Default size -->
        </div>
        <div class="pagination pagination-lg">
          <!-- Large pagination -->
        </div>
        ```
    *   **With Info Text:** Shows current page range and total.
        ```html
        <div class="flex items-center gap-4">
          <span class="text-gray-600 text-2sm">1-10 of 52</span>
          <div class="pagination">
            <!-- Pagination buttons -->
          </div>
        </div>
        ```
    *   **Combined with Page Size Selector:**
        ```html
        <div class="flex justify-between items-center flex-wrap gap-4">
          <div class="flex items-center gap-2">
            Show
            <select class="select select-sm w-16" name="perpage">
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="25">25</option>
              <option value="50">50</option>
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
*   **Key Classes:**
    *   `pagination`: Main container.
    *   Size variants: `pagination-sm`, `pagination-lg`.
    *   `pagination-ellipsis`: For ellipsis/separator.
    *   Button states: `active`, `disabled`.
*   **Integration with DataTable:**
    *   DataTable component generates pagination automatically.
    *   Example with DataTable:
        ```html
        <div class="datatable-footer">
          <div class="datatable-pagination" data-datatable-pagination="true">
            <!-- Auto-generated pagination -->
          </div>
        </div>
        ```
*   **JS Implementation:**
    *   Implement click handlers for page navigation:
        ```javascript
        // Example pagination handler
        document.querySelectorAll('.pagination .btn').forEach(btn => {
          btn.addEventListener('click', (e) => {
            if (btn.disabled || btn.classList.contains('active')) return;
            
            const page = btn.textContent;
            // Logic to load page data...
            
            // Update active state
            document.querySelector('.pagination .btn.active').classList.remove('active');
            btn.classList.add('active');
          });
        });
        ```
*   **Accessibility Considerations:**
    *   Add `aria-current="page"` to the active button.
    *   Use `aria-label` for prev/next buttons (e.g., `aria-label="Previous page"`).
    *   Wrap in `nav` element with `aria-label="Pagination"`.
*   **Usage Notes:**
    *   Limit visible page numbers to prevent overflow on smaller screens.
    *   Always disable navigation buttons when at first/last page.
    *   Use icons consistently - arrows for prev/next, double arrows for first/last.
    *   Show current range (e.g., "1-10 of 52") to provide context.
    *   Consider adding keyboard navigation support.

---

### 3.24. Scrollspy

*   **Description:** Automatically highlights navigation links in a list or menu as the user scrolls through corresponding content sections within a scrollable container. ([Metronic Scrollspy Docs](https://keenthemes.com/metronic/tailwind/docs/components/scrollspy))
*   **HTML Structure:**
    ```html
    <div class="flex gap-8">
      <!-- Navigation Links -->
      <div data-scrollspy="true" data-scrollspy-target="#scrollable_container">
        <a data-scrollspy-anchor="true" href="#section1" class="... scrollspy-active:bg-primary ...">Item 1</a>
        <a data-scrollspy-anchor="true" href="#section2" class="...">Item 2</a>
        <a data-scrollspy-anchor="true" href="#section3" class="...">Item 3</a>
      </div>
      
      <!-- Scrollable Content Area -->
      <div id="scrollable_container" class="scrollable-y h-[300px]">
        <div id="section1">Section 1 Content...</div>
        <div id="section2">Section 2 Content...</div>
        <div id="section3">Section 3 Content...</div>
      </div>
    </div>
    ```
*   **Key Data Attributes:**
    *   **On scrollspy container:**
        *   `data-scrollspy="true"`: Enable auto-initialization.
        *   `data-scrollspy-target="#id"`: Selector for the scrollable content container (default: `body`).
        *   `data-scrollspy-offset="number|breakpoint:number"`: Pixel offset for activation point (e.g., `30` or `30|lg:50`).
        *   `data-scrollspy-smooth="true|false"`: Enable smooth scrolling on link click (default: `true`).
    *   **On anchor links:**
        *   `data-scrollspy-anchor="true"`: Marks the link as a scrollspy anchor.
        *   `href="#id"`: Must point to the ID of the corresponding content section.
*   **Key Classes:**
    *   `scrollspy-active:{utility}`: Tailwind utility classes applied to the active anchor link (e.g., `scrollspy-active:bg-primary`, `scrollspy-active:text-white`). These are defined in your custom CSS or via the `scrollspy-active` variant in `tailwind.config.js`.
*   **JS Initialization:**
    *   **Auto:** Use `data-scrollspy="true"` on the navigation container.
    *   **Manual:** Use JavaScript:
        ```javascript
        const scrollspyEl = document.querySelector('#my_scrollspy_nav');
        const options = {
          target: '#my_scrollable_content',
          offset: 50,
          smooth: true
        };
        const scrollspy = new KTScrollspy(scrollspyEl, options);
        ```
*   **JS Methods:**
    *   `scrollTo(anchorElement)`: Programmatically scroll to a specific section.
    *   `update()`: Recalculate positions after DOM changes.
    *   `updateAnchor(anchorElement)`: Update a specific anchor's state.
    *   `isActive(anchorElement)`: Check if an anchor is active.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `activate`: Fires when an anchor becomes active.
        ```javascript
        scrollspy.on('activate', (anchorElement) => {
          console.log('Activated:', anchorElement.href);
        });
        ```
*   **Usage Notes:**
    *   Ideal for single-page documentation or landing pages.
    *   Ensure the scrollable container (`data-scrollspy-target`) has a defined height and allows overflow.
    *   Works with nested navigation structures.
    *   Customize the active state appearance using the `scrollspy-active:` variant.

---

### 3.25. Scrollto

*   **Description:** A utility component that provides smooth scrolling to a target element within the page when a trigger element is clicked. ([Metronic Scrollto Docs](https://keenthemes.com/metronic/tailwind/docs/components/scrollto))
*   **HTML Structure:**
    ```html
    <!-- Trigger element -->
    <button class="btn btn-primary" data-scrollto="true" data-scrollto-target="#target_section">
      Scroll to Section
    </button>
    
    <!-- Target element -->
    <div id="target_section" class="mt-[500px]">
      This is the target section.
    </div>
    ```
*   **Key Data Attributes:**
    *   `data-scrollto="true"`: Enable auto-initialization.
    *   `data-scrollto-target="#id"`: Selector for the target element to scroll to.
    *   `data-scrollto-offset="number"`: Pixel offset from the top of the target element (e.g., `-50` to stop 50px above).
    *   `data-scrollto-duration="milliseconds"`: Duration of the scroll animation (default: `500`).
    *   `data-scrollto-easing="linear|ease-in-out"`: Animation easing function (default: `ease-in-out`).
*   **JS Initialization:**
    *   **Auto:** Use `data-scrollto="true"` on the trigger element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const scrolltoEl = document.querySelector('#my_scroll_trigger');
        const options = {
          target: '#my_target_element',
          offset: 0,
          duration: 500,
          easing: 'ease-in-out'
        };
        const scrollto = new KTScrollto(scrolltoEl, options);
        ```
*   **JS Methods:**
    *   `scroll()`: Programmatically trigger the scroll animation.
    *   `update()`: Update target/options if needed.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `scroll`: Before scroll animation starts (cancelable).
    *   `scrolled`: After scroll animation completes.
*   **Usage Notes:**
    *   Useful for "Scroll to Top" buttons or navigating within a long page.
    *   `data-scrollto-offset` is helpful when using fixed headers.
    *   Ensure target element has a unique ID.

---

### 3.26. Stepper

*   **Description:** Guides users through a sequence of steps in a process, such as a wizard or multi-stage form, indicating current progress. ([Metronic Stepper Docs](https://keenthemes.com/metronic/tailwind/docs/components/stepper))
*   **HTML Structure:**
    ```html
    <div class="stepper" id="my_stepper" data-stepper="true">
      <!-- Stepper Navigation -->
      <div class="stepper-nav">
        <div class="stepper-item current" data-stepper-target="#step1" data-stepper-trigger="true">
          <span class="stepper-icon">1</span>
          <span class="stepper-title">Step 1</span>
        </div>
        <div class="stepper-line"></div>
        <div class="stepper-item" data-stepper-target="#step2" data-stepper-trigger="true">
          <span class="stepper-icon">2</span>
          <span class="stepper-title">Step 2</span>
        </div>
        <div class="stepper-line"></div>
        <div class="stepper-item" data-stepper-target="#step3" data-stepper-trigger="true">
          <span class="stepper-icon">3</span>
          <span class="stepper-title">Step 3</span>
        </div>
      </div>
      
      <!-- Stepper Content -->
      <div class="stepper-content mt-5">
        <div id="step1" class="stepper-pane current">
          Content for Step 1...
          <button class="btn btn-primary mt-3" data-stepper-action="next">Next</button>
        </div>
        <div id="step2" class="stepper-pane">
          Content for Step 2...
          <button class="btn btn-light mt-3" data-stepper-action="prev">Previous</button>
          <button class="btn btn-primary mt-3" data-stepper-action="next">Next</button>
        </div>
        <div id="step3" class="stepper-pane">
          Content for Step 3...
          <button class="btn btn-light mt-3" data-stepper-action="prev">Previous</button>
          <button class="btn btn-success mt-3" data-stepper-action="submit">Submit</button>
        </div>
      </div>
    </div>
    ```
*   **Variants:**
    *   **Horizontal Stepper:** Default layout.
    *   **Vertical Stepper:** Align steps vertically.
        ```html
        <div class="stepper stepper-vertical" id="vertical_stepper" data-stepper="true">
          <!-- Stepper nav and content -->
        </div>
        ```
*   **Key Data Attributes:**
    *   **On stepper container:**
        *   `data-stepper="true"`: Enable auto-initialization.
        *   `data-stepper-current-step="index"`: Set initial step (1-based).
        *   `data-stepper-clickable="true|false"`: Allow clicking nav items to jump steps (default: `false`).
    *   **On navigation items (`stepper-item`):**
        *   `data-stepper-target="#id"`: Target content pane ID.
        *   `data-stepper-trigger="true"`: Mark as clickable trigger (if `clickable=true`).
    *   **On action buttons:**
        *   `data-stepper-action="next|prev|submit|goto"`: Define button action.
        *   `data-stepper-goto="index"`: Specify target step index for `goto` action.
*   **Key Classes:**
    *   **Main:** `stepper`, `stepper-vertical`.
    *   **Navigation:** `stepper-nav`, `stepper-item`, `stepper-icon`, `stepper-title`, `stepper-line`.
    *   **Content:** `stepper-content`, `stepper-pane`.
    *   **States:** `current` (active step/pane), `completed`, `pending`.
*   **JS Initialization:**
    *   **Auto:** Use `data-stepper="true"` on the main container.
    *   **Manual:** Use JavaScript:
        ```javascript
        const stepperEl = document.querySelector('#my_stepper');
        const options = {
          startIndex: 1,
          clickable: false
        };
        const stepper = new KStepper(stepperEl, options);
        ```
*   **JS Methods:**
    *   `goNext()`: Move to the next step.
    *   `goPrev()`: Move to the previous step.
    *   `goto(index)`: Move to a specific step (1-based index).
    *   `getCurrentStepIndex()`: Get the index of the current step.
    *   `getTotalSteps()`: Get the total number of steps.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `stepper-change`: Before step change (cancelable).
    *   `stepper-changed`: After step change.
    *   `stepper-next`: Before going to next step (cancelable).
    *   `stepper-prev`: Before going to previous step (cancelable).
    *   `stepper-submit`: When submit action is triggered.
*   **Usage Notes:**
    *   Ideal for multi-stage forms, setup wizards, or onboarding flows.
    *   Use validation within the `stepper-change` or `stepper-next` events to prevent proceeding with invalid data.
    *   Structure content panes (`stepper-pane`) logically.
    *   Ensure action buttons (`data-stepper-action`) are correctly placed within panes.

---

### 3.27. Sticky

*   **Description:** Keeps an element fixed within the viewport or a parent container once it reaches a certain scroll position. Useful for sticky headers, sidebars, or toolbars. ([Metronic Sticky Docs](https://keenthemes.com/metronic/tailwind/docs/components/sticky))
*   **HTML Structure:**
    ```html
    <!-- Sticky element -->
    <div id="my_sticky_element" data-sticky="true" 
         data-sticky-offset-top="100" 
         data-sticky-offset-bottom="20"
         data-sticky-container="#parent_container"
         data-sticky-breakpoint="lg"
         class="bg-light p-4">
        This element will become sticky.
    </div>
    
    <!-- Optional parent container -->
    <div id="parent_container" class="mt-5 h-[1000px]">
      Scrollable content area...
    </div>
    ```
*   **Key Data Attributes:**
    *   `data-sticky="true"`: Enable auto-initialization.
    *   `data-sticky-offset-top="number"`: Top offset when sticky (pixels, default: `0`).
    *   `data-sticky-offset-bottom="number"`: Bottom offset when sticky (pixels, default: `0`).
    *   `data-sticky-zindex="number"`: Z-index when sticky (default: `100`).
    *   `data-sticky-container="#id|false"`: Selector for parent container to constrain stickiness (default: `false` - viewport).
    *   `data-sticky-breakpoint="lg"`: Breakpoint below which stickiness is disabled (options: `sm`, `md`, `lg`, `xl`, `xxl`, default: `false` - always sticky).
    *   `data-sticky-reverse="true|false"`: Sticks when scrolling up, not down (default: `false`).
*   **Key Classes (Applied dynamically):**
    *   `sticky`: Base class applied when sticky.
    *   `sticky-active`: Applied when element is currently sticky.
    *   `sticky-reverse`: Applied when `reverse=true`.
    *   `sticky-top-original|sticky-top-active`: Applied based on scroll direction.
*   **JS Initialization:**
    *   **Auto:** Use `data-sticky="true"` on the element.
    *   **Manual:** Use JavaScript:
        ```javascript
        const stickyEl = document.querySelector('#my_sticky_element');
        const options = {
          offsetTop: 100,
          offsetBottom: 20,
          zIndex: 101,
          container: '#parent_container',
          breakpoint: 'lg',
          reverse: false
        };
        const sticky = new KTSticky(stickyEl, options);
        ```
*   **JS Methods:**
    *   `update()`: Recalculate dimensions and position.
    *   `disable()`, `enable()`: Temporarily disable/enable stickiness.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `sticky-on`: When element becomes sticky.
    *   `sticky-off`: When element is no longer sticky.
    *   `sticky-position`: During position updates.
*   **Usage Notes:**
    *   Ensure the sticky element has a defined width, otherwise it might collapse when `position: fixed` is applied.
    *   `data-sticky-offset-top` is commonly used to account for fixed headers.
    *   Use `data-sticky-container` to limit stickiness within a specific section.
    *   `data-sticky-breakpoint` allows disabling stickiness on smaller screens.
    *   Combine with other components like toolbars or navigation menus.

---

### 3.28. Tabs

*   **Description:** Organizes content into different sections that can be switched between using tab navigation, saving space and improving clarity. ([Metronic Tabs Docs](https://keenthemes.com/metronic/tailwind/docs/components/tabs))
*   **HTML Structure:**
    ```html
    <div data-tabs="true">
      <!-- Tab Navigation -->
      <div class="tabs-nav">
        <button class="tab-link active" data-tab-target="#tab1" data-tab-toggle="true">Tab 1</button>
        <button class="tab-link" data-tab-target="#tab2" data-tab-toggle="true">Tab 2</button>
        <button class="tab-link" data-tab-target="#tab3" data-tab-toggle="true">Tab 3</button>
      </div>
      
      <!-- Tab Content -->
      <div class="tabs-content mt-5">
        <div id="tab1" class="tab-pane active">
          Content for Tab 1...
        </div>
        <div id="tab2" class="tab-pane">
          Content for Tab 2...
        </div>
        <div id="tab3" class="tab-pane">
          Content for Tab 3...
        </div>
      </div>
    </div>
    ```
*   **Variants:**
    *   **Default Tabs:** Basic tab navigation.
    *   **Pill Style:** Rounded pill-shaped tabs.
        ```html
        <div data-tabs="true" data-tabs-style="pills">
          <div class="tabs-nav">
            <!-- Pill-style tab links -->
          </div>
          <div class="tabs-content mt-5">
            <!-- Tab panes -->
          </div>
        </div>
        ```
    *   **Line Style:** Underlined tabs.
        ```html
        <div data-tabs="true" data-tabs-style="line">
          <div class="tabs-nav">
            <!-- Line-style tab links -->
          </div>
          <div class="tabs-content mt-5">
            <!-- Tab panes -->
          </div>
        </div>
        ```
*   **Key Data Attributes:**
    *   **On main container:**
        *   `data-tabs="true"`: Enable auto-initialization.
        *   `data-tabs-style="default|pills|line"`: Visual style (default: `default`).
    *   **On tab links (`tab-link`):**
        *   `data-tab-target="#id"`: Target content pane ID.
        *   `data-tab-toggle="true"`: Mark as tab toggle.
*   **Key Classes:**
    *   **Navigation:** `tabs-nav`, `tab-link`.
    *   **Content:** `tabs-content`, `tab-pane`.
    *   **States:** `active` (applied to active link and pane).
*   **JS Initialization:**
    *   **Auto:** Use `data-tabs="true"` on the main container.
    *   **Manual:** Use JavaScript:
        ```javascript
        const tabsEl = document.querySelector('#my_tabs');
        const options = {
          style: 'default'
        };
        const tabs = new KTTabs(tabsEl, options);
        ```
*   **JS Methods:**
    *   `show(tabElement)`: Activate a specific tab.
    *   `getActiveTab()`: Get the currently active tab element.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `tab-show`: Before a tab is shown (cancelable).
    *   `tab-shown`: After a tab is shown.
*   **Usage Notes:**
    *   Ensure `data-tab-target` on links matches the `id` of the `tab-pane`.
    *   Place tab navigation (`tabs-nav`) before content (`tabs-content`).
    *   Use consistent styling (`pills`, `line`, or default) for all tabs in a set.
    *   Can be nested, but avoid excessive complexity.

---
*(End of Components)* 