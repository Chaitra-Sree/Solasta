$(document).ready(function() {
    retrieve_saved_cart();
  
    if (window.location.href.indexOf("cart") > -1) {
        load_cart();
    }
  
    if (window.location.href.indexOf("view-orders") > -1) {
        order_list_functionality();
    }
  });
  
  function order_list_functionality() {
    onRowClick("orders_table", function(row) {
        var id = row.getElementsByTagName("td")[0].innerHTML;
        var csrftoken = getCookie('csrftoken');
  
        check_user_super(function(user_is_super) {
            if (user_is_super && row.classList.contains("mark-as-complete")) {
                var r = confirm("Would you like to mark order " + id + " as delivered?");
                if (r == true) {
                    $.ajax({
                        url: "/mark_order_as_delivered",
                        type: "POST",
                        data: { id: id, csrfmiddlewaretoken: csrftoken },
                        success: function() {
                            row.classList.remove("table-danger");
                            row.classList.add("table-success");
                        },
                        error: function(xhr) {
                            console.error("Failed to mark order as delivered:", xhr.responseText);
                        }
                    });
                }
            }
        });
    });
  }
  
  function check_user_super(callback) {
    $.ajax({
        url: "check_superuser",
        type: 'GET',
        success: function(res) {
            callback(res === "True");
        },
        error: function(xhr) {
            console.error("Failed to check user role:", xhr.responseText);
            callback(false);
        }
    });
  }
  
  function add_to_cart(item) {
    var cart_str = localStorage.getItem("cart");
    var cart = cart_str ? JSON.parse(cart_str) : [];
    
    // Check if the item already exists in the cart
    var itemExists = cart.find(cartItem => cartItem.item_description === item.item_description);
    
    if (!itemExists) {
        cart.push(item);
        localStorage.setItem("cart", JSON.stringify(cart));
        display_notif("add to cart", item);
        load_cart(); // Refresh the cart display
    } else {
        alert("Item already in the cart.");
    }
}

  
  function onRowClick(tableId, callback) {
    let table = document.getElementById(tableId);
    if (table) {
        let rows = table.getElementsByTagName("tr");
        for (let row of rows) {
            row.onclick = function() {
                callback(row);
            };
        }
    }
  }
  
  function display_notif(type, info = "No info provided") {
    toastr.options = {
        "closeButton": true,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "timeOut": "2000",
        "extendedTimeOut": "500"
    };
  
    switch (type) {
        case "add to cart":
            toastr.success(info.item_description + ': ₹' + info.price, 'Added to Cart');
            break;
        case "remove from cart":
            toastr.warning("Successfully removed " + info + " from cart");
            break;
        case "new order":
            toastr.success("Order successfully placed");
            break;
        default:
            toastr.info("Action performed successfully.");
    }
  }
  
  function load_cart() {
    var cart_str = localStorage.getItem("cart");
    var cartContainer = document.getElementById("cart-items");
    var cartBody = document.getElementById("cart_body");

    if (cart_str) {
        try {
            var cart = JSON.parse(cart_str);
            
            // Clear existing items in the cart display
            cartBody.innerHTML = "";

            if (cart.length === 0) {
                // Show empty cart message
                cartBody.innerHTML = `<tr><td colspan="4">Your cart is empty!</td></tr>`;
                document.getElementById("checkout_button").disabled = true; // Disable checkout button
            } else {
                // Populate cart items
                cart.forEach((item, index) => {
                    let row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${index + 1}</td> 
                        <td>${item.item_description || "N/A"}</td>
                        <td class="price">${parseFloat(item.price).toFixed(2) || "0.00"}</td>
                        <td><button onclick="remove_from_cart('${item.item_description}')">Remove</button></td>
                    `;
                    cartBody.appendChild(row);
                });
                document.getElementById("checkout_button").disabled = false; // Enable checkout button
            }
        } catch (e) {
            console.error("Error parsing cart data:", e);
        }
    } else {
        // Handle case when cart is not initialized
        cartBody.innerHTML = `<tr><td colspan="4">Your cart is empty!</td></tr>`;
        document.getElementById("checkout_button").disabled = true;
    }

    // Update the total amount
    updateTotal();
}


function clear_cart() {
    localStorage.removeItem("cart");
    localStorage.removeItem("total_price");
    load_cart(); // Refresh cart to show it's empty
}

  
  function display_empty_cart() {
    document.getElementById('cart-items').innerHTML = "<p>Cart is empty!</p>";
    document.getElementById('total').innerHTML = "";
    document.getElementById("checkout_button").disabled = true;
}

  function checkout() {
    var cart = localStorage.getItem("cart");
    var price_of_cart = localStorage.getItem("total_price");
    var csrftoken = getCookie('csrftoken');
  
    $.ajax({
        url: "/checkout",
        type: "POST",
        data: { cart: cart, price_of_cart: price_of_cart, csrfmiddlewaretoken: csrftoken },
        success: function() {
            display_notif("new order");
            clear_cart();
        },
        error: function(xhr) {
            console.error("Checkout failed:", xhr.responseText);
        }
    });
  }
  
  function logout() {
    var current_cart = localStorage.getItem("cart");
    var csrftoken = getCookie('csrftoken');

    console.log("Current cart:", current_cart);
    console.log("Sending logout request...");

    $.ajax({
        url: "/save_cart",
        type: "POST",
        data: { cart: current_cart, csrfmiddlewaretoken: csrftoken },
        success: function() {
            console.log("Cart saved successfully.");
            localStorage.removeItem("cart");
            localStorage.setItem('cart_retrieved', false);
            console.log("Redirecting to logout...");
            window.location.href = "/logout";
        },
        error: function(xhr) {
            console.error("Logout failed:", xhr.responseText);
        }
    });
}

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie) {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.split('=')[1]);
            }
        });
    }
    return cookieValue;
  }

  function remove_from_cart(item_description) {
    var cart_str = localStorage.getItem("cart");
    if (cart_str) {
        var cart = JSON.parse(cart_str);
        
        // Filter out the item to be removed
        cart = cart.filter(item => item.item_description !== item_description);
        
        // Update localStorage
        localStorage.setItem("cart", JSON.stringify(cart));
        
        // Display notification
        display_notif("remove from cart", item_description);
        
        // Update the UI dynamically
        let cartBody = document.getElementById('cart_body');
        let rows = cartBody.querySelectorAll('tr');
        rows.forEach(row => {
            if (row.innerText.includes(item_description)) {
                cartBody.removeChild(row); // Remove the matching row
            }
        });

        // Update the total amount
        updateTotal();
    }
}


