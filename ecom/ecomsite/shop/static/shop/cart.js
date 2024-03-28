
console.log('This is working');
 
    if(localStorage.getItem('cart')==null){
        var cart = {};
    }
    else{
        cart = JSON.parse(localStorage.getItem('cart'));
        document.getElementById("cart").innerText="Cart("+ Object.keys(cart).length +")";
        DisplayCart(cart);
    }
    
 
    document.addEventListener('click',function(event){
      if(event.target.classList.contains('atc')) {
        console.log("The add to cart button is clicked");
        var item_id = event.target.id.toString();
        console.log(item_id);
 
        if(cart[item_id]!=undefined)
        {
            quantity = cart[item_id][0] + 1;
            cart[item_id][0] = quantity;
            cart[item_id][2] = cart[item_id][2] + parseFloat(document.getElementById("price"+item_id).innerHTML);
        }
        else
        {
            quantity = 1;
            price = parseFloat(document.getElementById("price"+item_id).innerHTML);
            name = document.getElementById("nm"+item_id).innerHTML;
            cart[item_id]=[quantity,name,price];
        }
        console.log(cart);
        localStorage.setItem('cart',JSON.stringify(cart));
        document.getElementById("cart").innerHTML = "Cart("+ Object.keys(cart).length +")";
        DisplayCart(cart);
      }
      
       
    });
 
    // document.addEventListener('click',DisplayCart(cart));
    function DisplayCart(cart){
        var cartString ="";
        cartString += "<h5>This is your cart</h5>";
        var cartIndex = 1;
        for(var x in cart)
        {
            cartString += cartIndex;
            cartString += document.getElementById("nm"+x).innerHTML + "Qty:" + cart[x][0] + "</br>";
            cartIndex+=1;
        }
 
        cartString += "<a href='/checkout'><button class='btn btn-warning' id='checkout'>Checkout</button></a>";

        document.getElementById("cart").setAttribute('data-content',cartString);
        // $('[data-toggle="popover"]').popover();

        var elements = document.querySelectorAll('[data-toggle="popover"]');

        elements.forEach(function(element) {
            element.addEventListener('click', function() {
                var popoverContent = this.getAttribute('data-content');
                var popover = document.createElement('div');
                popover.classList.add('popover');
                popover.innerHTML = popoverContent;
                
                // Position the popover relative to the clicked element
                var rect = this.getBoundingClientRect();
                popover.style.position = 'absolute';
                popover.style.left = rect.left + 'px';
                popover.style.top = rect.bottom + 'px';
                
                document.body.appendChild(popover);
                
                // Close popover when clicking outside
                document.addEventListener('click', function(event) {
                    if (!popover.contains(event.target) && event.target !== element) {
                        popover.remove();
                    }
                });
            });
        });

    }