/* ===== Yandex.Metrika ===== */
(function(m,e,t,r,i,k,a){
  m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
  m[i].l=1*new Date();
  for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
  k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
})(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=109875276', 'ym');
ym(109875276, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});

/* ===== PARTICLES BACKGROUND ===== */
(function initParticles() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];
  let mouseX = 0, mouseY = 0;
  const MAX_PARTICLES = 60;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  class Particle {
    constructor() {
      this.reset();
    }
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 2 + 0.5;
      this.speedX = (Math.random() - 0.5) * 0.3;
      this.speedY = (Math.random() - 0.5) * 0.3;
      this.opacity = Math.random() * 0.5 + 0.1;
      this.baseOpacity = this.opacity;
    }
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      const dx = mouseX - this.x;
      const dy = mouseY - this.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 200) {
        const force = (200 - dist) / 200;
        this.opacity = this.baseOpacity + force * 0.3;
      } else {
        this.opacity = this.baseOpacity;
      }
      if (this.x < -10 || this.x > canvas.width + 10 || this.y < -10 || this.y > canvas.height + 10) {
        this.reset();
      }
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(201, 169, 89, ${this.opacity})`;
      ctx.fill();
    }
  }

  for (let i = 0; i < MAX_PARTICLES; i++) particles.push(new Particle());

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  function connectParticles() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 150) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(201, 169, 89, ${0.06 * (1 - dist / 150)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    connectParticles();
    requestAnimationFrame(animate);
  }
  animate();
})();

/* ===== NAVIGATION ===== */
(function initNav() {
  const nav = document.getElementById('nav');
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');

  // Scroll effect
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  });

  // Mobile toggle
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('open');
    });
    // Close menu on link click
    links.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => links.classList.remove('open'));
    });
  }
})();

/* ===== PROGRESS BAR ===== */
(function initProgress() {
  const bar = document.getElementById('progress-bar');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    const p = (window.scrollY / h) * 100;
    bar.style.width = p + '%';
  });
})();

/* ===== SCROLL ANIMATIONS ===== */
(function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.fade-in, .section, .stat-card, .fact-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
})();

/* ===== COUNTER ANIMATION ===== */
(function initCounters() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.querySelectorAll('.number').forEach(num => {
          const target = parseInt(num.dataset.target);
          if (!target) return;
          let current = 0;
          const duration = 2000;
          const start = performance.now();
          function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            current = Math.floor(ease * target);
            num.textContent = current;
            if (progress < 1) requestAnimationFrame(update);
            else { num.textContent = target; num.classList.add('done'); }
          }
          requestAnimationFrame(update);
        });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('.stats-grid').forEach(el => observer.observe(el));
})();

/* ===== TILT CARDS ===== */
(function initTilt() {
  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      const rx = (y - cy) / cy * 8;
      const ry = (cx - x) / cx * 8;
      card.querySelector('.tilt-card-inner').style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.querySelector('.tilt-card-inner').style.transform = 'rotateX(0) rotateY(0)';
    });
  });
})();

/* ===== MEDIA TABS ===== */
(function initMediaTabs() {
  document.querySelectorAll('.media-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const parent = tab.closest('.section');
      parent.querySelectorAll('.media-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      parent.querySelectorAll('.media-content').forEach(c => c.classList.remove('active'));
      const target = document.getElementById(tab.dataset.tab);
      if (target) target.classList.add('active');
    });
  });
})();

/* ===== LIGHTBOX ===== */
(function initLightbox() {
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lightboxImg');
  if (!lb || !img) return;

  document.querySelectorAll('.photo-item').forEach(item => {
    item.addEventListener('click', () => {
      const bg = item.style.backgroundImage;
      if (bg) {
        img.src = bg.replace(/url\(["']?/, '').replace(/["']?\)/, '');
        lb.classList.add('active');
      }
    });
  });

  lb.addEventListener('click', (e) => {
    if (e.target === lb || e.target.classList.contains('close-lb')) {
      lb.classList.remove('active');
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') lb.classList.remove('active');
  });
})();

/* ===== CAREER CAROUSEL ===== */
(function initCarousel() {
  const track = document.querySelector('.career-track');
  if (!track) return;
  const slides = track.querySelectorAll('.career-slide');
  const prev = document.getElementById('carouselPrev');
  const next = document.getElementById('carouselNext');
  const dotsContainer = document.querySelector('.carousel-dots');
  let current = 0;
  let isDragging = false;
  let startX = 0, scrollLeft = 0;

  function update() {
    const slideWidth = slides[0]?.offsetWidth + 20 || 340;
    track.style.transform = `translateX(-${current * slideWidth}px)`;
    if (dotsContainer) {
      dotsContainer.querySelectorAll('.dot').forEach((d, i) => {
        d.classList.toggle('active', i === current);
      });
    }
  }

  if (prev && next) {
    prev.addEventListener('click', () => { if (current > 0) { current--; update(); } });
    next.addEventListener('click', () => { if (current < slides.length - 1) { current++; update(); } });
  }

  if (dotsContainer) {
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'dot' + (i === 0 ? ' active' : '');
      dot.addEventListener('click', () => { current = i; update(); });
      dotsContainer.appendChild(dot);
    });
  }

  // Drag support
  track.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.pageX - track.offsetLeft;
    scrollLeft = parseInt(track.style.transform.replace(/[^\d-]/g, '')) || 0;
    track.classList.add('dragging');
  });
  track.addEventListener('mouseleave', () => {
    isDragging = false;
    track.classList.remove('dragging');
  });
  track.addEventListener('mouseup', () => {
    isDragging = false;
    track.classList.remove('dragging');
  });
  track.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - track.offsetLeft;
    const walk = (x - startX) * 2;
    const maxScroll = slides.length * (slides[0]?.offsetWidth + 20) - track.parentElement.offsetWidth;
    const newScroll = Math.max(0, Math.min(maxScroll, scrollLeft - walk));
    current = Math.round(newScroll / (slides[0]?.offsetWidth + 20 || 340));
    update();
  });
})();

/* ===== MUSIC / AUDIO PLAYER ===== */
(function initAudioPlayer() {
  let currentAudio = null;
  const toggleBtn = document.getElementById('music-toggle');
  const toggleIcon = document.getElementById('musicToggleIcon');
  const trackInfo = document.getElementById('musicTrackInfo');
  const trackName = document.getElementById('musicTrackName');

  window.playTrack = function(url, name) {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio = null;
    }
    currentAudio = new Audio(url);
    currentAudio.play();
    if (trackName) trackName.textContent = name;
    if (trackInfo) trackInfo.classList.add('show');
    if (toggleIcon) toggleIcon.className = 'fas fa-pause';
    if (toggleBtn) toggleBtn.classList.add('playing');

    currentAudio.addEventListener('ended', () => {
      if (toggleIcon) toggleIcon.className = 'fas fa-play';
      if (toggleBtn) toggleBtn.classList.remove('playing');
      if (trackInfo) trackInfo.classList.remove('show');
      currentAudio = null;
    });
  };

  window.togglePlay = function() {
    if (currentAudio) {
      if (currentAudio.paused) {
        currentAudio.play();
        if (toggleIcon) toggleIcon.className = 'fas fa-pause';
        if (toggleBtn) toggleBtn.classList.add('playing');
      } else {
        currentAudio.pause();
        if (toggleIcon) toggleIcon.className = 'fas fa-play';
        if (toggleBtn) toggleBtn.classList.remove('playing');
      }
    } else {
      // Play default track
      playTrack('audio/Lose Control.mp3', 'Lose Control');
    }
  };

  // Track items click
  document.querySelectorAll('.track-item .play-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const item = btn.closest('.track-item');
      const url = btn.dataset.src || item.dataset.src;
      const name = item.querySelector('.name')?.textContent || 'Unknown';
      if (url) playTrack(url, name);
    });
  });

  // Cover cards audio
  document.querySelectorAll('.cover-card audio').forEach(audio => {
    audio.addEventListener('play', () => {
      const name = audio.closest('.cover-card')?.querySelector('.name')?.textContent || 'Cover';
      if (trackName) trackName.textContent = name;
      if (trackInfo) trackInfo.classList.add('show');
      if (toggleIcon) toggleIcon.className = 'fas fa-pause';
      if (toggleBtn) toggleBtn.classList.add('playing');
    });
    audio.addEventListener('pause', () => {
      if (toggleIcon) toggleIcon.className = 'fas fa-play';
      if (toggleBtn) toggleBtn.classList.remove('playing');
    });
  });
})();

/* ===== TOAST ===== */
window.showToast = function(msg, duration = 3000) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), duration);
};

/* ===== CONTACT FORM ===== */
(function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const status = form.querySelector('.form-status');
    const data = new FormData(form);
    try {
      const res = await fetch(form.action, { method: 'POST', body: data });
      if (res.ok) {
        if (status) { status.textContent = '✅ Сообщение отправлено! Спасибо!'; status.className = 'form-status success'; }
        form.reset();
      } else {
        if (status) { status.textContent = '❌ Ошибка. Попробуйте позже или напишите в Telegram.'; status.className = 'form-status error'; }
      }
    } catch {
      if (status) { status.textContent = '❌ Ошибка. Попробуйте позже или напишите в Telegram.'; status.className = 'form-status error'; }
    }
  });
})();
