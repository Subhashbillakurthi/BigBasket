document.getElementById('login-btn').onclick = function () {
    document.getElementById('login-modal-overlay').style.display = 'flex';
  };
  document.getElementById('close-modal').onclick = function () {
    document.getElementById('login-modal-overlay').style.display = 'none';
  };
  document.getElementById('login-modal-overlay').onclick = function (e) {
    if (e.target === this) {
      this.style.display = "none";
    }
  };

document.getElementById('cart-btn').onclick = function () {
    document.getElementById('login-modal-overlay').style.display = 'flex';
  };
  document.getElementById('close-modal').onclick = function () {
    document.getElementById('login-modal-overlay').style.display = 'none';
  };
  document.getElementById('login-modal-overlay').onclick = function (e) {
    if (e.target === this) {
      this.style.display = "none";
    }
  };

  document.getElementById("login-btn").addEventListener("click", function() {
    window.location.href = "{% url 'login' %}";
  });

  document.getElementById("cart-btn").addEventListener("click", function() {
    window.location.href = "{% url 'login' %}";
  });