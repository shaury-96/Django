$("#add-to-cart").on("click",function(){
    let quantity=$("#product-quantity").val()
    let product_title=$(".product-title").val()
    let product_id=$(".product-id").val()
    let product_price=$(".product-price").val()

    if(quantity<=0)
        return;

    console.log(quantity,product_id,product_title,product_price)

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'qty': quantity,
            'title': product_title,
            'price': product_price
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Adding items...");
        },
        success:function(response){
            $(this).html("added");
            console.log("Item added to the cart");
            $(".cart-count").text(response.totalcartitems);
        }
    })

})