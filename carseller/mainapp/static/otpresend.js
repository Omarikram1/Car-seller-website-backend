
document.addEventListener( "DOMContentLoaded",function() {
    let countdown = parseInt(document.getElementById('time').innerText);
    let timer = document.getElementById('time');
    let resendButton = document.getElementById('resend-otp');
    let spent_time = 0;  // Track how much time has passed

    // Fallback to 30 seconds if remaining time is not set properly
    if (isNaN(countdown|| countdown <= 0)) {
        countdown =30;
    }
    
    // Start countdown
    let interval = setInterval(function() {
        countdown--;
        spent_time++;  // Track time spent
        timer.innerText = countdown;

        if (countdown <= 0) {
            clearInterval(interval);
            resendButton.disabled = false;  // Enable resend button
        }
    }, 1000);  // Update every second

    // Handle OTP submission
    document.querySelector('form').addEventListener('submit', function(event) {
        const hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'spent_time');
        hiddenInput.setAttribute('value', spent_time);
        this.appendChild(hiddenInput);  // Append hidden input to form
    });

    // Function to resend OTP and restart the timer
    window.resendOtp = function() {

        console.log("Resend OTP function triggered");
        console.log("Inside resenad otp")
        resendButton.disabled = true;  // Disable resend button
        countdown = 30;
        spent_time = 0;
        timer.innerText = countdown;

        // Reset the timer
        let interval = setInterval(function() {
            countdown--;
            spent_time++;
            timer.innerText = countdown;
            if (countdown <= 0) {
                clearInterval(interval);
                resendButton.disabled = false;
            }
        }, 1000);
        console.log(getCookie('csrftoken')); 
        // Send request to regenerate OTP
        fetch("/resend_otp/", {  // Ensure you have a trailing slash here to match Django's URL routing
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'resend': true }),
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('OTP has been resent.');
            } else {
                alert('Failed to resend OTP.');
            }
        }).catch(error => {
            console.error('Error resending OTP:', error);
        });
    };

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});