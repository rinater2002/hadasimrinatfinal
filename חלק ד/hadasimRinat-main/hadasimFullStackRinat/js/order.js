document.addEventListener("DOMContentLoaded", function () {
    fetch('http://127.0.0.1:5000/get_suppliers')
        .then(res => res.json())
        .then(data => {
            const suppliers = data;

            const supplierSelect = document.getElementById("supplierSelect");
            const productListDiv = document.getElementById("productList");
            const productItemsContainer = document.getElementById("productItems");
            const afterOrderOptionsDiv = document.getElementById("afterOrderOptions");
            const newOrderBtn = document.getElementById("newOrderBtn");
            const goHomeBtn = document.getElementById("goHomeBtn");

            // טען ספקים לתוך הרשימה
            for (let supplierName in suppliers) {
                const option = document.createElement("option");
                option.value = supplierName;
                option.textContent = supplierName;
                supplierSelect.appendChild(option);
            }

            // שינוי ספק - טען מוצרים מתאימים
            supplierSelect.addEventListener("change", function () {
                const selected = this.value;
                const rawProducts = suppliers[selected];

                // נקה מוצרים קודמים
                productItemsContainer.innerHTML = "";

                let products = [];

                if (typeof rawProducts === "string") {
                    products = rawProducts.split(',').map(p => p.trim());
                } else if (Array.isArray(rawProducts)) {
                    products = rawProducts;
                }

                if (products.length > 0) {
                    productListDiv.classList.remove("hidden");

                    products.forEach(productName => {
                        const label = document.createElement("label");
                        label.style.display = "block";

                        const checkbox = document.createElement("input");
                        checkbox.type = "checkbox";
                        checkbox.value = productName;

                        label.appendChild(checkbox);
                        label.append(" " + productName);

                        productItemsContainer.appendChild(label);
                    });
                } else {
                    productListDiv.classList.add("hidden");
                }
            });

            // שליחת הזמנה
            const submitBtn = document.getElementById("submitOrderBtn");
            submitBtn.addEventListener("click", function () {
                const selectedSupplier = supplierSelect.value;
                const checkboxes = document.querySelectorAll("#productItems input[type='checkbox']:checked");

                const selectedProducts = Array.from(checkboxes).map(cb => cb.value);

                if (!selectedSupplier || selectedProducts.length === 0) {
                    alert("אנא בחר ספק וסמן לפחות מוצר אחד להזמנה");
                    return;
                }

                const orderData = {
                    supplier: selectedSupplier,
                    products: selectedProducts
                };

                fetch('http://127.0.0.1:5000/save_order', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(orderData)
                })
                    .then(res => res.json())
                    .then(response => {
                        if (response.success) {
                            alert("ההזמנה נשלחה בהצלחה!");
                            productItemsContainer.innerHTML = "";
                            supplierSelect.value = "";
                            productListDiv.classList.add("hidden");
                            afterOrderOptionsDiv.classList.remove("hidden");
                        } else {
                            alert("שגיאה בשליחת ההזמנה");
                        }
                    })
                    .catch(err => {
                        console.error("שגיאה בשליחת ההזמנה", err);
                        alert("שגיאה בעת שליחת ההזמנה");
                    });
            });

            // כפתור הזמנה נוספת
            newOrderBtn.addEventListener("click", function () {
                productItemsContainer.innerHTML = "";
                supplierSelect.value = "";
                productListDiv.classList.add("hidden");
                afterOrderOptionsDiv.classList.add("hidden");
            });

            // כפתור חזרה לדף הבית
            goHomeBtn.addEventListener("click", function () {
                window.location.href = "../html/home.html";
            });
        })
        .catch(err => console.error('שגיאה בהבאת הספקים:', err));
});
