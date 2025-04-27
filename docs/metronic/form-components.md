# Metronic Form Components

[Back to Metronic Guide Index](index.md)

---

## 4. Form Components

### 4.1. Checkbox

*   **Description:** A custom styled checkbox control for forms. ([Metronic Checkbox Docs](https://keenthemes.com/metronic/tailwind/docs/components/checkbox))
*   **HTML Structure:**
    ```html
    <label class="form-label flex items-center gap-2.5">
      <input class="checkbox" name="check" type="checkbox" value="1"/>
      Checkbox Label
    </label>
    ```
*   **Variants:**
    *   **Default:** Standard checkbox.
    *   **Checked:** Use `checked` attribute.
        ```html
        <input checked class="checkbox" name="check" type="checkbox" value="1"/>
        ```
    *   **Indeterminate:** Set programmatically via JS.
        ```html
        <input class="checkbox" id="my_checkbox" name="check" type="checkbox" value="1"/>
        ```
        ```javascript
        const checkboxEl = document.querySelector('#my_checkbox');
        checkboxEl.indeterminate = true;
        ```
    *   **Disabled:** Use `disabled` attribute.
        ```html
        <input disabled class="checkbox" name="check" type="checkbox" value="1"/>
        <input checked disabled class="checkbox" name="check" type="checkbox" value="1"/>
        ```
    *   **Sizes:** Different size options.
        ```html
        <input class="checkbox checkbox-sm" type="checkbox" /> <!-- Small -->
        <input class="checkbox" type="checkbox" />           <!-- Default -->
        <input class="checkbox checkbox-lg" type="checkbox" /> <!-- Large -->
        ```
*   **Key Classes:**
    *   `checkbox`: Base class for styling.
    *   Size variants: `checkbox-sm`, `checkbox-lg`.
    *   Typically wrapped in a `label` with `form-label` for proper layout and click handling.
*   **Usage Notes:**
    *   Use standard `name` and `value` attributes for form submission.
    *   Indeterminate state is visual only and must be set via JavaScript.

---

### 4.2. File Input

*   **Description:** An enhanced file input element with improved styling. ([Metronic File Input Docs](https://keenthemes.com/metronic/tailwind/docs/components/file-input))
*   **HTML Structure:**
    ```html
    <input class="file-input" type="file"/>
    ```
*   **Variants:**
    *   **Default:** Basic file input.
    *   **Multiple:** Allow multiple file selection.
        ```html
        <input class="file-input" multiple type="file"/>
        ```
    *   **Disabled:** Non-interactive state.
        ```html
        <input class="file-input" disabled type="file"/>
        ```
    *   **Validation States:** Use border colors for visual feedback.
        ```html
        <input class="file-input border-danger" type="file"/> <!-- Error -->
        <input class="file-input border-success" type="file"/> <!-- Success -->
        ```
    *   **Sizes:** Adjust input size.
        ```html
        <input class="file-input file-input-sm" type="file"/> <!-- Small -->
        <input class="file-input" type="file"/>           <!-- Default -->
        <input class="file-input file-input-lg" type="file"/> <!-- Large -->
        ```
*   **Key Classes:**
    *   `file-input`: Base class.
    *   Size variants: `file-input-sm`, `file-input-lg`.
    *   Validation state classes (applied directly or on parent): `border-danger`, `border-success`.
*   **Usage Notes:**
    *   Styling applies to the button part of the input.
    *   File list rendering needs custom handling.

---

### 4.3. Image Input

*   **Description:** A custom component for handling image uploads with thumbnail preview and remove/change actions. ([Metronic Image Input Docs](https://keenthemes.com/metronic/tailwind/docs/components/image-input))
*   **HTML Structure:**
    ```html
    <div class="image-input size-16" data-image-input="true">
      <!-- Hidden file input -->
      <input accept=".png, .jpg, .jpeg" name="avatar" type="file"/>
      <!-- Hidden input for remove state -->
      <input name="avatar_remove" type="hidden"/>
      
      <!-- Remove/Revert Button -->
      <div class="btn btn-icon btn-icon-xs btn-light shadow-default absolute z-1 size-5 -top-0.5 -right-0.5 rounded-full" 
           data-image-input-remove data-tooltip="#image_input_tooltip">
        <i class="ki-outline ki-cross"></i>
      </div>
      <span class="tooltip" id="image_input_tooltip">Click to remove or revert</span>
      
      <!-- Placeholder / Preview Area -->
      <div class="image-input-placeholder rounded-full border-2 border-gray-300" 
           style="background-image:url(/path/to/blank.png)">
        <!-- Image Preview -->
        <div class="image-input-preview rounded-full"></div>
        <!-- Change Overlay (optional) -->
        <div class="flex items-center justify-center cursor-pointer h-5 left-0 right-0 bottom-0 bg-dark-clarity absolute">
          <svg ...>...</svg> <!-- Change icon -->
        </div>
      </div>
    </div>
    ```
*   **Key Data Attributes:**
    *   `data-image-input="true"`: Enable auto-initialization.
    *   `data-image-input-remove`: Marks the remove/revert button.
*   **Key Classes:**
    *   `image-input`: Main container.
    *   `image-input-placeholder`: Container for background/preview.
    *   `image-input-preview`: Dynamically populated preview element.
    *   `image-input-empty`: Class added when no image is selected/previewed.
    *   Size classes (`size-16` etc.) applied to main container.
    *   Shape classes (`rounded-full`, `rounded`, etc.) applied to placeholder and preview.
*   **JS Initialization:**
    *   **Auto:** Use `data-image-input="true"`.
    *   **Manual:** Use JavaScript:
        ```javascript
        const imageInputEl = document.querySelector('#my_image_input');
        const imageInput = new KTImageInput(imageInputEl);
        ```
*   **JS Methods:**
    *   `remove()`: Clear the preview and set remove state.
    *   `getInputElement()`: Get the hidden file input.
    *   `isChanged()`: Check if image has been changed.
    *   `isEmpty()`: Check if currently empty.
    *   `update()`: Recalculate state.
    *   Other utility methods: `getElement()`, `dispose()`.
*   **JS Events:**
    *   `change`: Before image change initiated.
    *   `changed`: After image successfully changed.
    *   `remove`: Before image removal initiated.
    *   `removed`: After image successfully removed.
*   **Usage Notes:**
    *   Requires specific HTML structure with nested elements for preview and controls.
    *   Use `accept` attribute on file input to restrict file types.
    *   The `name="avatar_remove"` hidden input helps track removal state on form submission.

---

### 4.4. Input

*   **Description:** A custom styled text input field for forms. ([Metronic Input Docs](https://keenthemes.com/metronic/tailwind/docs/components/input))
*   **HTML Structure:**
    ```html
    <input class="input" type="text" placeholder="Enter text..."/>
    ```
*   **Variants:**
    *   **Default:** Basic text input.
    *   **Disabled:** Non-interactive state.
        ```html
        <input class="input" disabled type="text" placeholder="Disabled"/>
        ```
    *   **Readonly:** Value cannot be changed.
        ```html
        <input class="input" readonly type="text" value="Readonly value"/>
        ```
    *   **Validation States:** Visual feedback using border colors.
        ```html
        <input class="input border-danger" type="text" placeholder="Error state"/>
        <input class="input border-success" type="text" placeholder="Success state"/>
        ```
    *   **Sizes:** Adjust input field size.
        ```html
        <input class="input input-sm" type="text" placeholder="Small"/>
        <input class="input" type="text" placeholder="Default"/>
        <input class="input input-lg" type="text" placeholder="Large"/>
        ```
*   **Key Classes:**
    *   `input`: Base class for styling.
    *   Size variants: `input-sm`, `input-lg`.
    *   Validation state classes: `border-danger`, `border-success`.
*   **Usage Notes:**
    *   Works with standard input types like `text`, `email`, `password`, `number`, etc.
    *   Combine with Input Group component for icons or buttons attached.

---

### 4.5. Input Group

*   **Description:** Extends input fields by adding text, icons, or buttons directly adjacent to the input. ([Metronic Input Group Docs](https://keenthemes.com/metronic/tailwind/docs/components/input-group))
*   **HTML Structure:**
    ```html
    <!-- Icon Prefix -->
    <div class="input-group">
      <i class="ki-outline ki-magnifier input-group-icon"></i>
      <input class="input ps-11" type="text" placeholder="Search..."/>
    </div>
    
    <!-- Text Suffix -->
    <div class="input-group">
      <input class="input" type="text" placeholder="Amount"/>
      <span class="input-group-text">.00</span>
    </div>
    
    <!-- Button Appended -->
    <div class="input-group">
      <input class="input rounded-e-none" type="email" placeholder="Recipient's username"/>
      <button class="btn btn-primary rounded-s-none">@example.com</button>
    </div>
    ```
*   **Variants:**
    *   **Text Addon:** Prepend or append text labels.
    *   **Icon Addon:** Prepend or append icons.
    *   **Button Addon:** Attach buttons to the input.
    *   **Checkbox/Radio Addon:** Embed checkboxes or radios.
        ```html
        <div class="input-group">
          <div class="input-group-text">
            <input class="checkbox checkbox-sm" type="checkbox"/>
          </div>
          <input class="input" type="text" placeholder="Checkbox addon"/>
        </div>
        ```
    *   **Segmented Buttons:** Multiple buttons attached.
        ```html
        <div class="input-group">
          <button class="btn btn-outline-secondary">Action</button>
          <button class="btn btn-icon btn-outline-secondary" data-dropdown="true" data-dropdown-trigger="click">
            <i class="ki-outline ki-down"></i>
          </button>
          <input class="input" type="text" placeholder="Segmented button"/>
        </div>
        ```
    *   **Sizes:** Match input group size to input size (`input-group-sm`, `input-group-lg`).
        ```html
        <div class="input-group input-group-sm">
          <span class="input-group-text">Small</span>
          <input class="input input-sm" type="text"/>
        </div>
        <div class="input-group input-group-lg">
          <span class="input-group-text">Large</span>
          <input class="input input-lg" type="text"/>
        </div>
        ```
*   **Key Classes:**
    *   `input-group`: Main container.
    *   `input-group-text`: For text addons.
    *   `input-group-icon`: For icon addons.
    *   Size variants: `input-group-sm`, `input-group-lg` (applied to main container).
    *   Use `rounded-s-none` or `rounded-e-none` on inputs/buttons to remove rounding on joined sides.
    *   Adjust input padding (`ps-*`, `pe-*`) when using icons.
*   **Usage Notes:**
    *   Ensure elements inside `input-group` have consistent heights (e.g., use matching size variants like `input-sm` with `input-group-sm`).
    *   Icons require manual padding adjustment on the input (e.g., `ps-11` if icon is on the left).

---

### 4.6. Radio

*   **Description:** A custom styled radio button control for selecting one option from a set. ([Metronic Radio Docs](https://keenthemes.com/metronic/tailwind/docs/components/radio))
*   **HTML Structure:**
    ```html
    <label class="form-label flex items-center gap-2.5">
      <input class="radio" name="radio_option" type="radio" value="1"/>
      Option 1
    </label>
    <label class="form-label flex items-center gap-2.5">
      <input checked class="radio" name="radio_option" type="radio" value="2"/>
      Option 2 (Checked)
    </label>
    ```
*   **Variants:**
    *   **Default:** Standard radio button.
    *   **Checked:** Use `checked` attribute for default selection.
    *   **Disabled:** Use `disabled` attribute.
        ```html
        <input disabled class="radio" name="radio_disabled" type="radio" value="1"/>
        <input checked disabled class="radio" name="radio_disabled" type="radio" value="2"/>
        ```
    *   **Sizes:** Different size options.
        ```html
        <input class="radio radio-sm" type="radio" /> <!-- Small -->
        <input class="radio" type="radio" />           <!-- Default -->
        <input class="radio radio-lg" type="radio" /> <!-- Large -->
        ```
*   **Key Classes:**
    *   `radio`: Base class for styling.
    *   Size variants: `radio-sm`, `radio-lg`.
    *   Wrap in a `label` with `form-label`.
*   **Usage Notes:**
    *   All radio buttons within a group must share the same `name` attribute.
    *   Use the `value` attribute to differentiate options.

---

### 4.7. Range

*   **Description:** A custom styled range input slider for selecting a value within a defined range. ([Metronic Range Docs](https://keenthemes.com/metronic/tailwind/docs/components/range))
*   **HTML Structure:**
    ```html
    <label class="form-label mb-2" for="range_1">Example range</label>
    <input class="range" id="range_1" max="10" min="0" type="range" value="5"/>
    ```
*   **Variants:**
    *   **Default:** Basic range slider.
    *   **Min/Max:** Define the range boundaries.
        ```html
        <input class="range" max="20" min="10" type="range" value="15"/>
        ```
    *   **Steps:** Specify the increment value.
        ```html
        <input class="range" max="10" min="2" step="0.5" type="range" value="5"/>
        ```
    *   **Disabled:** Non-interactive state.
        ```html
        <input class="range" disabled max="10" min="0" type="range" value="5"/>
        ```
*   **Key Classes:**
    *   `range`: Base class for styling.
*   **HTML Attributes:**
    *   `min`, `max`, `step`, `value`, `disabled` standard input type="range" attributes.
*   **Usage Notes:**
    *   Styling primarily affects the track and thumb.
    *   Combine with JavaScript to display the current value dynamically.

---

### 4.8. Select

*   **Description:** A custom styled dropdown select control for forms. ([Metronic Select Docs](https://keenthemes.com/metronic/tailwind/docs/components/select))
*   **HTML Structure:**
    ```html
    <select class="select" name="select">
      <option value="1">Option 1</option>
      <option value="2">Option 2</option>
      <option value="3">Option 3</option>
    </select>
    ```
*   **Variants:**
    *   **Default:** Basic select dropdown.
    *   **With Label:** Associated form label.
        ```html
        <label class="form-label">Example Label</label>
        <select class="select" name="select">...</select>
        ```
    *   **With Hint Text:** Additional guidance below the select.
        ```html
        <select class="select" name="select">...</select>
        <span class="text-xs text-gray-500">Hint text goes here</span>
        ```
    *   **Validation States:** Visual feedback using border colors.
        ```html
        <select class="select border-danger" name="select">...</select> <!-- Error -->
        <select class="select border-success" name="select">...</select> <!-- Success -->
        ```
    *   **Disabled:** Non-interactive state using `disabled` attribute.
        ```html
        <select class="select" disabled name="select">...</select>
        ```
    *   **Sizes:** Adjust select field size.
        ```html
        <select class="select select-sm" name="select">...</select> <!-- Small -->
        <select class="select" name="select">...</select>           <!-- Default -->
        <select class="select select-lg" name="select">...</select> <!-- Large -->
        ```
*   **Key Classes:**
    *   `select`: Base class for styling.
    *   Size variants: `select-sm`, `select-lg`.
    *   Validation state classes: `border-danger`, `border-success`.
*   **Usage Notes:**
    *   Uses standard HTML `<select>` and `<option>` elements.
    *   For advanced features like search and multi-select, consider using a dedicated JavaScript library (e.g., Tom Select, Select2) and styling it to match, or wait for potential future Metronic Advanced Select component.

---

### 4.9. Switch

*   **Description:** A custom toggle switch, visually distinct from a checkbox, representing binary states (on/off). ([Metronic Switch Docs](https://keenthemes.com/metronic/tailwind/docs/components/switch))
*   **HTML Structure:**
    ```html
    <label class="switch">
      <input name="check" type="checkbox" value="1"/>
      <span class="switch-label">Switch Label</span>
    </label>
    ```
*   **Variants:**
    *   **Default:** Basic switch.
    *   **Label Position:** Control label placement with `order-*` utilities.
        ```html
        <label class="switch">
          <input class="order-2" name="check" type="checkbox"/>
          <span class="switch-label order-1">Label First</span>
        </label>
        ```
    *   **Checked:** Use `checked` attribute for default on state.
    *   **Disabled:** Use `disabled` attribute.
    *   **Sizes:** Adjust switch size.
        ```html
        <label class="switch switch-sm">...</label> <!-- Small -->
        <label class="switch">...</label>           <!-- Default -->
        <label class="switch switch-lg">...</label> <!-- Large -->
        ```
*   **Key Classes:**
    *   `switch`: Main label container class.
    *   `switch-label`: Text label part.
    *   Size variants: `switch-sm`, `switch-lg`.
*   **HTML Attributes:**
    *   Standard `checked` and `disabled` attributes on the hidden `input`.
*   **Usage Notes:**
    *   Functionally similar to a checkbox but offers a different visual style.
    *   The actual `input` element is visually hidden and styled through the `label` and `span`.

---

### 4.10. Textarea

*   **Description:** A custom styled multi-line text input field. ([Metronic Textarea Docs](https://keenthemes.com/metronic/tailwind/docs/components/textarea))
*   **HTML Structure:**
    ```html
    <textarea class="textarea" name="notes" placeholder="Enter notes..."></textarea>
    ```
*   **Variants:**
    *   **Default:** Basic textarea.
    *   **With Label & Hint:**
        ```html
        <label class="form-label">Description</label>
        <textarea class="textarea" name="desc"></textarea>
        <span class="text-xs text-gray-500">Provide more details.</span>
        ```
    *   **Rows:** Control default height using `rows` attribute.
        ```html
        <textarea class="textarea" rows="5"></textarea>
        ```
    *   **Disabled:** Non-interactive state.
        ```html
        <textarea class="textarea" disabled></textarea>
        ```
    *   **Readonly:** Value cannot be changed.
        ```html
        <textarea class="textarea" readonly>Readonly content.</textarea>
        ```
    *   **Validation States:** Visual feedback using border colors.
        ```html
        <textarea class="textarea border-danger"></textarea> <!-- Error -->
        <textarea class="textarea border-success"></textarea> <!-- Success -->
        ```
    *   **Sizes:** Adjust textarea size.
        ```html
        <textarea class="textarea textarea-sm"></textarea> <!-- Small -->
        <textarea class="textarea"></textarea>           <!-- Default -->
        <textarea class="textarea textarea-lg"></textarea> <!-- Large -->
        ```
*   **Key Classes:**
    *   `textarea`: Base class for styling.
    *   Size variants: `textarea-sm`, `textarea-lg`.
    *   Validation state classes: `border-danger`, `border-success`.
*   **HTML Attributes:**
    *   Standard `rows`, `disabled`, `readonly`, `placeholder`, `name` attributes.
*   **Usage Notes:**
    *   Default styling allows vertical resizing by the user.

---

### 4.11. Toggle Password

*   **Description:** Enhances a password input field with a toggle button to show/hide the password text. ([Metronic Toggle Password Docs](https://keenthemes.com/metronic/tailwind/docs/components/toggle-password))
*   **HTML Structure:**
    ```html
    <div class="input-group" data-toggle-password="true">
      <input class="input" type="password" placeholder="Password" name="password"/>
      <button type="button" class="btn btn-icon btn-light">
        <i class="ki-outline ki-eye-slash toggle-password-active:hidden"></i>
        <i class="ki-outline ki-eye hidden toggle-password-active:inline-block"></i>
      </button>
    </div>
    ```
*   **Key Data Attributes:**
    *   `data-toggle-password="true"`: Enable auto-initialization on the parent container (usually `input-group`).
*   **Key Classes:**
    *   `toggle-password-active:hidden`: Utility to hide icon when password *is* visible.
    *   `toggle-password-active:inline-block` (or similar): Utility to show icon when password *is* visible.
    *   Requires `input-group` structure for proper layout.
*   **JS Initialization:**
    *   **Auto:** Use `data-toggle-password="true"` on the container.
    *   **Manual:** Use JavaScript:
        ```javascript
        const togglePasswordEl = document.querySelector('#my_password_group');
        const togglePassword = new KTTogglePassword(togglePasswordEl);
        ```
*   **JS Methods:**
    *   `toggle()`: Programmatically toggle password visibility.
    *   `isVisible()`: Check if password text is currently visible.
    *   Other utility methods: `getOption()`, `getElement()`, `dispose()`.
*   **JS Events:**
    *   `toggle`: Before visibility changes (cancelable).
    *   `toggled`: After visibility changes.
*   **Usage Notes:**
    *   Relies on the `input-group` structure.
    *   Uses utility classes (`toggle-password-active:*`) applied to the toggle *button* to switch the icon appearance based on the state managed by the JS component.

---
*(End of Form Components)* 