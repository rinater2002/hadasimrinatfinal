// פונקציה של טעינת הזמנות
function loadOrders() {
    fetch('http://127.0.0.1:5000/get_orders')
        .then(response => response.json())
        .then(orders => {
            document.getElementById("ordersContainer").innerHTML = '';

            orders.forEach(order => {
                const orderDiv = document.createElement("div");
                orderDiv.classList.add("order");
                orderDiv.id = order._id; 

                const supplier = document.createElement("h3");
                supplier.textContent = `ספק: ${order.supplier}`;
                orderDiv.appendChild(supplier);

                const productList = document.createElement("ul");
                order.products.forEach(product => {
                    const li = document.createElement("li");
                    li.textContent = product; 
                    productList.appendChild(li);
                });
                orderDiv.appendChild(productList);

                const status = document.createElement("p");
                status.textContent = `סטטוס: ${order.status || "לא ידוע"}`;
                orderDiv.appendChild(status);

              
                if (order.status === "מאושר") {
                    const deleteBtn = document.createElement("button");
                    deleteBtn.textContent = "מחק הזמנה";
                    deleteBtn.onclick = () => deleteOrder(order._id, orderDiv); // מעביר את ה-div של ההזמנה למחיקה
                    orderDiv.appendChild(deleteBtn);
                }

                document.getElementById("ordersContainer").appendChild(orderDiv);
            });
        })
        .catch(error => console.error('Error loading orders:', error));
}

// פונקציה למחוק הזמנה
function deleteOrder(orderId, orderDiv) {
    fetch(`http://127.0.0.1:5000/delete_order/${orderId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("ההזמנה נמחקה בהצלחה");
            orderDiv.remove(); 
        } else {
            alert("לא ניתן למחוק את ההזמנה");
        }
    })
    .catch(error => console.error('Error deleting order:', error));
}

// טוען את ההזמנות בזמן טעינת הדף
window.onload = loadOrders;
