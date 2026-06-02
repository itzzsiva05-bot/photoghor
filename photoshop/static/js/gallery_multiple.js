// static/admin/js/gallery_multiple.js
// Enables multiple file selection and injects a Category dropdown
// into the Django admin "Add Gallery" page.

(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {

    // ── 1. Allow multiple file selection on the image input ──────────────
    var imageInput = document.querySelector('input[name="image"]');
    if (imageInput) {
      imageInput.setAttribute("multiple", "multiple");
    }

    // ── 2. Inject a Category <select> above the image field ──────────────
    // Django renders category choices via the normal form, but since we
    // bypass the ModelForm in add_view we need to inject it manually.
    // The select posts as 'category' which matches request.POST.get('category').

    var form = document.querySelector("#content-main form");
    if (!form) return;

    // Fetch category choices from the inline JSON block Django puts on the page,
    // or fall back to an AJAX call to a simple endpoint if you add one later.
    // For now we read them from the existing Django-rendered select (if present)
    // and re-use it — or build the widget fresh.

    var existingSelect = form.querySelector('select[name="category"]');
    if (existingSelect) {
      // Django already rendered it via the normal ModelForm path — nothing to do.
      styleSelect(existingSelect);
      return;
    }

    // No select rendered (because add_view bypasses the normal form).
    // Fetch the category list via the Django admin autocomplete JSON endpoint.
    fetch("/admin/photoshop/category/?_to_field=id&_as_choice_widget=1", {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        buildCategorySelect(form, data.results || []);
      })
      .catch(function () {
        // Fallback: render an empty select so the field still posts.
        buildCategorySelect(form, []);
      });
  });


  // ── Helpers ──────────────────────────────────────────────────────────────

  function buildCategorySelect(form, choices) {
    var wrapper = document.createElement("div");
    wrapper.className = "form-row field-category";
    wrapper.style.cssText = "padding: 8px 0; display: flex; align-items: center; gap: 12px;";

    var label = document.createElement("label");
    label.textContent = "Category:";
    label.style.cssText = "font-weight: bold; min-width: 120px;";

    var select = document.createElement("select");
    select.name = "category";
    styleSelect(select);

    // Blank / optional option
    var blank = document.createElement("option");
    blank.value = "";
    blank.textContent = "---------";
    select.appendChild(blank);

    choices.forEach(function (c) {
      var opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.text;
      select.appendChild(opt);
    });

    wrapper.appendChild(label);
    wrapper.appendChild(select);

    // Insert before the image field row
    var imageRow = form.querySelector(".field-image") || form.querySelector("input[name='image']");
    if (imageRow && imageRow.closest) {
      imageRow = imageRow.closest(".form-row") || imageRow.parentNode;
    }
    form.insertBefore(wrapper, imageRow || form.firstChild);
  }

  function styleSelect(select) {
    select.style.cssText =
      "padding: 6px 10px; border: 1px solid #ccc; border-radius: 4px;" +
      "font-size: 14px; min-width: 200px; background: #fff;";
  }

})();