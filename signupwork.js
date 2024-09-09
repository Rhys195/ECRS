  $(document).ready(function() {
    // Handle form submission
    $('#signupForm').on('submit', function(event) {
        event.preventDefault();  // Prevent default form submission

        // First, verify the CAPTCHA
        $.ajax({
            url: '/verify_captcha',
            method: 'POST',
            data: $(this).serialize(),  // Serialize form data
            success: function(captchaResponse) {
                if (captchaResponse.status === 'success') {
                    // CAPTCHA verified, proceed with form submission
                    $.ajax({
                        url: '/signup',
                        method: 'POST',
                        data: $('#signupForm').serialize(),
                        success: function(signupResponse) {
                            console.log("Sign-up response:", signupResponse);
                            if (signupResponse.status === 'success') {
                                $('#otpFormContainer').show();
                            } else {
                                alert('Error: ' + signupResponse.message);
                            }
                        },
                        error: function(xhr, status, error) {
                            console.log("AJAX Error:", error);
                        }
                    });
                } else {
                    alert('Error: ' + captchaResponse.message);

                    // Refresh CAPTCHA image
                    $('#captchaImage').attr('src', '/generate_captcha_image?' + new Date().getTime());
                }
            },
            error: function(xhr, status, error) {
                console.log("AJAX Error:", error);
            }
        });
    });
});

 $(document).ready(function() {
    // Handle sign-up form submission
    $('#signupForm').on('submit', function(event) {
        event.preventDefault();  // Prevent default form submission
        $.ajax({
            url: '/signup',  // Flask route for sign-up
            method: 'POST',
            data: $(this).serialize(),  // Serialize form data
            success: function(response) {
                console.log("Sign-up response:", response);
                if (response.status === 'success') {

                    // Keep signup form visible and show OTP form below
                    $('#otpFormContainer').show();
                } else {
                    alert('Error: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                console.log("AJAX Error:", error);
            }
        });
    });

    // Handle OTP form submission
    $('#otpForm').on('submit', function(event) {
        event.preventDefault();  // Prevent default form submission
        $.ajax({
            url: '/verify_otp',  // Flask route for OTP verification
            method: 'POST',
            data: $(this).serialize(),  // Serialize form data
            success: function(response) {
                if (response.status === 'success') {
                    alert(response.message);  // Success message
                    $('#signupModal').modal('hide');  // Close modal on successful verification

                    // Clear the sign-up form fields
                    $('#signupForm')[0].reset();
                    $('#otpFormContainer').hide().find('form')[0].reset();

                       $('#signin-tab').tab('show');  // Switch to Sign-In tab
                } else {
                    alert(response.message);  // Show error message
                }
            },
            error: function(xhr, status, error) {
                console.log("AJAX Error:", error);
            }
        });
    });
});
