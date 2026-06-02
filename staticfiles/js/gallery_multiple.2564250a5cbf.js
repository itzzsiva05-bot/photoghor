// image input-ஐ multiple ஆக மாற்றுகிறோம்
document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('input[name="image"]');
    if (input) {
        input.setAttribute('multiple', true);
    }
});