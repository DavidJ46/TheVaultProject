/* checkout.js 
    Developed by: Kaila
    Purpose: Pulls cart data to display a dynamic order summary.
*/

document.addEventListener('DOMContentLoaded', () => {
    // Target the HTML elements we need to update
    const itemsContainer = document.getElementById('checkoutItemsList');
    const totalDisplay = document.querySelector('.total-amount'); 
    
    // Grab the cart data saved from the Storefront/Listing screens
    // If no data exists, we default to an empty list []
    const cartData = JSON.parse(localStorage.getItem('vaultCart')) || [];

    // Logic to display items or a "Empty" message
    if (cartData.length === 0) {
        itemsContainer.innerHTML = '<p class="helper-text">Your bag is currently empty.</p>';
        if(totalDisplay) totalDisplay.innerText = "$0.00";
    } else {
        itemsContainer.innerHTML = ''; // Clear the "No items selected" placeholder
        let runningTotal = 0;

        // Loop through each item in the cart array
        cartData.forEach((item, index) => {
            const itemRow = document.createElement('div');
            itemRow.className = 'checkout-item-row';
            
            // Create the visual layout for the item name and price
            itemRow.innerHTML = `
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 5px;">
                    <span>${item.name}</span>
                    <span class="gold">$${parseFloat(item.price).toFixed(2)}</span>
                </div>
            `;
            
            itemsContainer.appendChild(itemRow);
            runningTotal += parseFloat(item.price);
        });

        // Update the final Total price
        if(totalDisplay) {
            totalDisplay.innerText = `$${runningTotal.toFixed(2)}`;
        }
    }
});

// Function to handle the "Complete Transaction" button
document.getElementById('checkoutForm')?.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevents page from reloading instantly
    
    alert("Transaction Secured! The seller has been notified of your meeting location.");
    
    // Clear the cart after purchase so they don't buy it twice
    localStorage.removeItem('vaultCart');
    
    // Redirect back to storefront or a thank you page
    window.location.href = "/storefront"; 
});