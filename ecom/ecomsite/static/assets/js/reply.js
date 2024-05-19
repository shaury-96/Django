
   



document.addEventListener('DOMContentLoaded', function() {



    const replyButtons = document.querySelectorAll('.reply-btn');
    replyButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); 
            
            const replyForm = button.nextElementSibling;
            replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
        });
    });

    const postButtons = document.querySelectorAll('.post-btn');
    const csrftoken = document.getElementById('csrf_token').value;

    postButtons.forEach(button => {
        button.addEventListener('click', function() {
            const reviewId = button.getAttribute('reviewId');
            const productId = button.getAttribute('pid');
            const replyText = button.parentElement.querySelector('.reply-text').value;
            
            console.log(reviewId, productId, replyText);
            fetch('reply/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ reviewId: reviewId, replyText: replyText, productId: productId })
            })
            .then(response => {
                console.log(response);
                if (response.ok) {
                    console.log('Reply submitted successfully!');
                } else {
                    console.error('Failed to submit reply.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });





    

});
