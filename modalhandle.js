$(document).ready(function() {

    // Handle tab switching and reset fields
    $('a[data-toggle="tab"]').on('click', function() {
        var $currentTab = $(this).attr('href');
        $('.tab-pane').each(function() {
            if ($(this).attr('id') !== $currentTab.substring(1)) {
                $(this).find('form')[0].reset();
            }
        });
    });

    // Initially hide the Forgot Password tab and its content
    $('#forgotPassword').hide();
    $('#forgot-password-tab').hide();

    // Handle click on the "Forgot Password?" link
    $('#forgotPasswordLink').on('click', function(event) {
        event.preventDefault();  // Prevent default link behavior

        // Show the Forgot Password tab and switch to it
        $('#forgot-password-tab').show();
        $('#authTabs a[href="#forgotPassword"]').tab('show');

        // Show the Forgot Password tab content
        $('#forgotPassword').show();
    });

    // Handle tab changes to ensure "Forgot Password" tab is hidden
    $('#authTabs a').on('click', function() {
        // Hide the "Forgot Password" tab and header when switching to other tabs
        if ($(this).attr('id') !== 'forgot-password-tab') {
            $('#forgotPassword').hide();
            $('#forgot-password-tab').hide();
        }
    });

    // Handle the Forgot Password form submission
    $('#forgotPasswordForm').on('submit', function(e) {
        e.preventDefault();
        var email = $('#forgotPasswordEmail').val();

        fetch('/send_forgot_password_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ 'email': email })
        }).then(response => response.json())
          .then(data => {
              showToast(data);
              if (data.status === 'success') {
                  $('#forgotPasswordOtpFormContainer').show();
                  $('#forgotPasswordFormContainer').hide();
              }
          });
    });

    // Handle OTP verification
    $('#verifyOtpButton').on('click', function() {
        var otp = $('#forgotPasswordOtp').val();

        fetch('/verify_forgot_password_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ 'otp': otp })
        }).then(response => response.json())
          .then(data => {
              showToast(data);
              if (data.status === 'success') {
                  $('#resetPasswordFormContainer').show();
                  $('#forgotPasswordOtpFormContainer').hide();
              }
          });
    });

    // Handle the Reset Password form submission
    $('#resetPasswordForm').on('submit', function(e) {
        e.preventDefault();
        var otp = $('#forgotPasswordOtp').val();
        var newPassword = $('#newPassword').val();

        fetch('/reset_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'otp': otp,
                'newPassword': newPassword
            })
        }).then(response => response.json())
          .then(data => {
              showToast(data);
              if (data.status === 'success') {
                  $('#forgotPassword').hide();
                  $('#forgot-password-tab').hide();
                  $('#signin-tab').tab('show');  // Switch to the Sign-In tab
              }
          });
    });

    // Function to display toast messages
    function showToast(data) {
        var toastContainer = $('.toast-container');

        var toastHtml = `
            <div class="toast align-items-center text-bg-${data.status} border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${data.message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;

        toastContainer.append(toastHtml);

var toastElement = toastContainer.find('.toast').last();
var toast = new bootstrap.Toast(toastElement[0], {
    delay: 3000  // Set delay to 7 seconds (7000 milliseconds)
});
toast.show();

toastElement.on('hidden.bs.toast', function () {
    toastElement.remove();
});
    }
});
