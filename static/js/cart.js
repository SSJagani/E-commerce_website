function modelhideen() {
	// body...
	$('#loginmodal').modal('hide')
	console.log('model script run...')
}

function checkemail() {
	// body...
	var email = document.getElementById('email').value;
	var url = 'emailcheck'
	fetch(url,{
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken,
		},
		body:JSON.stringify({'email':email})
	}).then((response)=>{
		return response.json();
	}).then((data)=>{
		console.log('Data:',data)
		if(data==2001){
			$('#error_email').attr("style", "color: red; font-weight: bold; display:block")
			console.log("exits")
		}
		if(data==2002){
			console.log("not exits")

		}
	});
}


var updatButton = document.getElementsByClassName('update-cart');
for(var i=0; i < updatButton.length; i++){
	updatButton[i].addEventListener('click',function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('product id: ',productId,'action: ',action)
		console.log('User: ',user)
		if (user == 'AnonymousUser') {
			addCookieItems(productId,action)
		}
		else{
			upadateUserOrder(productId ,action)
			console.log('User is Authenticeted , sending data....')
		}
	})
}

function addCookieItems(productId,action) {
	// body...
	console.log(productId,'===',action)
	if(action == 'add'){
		if(cart[productId] == undefined){
			cart[productId] = {'quantity':1}
		}
		else{
			cart[productId]['quantity'] +=1
		}
	}
	if(action == 'remove'){
		cart[productId]['quantity'] -=1
		if(cart[productId]['quantity']<=0){
			delete cart[productId];
		}
	}
	location.reload()
	console.log('Cart :',cart)
    document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
}

// Update Item fuction
function upadateUserOrder(productId,action) {
	// body...
	console.log(productId,'===',action)
	var url = 'update_item'

	fetch(url,{
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken,
		},
		body:JSON.stringify({'productId':productId,'action':action})
	}).then((response)=>{
		return response.json();
	}).then((data)=>{
		location.reload()
		console.log('Data:',data)
	});
}

var orderCancelButton = document.getElementsByClassName('cancel-order');
for(var i=0; i < orderCancelButton.length; i++){
orderCancelButton[i].addEventListener('click',function() {
	// body...
	var orderId = this.dataset.order
	var url = 'cancel_order'
	fetch(url,{
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken,
		},
		body:JSON.stringify({'orderId':orderId})
	}).then((response)=>{
		return response.json();
	}).then((data)=>{
		location.reload()
		console.log('Data:',data)
	});
})
}
