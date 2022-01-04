var date = (document.getElementById("date").innerHTML = new Date().getFullYear());
var navBtn = document.getElementById("nav-btn");
var navbar = document.getElementById("navbar");
var navClose = document.getElementById("nav-close");
var updateBtns = document.getElementsByClassName('update-cart');


navBtn.addEventListener("click", () => {
    navbar.classList.add("showNav");
});

navClose.addEventListener("click", () => {
    navbar.classList.remove("showNav")
})

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)

        
        console.log('USER', user)
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action) {
    console.log('User is not authenticated')

    if (action == 'add') {
        if (cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 1) {
            console.log('remove item')
            delete cart[productId]
        }
    }
    console.log('cart:', cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    location.reload()
    // try to fix this
}


function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...')

    var url = 'update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
       return response.json();
    })
    .then((data) => {
        console.log('Data:', data)
        location.reload()
    });
}


  //setup date


// hamburger.addEventListener('click',()=> {
//     hamburger.classList.toggle('active');
//     mobile_menu.classList.toggle('active');
// });

// document.addEventListener('scroll', ()=> {
//     let scroll_position = window.scrollY
//     if(scroll_position > 250){
//         header.style.backgroundColor = "#29323c";
//     }else{
//         header.style.backgroundColor = "transparent";
//     }
// });

// menu_item.forEach((item) => {
//     item.addEventListener('click', () => {
//         hamburger.classList.toggle('active');
//         mobile_menu.classList.toggle('active');
//     });
// });

// console.log(updateBtns)



