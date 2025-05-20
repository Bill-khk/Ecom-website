# Ecom-website
<p>Using https://docs.stripe.com/payments/checkout</p>
<h1>Simple E-commerce Checkout (Stripe Integration)</h1>
<p>This is a <strong>very simple web application</strong> built to demonstrate <strong>Stripe Checkout integration</strong> using the Stripe API.</p>
<p class="note">The focus is <strong>not on design or UI</strong>, but entirely on how to manage products, add them to a cart, and handle payments through Stripe’s secure payment flow.</p>

<h2>Product and Cart Interface</h2>

<img src="https://github.com/user-attachments/assets/97f44969-374a-472a-af2b-ee15dbeb6096" alt="Cart UI">
<p>Users can add items to their cart, remove them, and proceed to checkout.</p>

<h2>Stripe Checkout Page</h2>
<img src="https://github.com/user-attachments/assets/891351e1-79e0-42cc-aef1-cc5f376966a3" alt="Stripe Checkout" style="width:50%">
<p>The payment page is powered by <strong>Stripe Checkout</strong>, which securely handles all card inputs, validations, and transaction logic.</p>

<h2>Stripe Dashboard: Payment API Result</h2>
<img src="https://github.com/user-attachments/assets/796f2f8c-a21d-4230-8c02-72c9aa2a9545" alt="Stripe API Result" style="width:60%">
<p>Once a payment is completed, the result can be viewed in the <a href="https://dashboard.stripe.com/" target="_blank">Stripe Dashboard</a>. This includes all transaction metadata such as total amount, customer email, and status.</p>

<h2>Tech Stack</h2>
<ul>
    <li>Python (Flask)</li>
    <li>Stripe API</li>
    <li>Basic HTML/CSS</li>
</ul>
