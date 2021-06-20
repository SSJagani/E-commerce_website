var deleteButton = document.getElementsByClassName('delete-items');
for(var i=0; i < deleteButton.length; i++){
	deleteButton[i].addEventListener('click',function(){
		var productId = this.dataset.product
		var url = "product_delete/Ref=*sOur8Cl8s7"

		fetch(url,{
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken,
		},
		body:JSON.stringify({'productId':productId})
		}).then((response)=>{
			return response.json();
		}).then((data)=>{
			console.log('Data:',data)
			location.reload()
	
	});
	})
}


var shippingButton = document.getElementsByClassName('shipping-complete');
for(var i=0; i < shippingButton.length; i++){
	shippingButton[i].addEventListener('click',function(){
		var orderId = this.dataset.order 
		console.log(orderId)	
		var url = "shipping-complete/Ref=!DerRe8F5S6Q"

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
			console.log('Data:',data)
			location.reload()	
	});
	})
}