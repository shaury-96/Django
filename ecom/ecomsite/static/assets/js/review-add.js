console.log("Hello")

$("#reviewForm").submit(function(e){
    e.preventDefault();
    console.log("Form Submitted")

    $.ajax({
        
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        data: $(this).serialize(),    
        dataType: "json",

        success: function(response){
            console.log(response, "review added");

            if(response.bool == true){
                

                let newReview=
                '<div class="review">'+
                '<div class="review-header">'+

                '<div class="user-icon">'+
                '<img src="https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png" alt="User Icon">'+
                '</div>'+
                '<div class="review-info">'+

                '<div class="review-date"><strong>'+ response.context.user.username + '</strong>' + response.context.date

                
                for(let i=1;i<=response.context.rating;i++)
                newReview+='<i class="fas fa-star text-warning"></i>';
                
                newReview+=       
                '</div>'+
                '<div class="review-rating">'+
                           
                '</div>'+
                '</div>'+
                '</div>'+
                '<div class="review-body">'+
                response.context.review+
                '</div>'+
                '<a href="#" class="reply-btn">Reply</a>'+

                '</div>'
                
            
            $(".review-section").prepend(newReview);
            $("#review-response").html("Review posted Successfully");
            $("#reviewForm").hide();
            $("#no-review").hide();
          
            }

        },
        error: function(xhr, status, error) {
            console.log("Error: " + error);
            console.log("Status: " + status);
            console.log(xhr.responseText);
        }
    })
})

