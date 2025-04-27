# Metronic Plugins

[Back to Metronic Guide Index](index.md)

---

## 5. Plugins

This section covers integrated 3rd-party plugins provided with Metronic.

### 5.1. ApexCharts

*   **Description:** A modern JavaScript charting library for creating interactive visualizations. Metronic provides customized styling to integrate seamlessly with the theme. ([Metronic ApexCharts Docs](https://keenthemes.com/metronic/tailwind/docs/plugins/apexcharts))
*   **Installation:** Included as a vendor dependency. Compiled assets are in `dist/assets/vendors/apexcharts/`.
*   **Required Assets:**
    *   CSS: `/dist/assets/vendors/apexcharts/apexcharts.css` (Include before main `styles.css`)
    *   JS: `/dist/assets/vendors/apexcharts/apexcharts.min.js` (Include after `core.bundle.js`)
*   **Usage (Example - Area Chart):**
    ```html
    <!-- Chart container -->
    <div id="area_chart"></div>
    ```
    ```javascript
    // Basic Area Chart Example
    const element = document.querySelector('#area_chart');
    if (element) {
      const options = {
        series: [{
          name: 'Sales',
          data: [30, 40, 35, 50, 49, 60, 70, 91, 125]
        }],
        chart: {
          height: 350,
          type: 'area',
          toolbar: { show: false }
        },
        // Use Metronic CSS variables for colors
        colors: ['var(--tw-primary)'],
        stroke: {
          curve: 'smooth',
          width: 3,
          colors: ['var(--tw-primary)']
        },
        dataLabels: { enabled: false },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
          labels: { style: { colors: 'var(--tw-gray-500)' } },
          axisBorder: { show: false },
          axisTicks: { show: false }
        },
        yaxis: {
          labels: { style: { colors: 'var(--tw-gray-500)' } }
        },
        grid: {
          borderColor: 'var(--tw-gray-200)',
          strokeDashArray: 4,
          yaxis: { lines: { show: true } }
        },
        tooltip: {
          // Custom tooltip styling/formatter possible here
        },
        fill: {
          gradient: {
            enabled: true,
            opacityFrom: 0.25,
            opacityTo: 0
          }
        },
        markers: { // Customized hover markers
          strokeColors: 'var(--tw-primary)',
          colors: 'var(--tw-light)',
          strokeWidth: 3
        }
      };
      
      const chart = new ApexCharts(element, options);
      chart.render();
    }
    ```
*   **Customization:** Metronic includes a Tailwind plugin (`src/core/plugins/components/apexcharts.js`) to style charts according to the theme. Use CSS variables (e.g., `var(--tw-primary)`, `var(--tw-gray-500)`) in chart options for consistency.
*   **Usage Notes:**
    *   Refer to the official ApexCharts documentation for the full range of chart types and options.
    *   Metronic demos provide specific examples (like Area, Pie charts) in files like `dist/assets/pages/plugins/apexcharts/`. 

---

### 5.2. Clipboard

*   **Description:** A lightweight utility for copying text to the clipboard without Flash or frameworks. ([Metronic Clipboard Docs](https://keenthemes.com/metronic/tailwind/docs/plugins/clipboard))
*   **Installation:** Included as a vendor dependency. Compiled assets are in `dist/assets/vendors/clipboard/`.
*   **Required Assets:**
    *   JS: `/dist/assets/vendors/clipboard/clipboard.min.js` (Include after `core.bundle.js`)
*   **Usage (Example - Copy from Input):**
    ```html
    <!-- Input field -->
    <input id="clipboard_input" class="input" value="Text to copy"/>
    
    <!-- Trigger button -->
    <button class="btn btn-primary" data-clipboard-target="#clipboard_input">
      Copy
    </button>
    ```
    ```javascript
    // Initialize all clipboard instances
    new ClipboardJS('[data-clipboard-target]');
    
    // Optional: Add feedback on success
    const clipboard = new ClipboardJS('.btn'); // Target your buttons
    clipboard.on('success', function(e) {
        console.log('Copied!', e.text);
        // Provide user feedback (e.g., change button text/icon)
        const originalText = e.trigger.innerHTML;
        e.trigger.innerHTML = 'Copied!';
        setTimeout(() => { e.trigger.innerHTML = originalText; }, 2000);
        e.clearSelection();
    });
    clipboard.on('error', function(e) {
        console.error('Copy failed', e.action);
        // Provide error feedback
    });
    ```
*   **Key Data Attributes:**
    *   `data-clipboard-target="#id"`: Selector for the element whose content/value to copy.
    *   `data-clipboard-action="copy|cut"`: Action to perform (default: `copy`).
    *   `data-clipboard-text="text"`: Define static text to copy directly.
*   **Usage Notes:**
    *   Initialize using `new ClipboardJS('selector')` where selector matches your trigger elements.
    *   Provide visual feedback to the user on success/error using the `.on('success')` and `.on('error')` event handlers.
    *   Can copy from input/textarea values or the `innerHTML` of any element.

---

### 5.3. KeenIcons

*   **Description:** Metronic's in-house icon set, offering a wide variety of icons in different styles (Outline, Solid, Duotone). ([Metronic KeenIcons Docs](https://keenthemes.com/metronic/tailwind/docs/plugins/keenicons))
*   **Installation:** Core font files and CSS are part of the Metronic build process.
*   **Required Assets:**
    *   CSS: Included within the main `dist/assets/css/styles.css` bundle.
    *   Fonts: Located in `dist/assets/fonts/keenicons/`.
*   **Usage:**
    ```html
    <!-- Outline Style -->
    <i class="ki-outline ki-home"></i>
    <i class="ki-outline ki-user"></i>
    
    <!-- Solid Style -->
    <i class="ki-solid ki-home"></i>
    <i class="ki-solid ki-user"></i>
    
    <!-- Duotone Style (Requires multiple path spans) -->
    <i class="ki-duotone ki-home">
      <span class="path1"></span>
      <span class="path2"></span>
    </i>
    <i class="ki-duotone ki-user">
      <span class="path1"></span>
      <span class="path2"></span>
    </i>
    ```
*   **Key Classes:**
    *   Style prefix: `ki-outline`, `ki-solid`, `ki-duotone`.
    *   Icon name: `ki-{icon-name}` (e.g., `ki-home`, `ki-graph-up`, `ki-calendar`).
    *   For Duotone: Requires nested `<span class="path1"></span>`, `<span class="path2"></span>`, etc. (number of paths varies per icon).
*   **Finding Icons:**
    *   Refer to the KeenIcons preview page in the Metronic documentation or the local `dist/docs/icons/keenicons` pages.
*   **Styling:**
    *   Use Tailwind text color utilities (`text-primary`, `text-gray-500`, etc.).
    *   Use Tailwind font size utilities (`text-lg`, `text-2xl`, etc.).
*   **Usage Notes:**
    *   Use the `<i>` tag for semantic representation of icons.
    *   Duotone icons offer more color customization via CSS targeting `.path1`, `.path2`, etc., but require more complex markup.
    *   Outline and Solid are generally easier to use.

---
Icons list:
Abstract
abstract-33
abstract-27
abstract-26
abstract-32
abstract-18
abstract-24
abstract-30
abstract-8
abstract-9
abstract-31
abstract-25
abstract-19
abstract-21
abstract-35
abstract-34
abstract-20
abstract-36
abstract-22
abstract-23
abstract-37
abstract-44
abstract
abstract-45
abstract-47
abstract-46
abstract-42
abstract-43
abstract-41
abstract-40
abstract-48
abstract-49
abstract-12
abstract-2
abstract-3
abstract-13
abstract-39
abstract-11
abstract-1
abstract-10
abstract-38
abstract-14
abstract-28
abstract-4
abstract-5
abstract-29
abstract-15
abstract-17
abstract-7
abstract-6
abstract-16
Settings
toggle-on
toggle-on-circle
toggle-off
category
setting
toggle-off-circle
more-2
setting-4
setting-2
setting-3
Design
eraser
paintbucket
design-1
design-2
brush
size
disguise
additem
copy
text
bucket
glass
feather
frame
pencil
colors-square
bucket-square
copy-success
color-swatch
Social-media
instagram
snapchat
classmates
facebook
whatsapp
social-media
youtube
dribbble
twitter
tiktok
behance
It-network
underlining
disconnect
wireframe
code
loading
scroll
wrench
square-brackets
message-programming
data
fasten
click
Technologies
joystick
wlan
face-id
technology-3
technology-2
electricity
fingerprint-scanning
technology-1
technology-4
artificial-intelligence
Ecommerce
basket-ok
cheque
handcart
shop
tag
purchase
discount
package
percentage
barcode
lots-shopping
basket
Archive
book-square
receipt-square
save-2
archive-tick
Security
shield-search
password-check
shield-tick
lock
key
shield
shield-cross
key-square
eye-slash
ensure
lock-3
scan-barcode
lock-2
eye
shield-slash
security-user
General
subtitle
ghost
information
milk
home
mouse-square
filter-tick
filter-search
wifi-home
trash-square
paper-clip
archive
pin
wifi-square
coffee
icon
emoji-happy
cursor
ranking
slider
crown-2
rescue
flash-circle
safe-home
cloud-change
crown
paper-plane
filter-edit
picture
verify
tag-cross
autobrightness
cloud-add
home-3
disk
trash
star
cd
home-2
mouse-circle
home-1
call
gift
share
sort
magnifier
filter-square
tree
filter
switch
cloud
cup
diamonds
status
rocket
cloud-download
menu
chrome
happyemoji
Arrow
exit-right-corner
dots-circle-vertical
right-left
arrow-down
dots-horizontal
double-check-circle
arrow-right-left
up-down
plus-squared
arrow-up-left
down
exit-up
up-square
down-square
double-check
dots-circle
arrow-down-left
up
entrance-right
arrow-right
arrow-two-diagonals
black-left
check-squared
arrow-down-refraction
black-right
arrow-circle-left
double-right
double-up
arrow-zigzag
plus
check
exit-left
arrow-circle-right
cross-square
entrance-left
left-square
arrows-loop
black-left-line
double-left-arrow
check-circle
right
dots-square-vertical
up-diagonal
arrow-up-right
exit-down
dots-square
to-left
double-down
plus-circle
double-left
black-down
black-up
double-right-arrow
arrow-up
black-right-line
arrow-up-refraction
arrow-left
cross
minus-circle
arrow-down-right
exit-right
to-right
arrow-mix
right-square
minus-squared
arrows-circle
cross-circle
left
minus
dots-vertical
arrow-up-down
Location
geolocation-home
map
telephone-geolocation
satellite
flag
focus
pointers
compass
route
geolocation
Education
brifecase-timer
briefcase
clipboard
bookmark-2
note
note-2
book-open
book
teacher
award
brifecase-tick
brifecase-cros
bookmark
Business
chart-line
chart
graph-3
chart-pie-3
graph-2
chart-line-down
chart-pie-too
chart-pie-4
chart-line-down-2
graph-4
chart-line-up-2
badge
chart-line-up
chart-simple-3
chart-pie-simple
chart-simple-2
graph-up
chart-line-star
graph
chart-simple
Files-folders
tablet-delete
file-added
file-up
minus-folder
files
delete-files
add-folder
file-left
file-deleted
some-files
file-right
notepad
notepad-bookmark
document
like-folder
folder-up
folder-added
file-down
filter-tablet
tab-tablet
update-file
add-notepad
questionnaire-tablet
tablet-up
tablet-ok
update-folder
folder-down
notepad-edit
tablet-text-up
search-list
tablet-text-down
tablet
add-files
tablet-down
delete-folder
folder
file-sheet
Software
bootstrap
figma
dropbox
xaomi
microsoft
android
vue
js
spring-framework
github
dj
google-play
angular
soft-3
python
soft-2
ts
xd
spotify
js-2
laravel
css
google
photoshop
twitch
illustrator
pails
react
html
slack
soft
yii
apple
vuesax
Time
calendar-add
calendar-search
calendar-2
calendar-tick
time
watch
calendar-edit
calendar
calendar-8
timer
calendar-remove
Delivery-logistics
parcel
delivery-time
delivery
delivery-24
ship
courier
logistic
airplane-square
cube-3
bus
cube-2
delivery-door
delivery-3
delivery-2
car
courier-express
airplane
delivery-geolocation
parcel-tracking
Support
heart-circle
like
information-4
information-1
information-2
information-3
question
dislike
message-question
medal-star
like-tag
support
like-2
question-2
lovely
like-shapes
heart
Users
user
user-square
user-tick
people
user-edit
profile-circle
users
Medicine
capsule
virus
bandage
thermometer
flask
test-tubes
syringe
mask
pill
pulse
Burger-menu
burger-menu
burger-menu-6
burger-menu-5
burger-menu-4
burger-menu-1
burger-menu-3
burger-menu-2
Typography
textalign-left
textalign-justifycenter
text-italic
text-bold
textalign-right
text-strikethrough
text-underline
textalign-center
text-number
text-circle
Finance
dollar
binance
wanchain-wan
avalanche-avax
celsius-cel
nexo
euro
bitcoin
wallet
price-tag
theta-theta
dash
lts
enjin-coin-enj
credit-cart
paypal
bill
ocean
vibe-vibe
two-credit-cart
bank
trello
save-deposit
educare-ekt
binance-usd-busd
xmr
financial-schedule
calculator
office-bag
Weather
night-day
sun
drop
moon
Communication
message-text-2
message-add
sms
directbox-default
message-text
messages
address-book
message-edit
message-minus
message-notify
Notifications
notification-circle
notification-favorite
notification-1
notification
notification-bing
notification-status
notification-on
Devices
pad
desktop-mobile
devices
keyboard
devices-2
bluetooth
wifi
airpod
simcard-2
speaker
printer
simcard
router
phone
electronic-clock
calculatoror
external-drive
laptop
screen
mouse
Grid
grid
fatrows
maximize
bar-chart
slider-vertical
row-horizontal
kanban
slider-vertica
row-vertical
grid-2
element-8
element-9
element-12
element-4
element-5
element-11
element-7
element-6
element-10
element-2
element-3
element-equal
element-1
slider-horizontal-2
slider-horizontal
element-plus
*(End of Plugins)* 