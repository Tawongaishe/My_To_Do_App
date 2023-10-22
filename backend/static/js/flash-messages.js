// JavaScript
document.addEventListener("DOMContentLoaded", function () {
    const flashMessage = document.querySelectorAll("flash-message");

    function showFlashMessage(message) {
        flashMessage.textContent = message;
        flashMessage.style.display = "block";
        setTimeout(function () {
            flashMessage.style.display = "none";
        }, 5000); // Adjust the timeout (in milliseconds) as needed
    }

    const flashMessages = document.querySelectorAll(".flash-message");

    if (flashMessages.length > 0) {
        showFlashMessage(flashMessages[flashMessages.length - 1].textContent);
    }
});
