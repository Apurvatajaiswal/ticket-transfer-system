const API = "http://127.0.0.1:8000";

function getParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    source: params.get("source"),
    destination: params.get("destination")
  };
}

const API = "https://postchart-backend.onrender.com";
function loadResults() {
  let { source, destination } = getParams();

  fetch(`${API}/search-ticket?source=${source}&destination=${destination}`)
    .then(res => res.json())
    .then(data => {
      let container = document.getElementById("results");
      container.innerHTML = "";

      if (!data || data.length === 0) {
        container.innerHTML = "<p>No tickets found</p>";
        return;
      }

      data.forEach(ticket => {
        container.innerHTML += `
          <div class="ticket-card">
            <h3>${ticket.source} → ${ticket.destination}</h3>
            <p>Train: ${ticket.train_number}</p>
            <button onclick="payNow(500)">Pay</button>
          </div>
        `;
      });
    })
    .catch(() => {
      alert("Backend not running ❌");
    });
}
function payNow(amount) {

  fetch("http://127.0.0.1:8000/create-order", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ amount: amount })
  })
  .then(res => res.json())
  .then(order => {

    var options = {
      key: "YOUR_KEY_ID",
      amount: order.amount,
      currency: "INR",
      name: "PostChart",
      description: "Ticket Payment",
      order_id: order.id,

      handler: function (response) {
        alert("Payment Successful ✅");
      }
    };

    var rzp = new Razorpay(options);
    rzp.open();
  });
}

function goToList() {
  window.location.href = "list.html";
}
function goToResults() {
  let source = document.getElementById("source").value;
  let destination = document.getElementById("destination").value;

  window.location.href = `results.html?source=${source}&destination=${destination}`;
}

function payNow(amount) {

  fetch("http://127.0.0.1:8000/create-order", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ amount: amount })
  })
  .then(res => res.json())
  .then(order => {

    var options = {
      key: "YOUR_KEY_ID",   // 👈 same as backend
      amount: order.amount,
      currency: "INR",
      name: "PostChart",
      description: "Ticket Payment",
      order_id: order.id,

      handler: function (response) {
        alert("Payment Successful ✅");
        console.log(response);
      },

      theme: {
        color: "#6C4CF1"
      }
    };

    var rzp = new Razorpay(options);
    rzp.open();
  })
  .catch(() => {
    alert("Payment failed ❌");
  });
}