function switchDevice(type) {
  document.querySelectorAll('.device-frame').forEach(function(el) {
    el.style.display = 'none';
  });
  var target = document.getElementById('device-' + type);
  if (target) {
    target.style.display = 'block';
  }
  document.querySelectorAll('.device-switcher button').forEach(function(btn) {
    btn.classList.remove('active');
  });
  var activeBtn = document.querySelector('.device-switcher button[data-device="' + type + '"]');
  if (activeBtn) {
    activeBtn.classList.add('active');
  }
}

function navigateTo(url) {
  var iframe = document.querySelector('.device-screen iframe');
  if (iframe) {
    iframe.src = url;
  }
}

function goBack() {
  var iframe = document.querySelector('.device-screen iframe');
  if (iframe && iframe.contentWindow) {
    iframe.contentWindow.history.back();
  }
}
