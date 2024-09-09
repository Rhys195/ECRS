
document.addEventListener('DOMContentLoaded', () => {
    // Show modal if URL hash is #authModal
    const authModal = document.getElementById('authModal');
    if (window.location.hash === '#authModal') {
        const modal = new bootstrap.Modal(authModal);
        modal.show();

        // Hide the modal after 3 seconds
        setTimeout(() => {
            modal.hide();
            // Optionally, remove the hash from the URL after hiding the modal
            history.replaceState(null, null, window.location.pathname);
        },)
    }

    // Show toast messages
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toastElement => {
        // Create a new Toast instance with custom options
        const toast = new bootstrap.Toast(toastElement, {
            animation: true,
            autohide: true,
            delay: 2000  // 3000 milliseconds = 3 seconds
        });
        toast.show();
    });
});

