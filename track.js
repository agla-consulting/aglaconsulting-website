/* Agla Consulting: click tracking for Google Analytics 4.
   Sends events through the existing Google tag (gtag). No names, emails or other
   personal details are sent: only the link type, its text, where it sits and the page path. */
(function () {
  'use strict';
  var SERVICE_PAGES = ['ai-lead-capture', 'quote-automation', 'invoice-automation'];
  var ARTICLE_PAGES = ['slow-lead-follow-up-costs-jobs', 'how-often-to-follow-up-on-a-quote', 'how-to-measure-speed-to-lead'];

  function where(link) {
    if (link.closest('nav')) return 'nav';
    if (link.closest('footer')) return 'footer';
    if (link.closest('.article-cta')) return 'article_cta';
    if (link.closest('.svc-cta')) return 'page_cta';
    if (link.closest('.team-card')) return 'team';
    return 'body';
  }

  function slugOf(href) {
    var path = href.split('#')[0].split('?')[0];
    var last = path.split('/').pop() || '';
    return last.replace(/\.html$/, '');
  }

  function send(name, params) {
    if (typeof window.gtag !== 'function') return;
    params.page_path = window.location.pathname;
    params.transport_type = 'beacon';
    window.gtag('event', name, params);
  }

  document.addEventListener('click', function (event) {
    var link = event.target && event.target.closest ? event.target.closest('a[href]') : null;
    if (!link) return;
    var href = link.getAttribute('href') || '';
    var loc = where(link);
    var text = (link.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80);

    if (href.indexOf('tel:') === 0) return send('phone_click', { link_location: loc });
    if (href.indexOf('mailto:') === 0) return send('email_click', { link_location: loc });
    if (href.indexOf('linkedin.com') !== -1) return send('linkedin_click', { link_location: loc });

    // Calls to action that point at the consultation form
    if (/(^|\/)#contact$/.test(href) || href.slice(-8) === '#contact') {
      return send('cta_click', { cta_text: text, link_location: loc });
    }

    // Moves toward a service page or an article
    var slug = slugOf(href);
    if (SERVICE_PAGES.indexOf(slug) !== -1) {
      return send('service_page_click', { destination: slug, link_location: loc });
    }
    if (ARTICLE_PAGES.indexOf(slug) !== -1) {
      return send('article_click', { destination: slug, link_location: loc });
    }
  });
})();
