#!/usr/bin/env python3
"""Generate the Agla Consulting service pages from one template.

Usage (from the repo root):
  python3 tools/build-service-pages.py            # writes the live pages (ai-lead-capture.html, ...)
  python3 tools/build-service-pages.py --preview  # writes *-preview.html drafts (git-ignored)

Edit page copy in PAGES below, then re-run. Each page's FAQ is written into both the visible
FAQ and the FAQPage structured data, so they always match (Google requires that).
"""
import html
import json
import sys

PREVIEW = "--preview" in sys.argv
SITE = "https://aglaconsulting.com"

ICONS = {
    "phone": "M3 5a2 2 0 012-2h3.28a1 1 0 01.95.68l1.5 4.5a1 1 0 01-.5 1.2l-2.26 1.13a11 11 0 005.52 5.52l1.13-2.26a1 1 0 011.2-.5l4.5 1.5a1 1 0 01.68.95V19a2 2 0 01-2 2h-1C9.72 21 3 14.28 3 6V5z",
    "chat": "M8 10h8M8 14h5M21 12a9 9 0 01-13.5 7.8L3 21l1.2-4.5A9 9 0 1121 12z",
    "mail": "M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z",
    "clipboard": "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4",
    "database": "M4 7v10c0 2 3.6 3 8 3s8-1 8-3V7M4 7c0 2 3.6 3 8 3s8-1 8-3M4 7c0-2 3.6-3 8-3s8 1 8 3M4 12c0 2 3.6 3 8 3s8-1 8-3",
    "calendar": "M8 7V3m8 4V3M4 11h16M5 5h14a1 1 0 011 1v14a1 1 0 01-1 1H5a1 1 0 01-1-1V6a1 1 0 011-1z",
    "calc": "M9 7h6M9 11h.01M12 11h.01M15 11h.01M9 15h.01M12 15h.01M15 15h.01M7 3h10a2 2 0 012 2v14a2 2 0 01-2 2H7a2 2 0 01-2-2V5a2 2 0 012-2z",
    "home": "M3 11l9-8 9 8M5 10v10h14V10M10 20v-6h4v6",
    "doc": "M9 12h6M9 16h6M7 3h7l5 5v11a2 2 0 01-2 2H7a2 2 0 01-2-2V5a2 2 0 012-2zM14 3v5h5",
    "repeat": "M4 4v6h6M20 20v-6h-6M5.6 15A8 8 0 0019 13M18.4 9A8 8 0 005 11",
    "pen": "M15.2 5.2l3.6 3.6M4 20l4.5-1 10.3-10.3a2.5 2.5 0 00-3.5-3.5L5 15.5 4 20z",
    "card": "M3 7a2 2 0 012-2h14a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V7zM3 10h18M7 15h4",
    "bell": "M15 17h5l-1.4-1.4A2 2 0 0118 14.2V11a6 6 0 10-12 0v3.2a2 2 0 01-.6 1.4L4 17h5m6 0a3 3 0 11-6 0",
    "layers": "M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5",
    "sync": "M4 12a8 8 0 0114-5.3L20 9M20 4v5h-5M20 12a8 8 0 01-14 5.3L4 15M4 20v-5h5",
    "chart": "M4 20V10M10 20V4M16 20v-7M22 20H2",
}

GOOD_FIT = ("Home services and trades, professional services, medical and dental offices, real estate, "
            "and other local businesses that depend on inbound calls and quote requests.")

PAGES = [
    {
        "slug": "ai-lead-capture",
        "nav_name": "AI Lead Capture",
        "stage": "Stages 1&ndash;2 &middot; Capture &amp; Qualify",
        "title": "AI Call Answering & Lead Capture for Small Businesses | Agla Consulting",
        "og_title": "AI Call Answering & Lead Capture | Agla Consulting",
        "description": "Answer every call, text and web inquiry in seconds, day or night. Agla sets up AI lead capture that qualifies leads your way and logs them in your CRM. St. Louis and nationwide.",
        "og_description": "Every call, text and web inquiry answered in seconds, qualified your way and logged in your CRM.",
        "service_name": "AI Call Answering & Lead Capture",
        "service_type": "AI lead capture and call answering automation",
        "service_desc": "AI agents that answer calls, texts and web inquiries 24/7, ask qualifying questions, log every lead in the CRM, and book appointments or alert the team.",
        "eyebrow": "Lead-to-Cash stages 1&ndash;2: Capture &amp; Qualify",
        "h1": "AI call answering &amp; lead capture <span>for small businesses</span>",
        "lead": "Every call, text and web inquiry answered in seconds, day or night. Your AI agent asks the questions your team would ask, logs every lead in your CRM, and books the appointment or alerts the right person.",
        "pain_title": "Leads don't wait",
        "pain_sub": "Most customers hire whoever responds first. These are the moments growing businesses lose them.",
        "pain": [
            ("Calls during a job", "The phone rings while your team is on site, and the caller hangs up and dials the next company."),
            ("After hours and weekends", "Inquiries that arrive at night or on Saturday wait until someone is back in the office."),
            ("Buried in the inbox", "Form emails, social media leads and texts pile up in shared inboxes, and some never get answered."),
            ("No record of where leads came from", "Details get scribbled on paper and typed in later, so you can't see which marketing works."),
        ],
        "cards_title": "What your AI agent handles",
        "cards_sub": "Set up around your services, your questions and your rules, not a generic script.",
        "cards": [
            ("phone", "Answers every call", "A natural-sounding voice agent greets callers by your business name, answers common questions, collects the details and transfers to a person when needed."),
            ("chat", "Texts back missed calls", "If a call can't be answered, the caller gets an instant text so the conversation keeps going instead of going to a competitor."),
            ("mail", "Responds to web and social leads", "Website forms, social media lead ads and email inquiries are read, sorted and answered in seconds, in a consistent format."),
            ("clipboard", "Qualifies with your questions", "Service needed, address, timeline and anything else you ask today. Hot leads are flagged, and poor fits are handled politely."),
            ("database", "Logs everything in your CRM", "Contact details, lead source, a call summary and the answers to your questions, checked against existing customers to avoid duplicates."),
            ("calendar", "Books or routes the next step", "Books the appointment on your calendar, or alerts the right person by text or email with everything they need to follow up."),
        ],
        "flow_sub": "From first contact to a qualified lead in your CRM, without anyone stopping what they're doing.",
        "flow": [
            ("An inquiry arrives", "A call, text, website form, social lead or email."),
            ("AI responds in seconds", "By voice or text, 24 hours a day, in your business's voice."),
            ("It qualifies the lead", "Asks your questions and captures the details you need to quote."),
            ("The lead is logged", "Added to your CRM with its source, summary and no duplicates."),
            ("The next step happens", "An appointment is booked, a quote is started, or your team is alerted."),
        ],
        "control": [
            ("Your script, your rules.", "You approve what the agent says, which questions it asks and what it should never promise."),
            ("A person whenever it's needed.", "Callers can ask for a human, and urgent or unusual requests go straight to your team."),
            ("Business-hours settings.", "Decide what happens during the day, after hours, on weekends and on holidays."),
            ("Everything is reviewable.", "Call summaries and transcripts let you check quality and coach the agent over time."),
            ("Your accounts, your data.", "Built on accounts in your name and documented, so you're never locked in."),
        ],
        "tools": ["Your CRM", "Business phone &amp; cloud PBX", "Website forms", "Social media lead ads", "Shared email inbox", "Calendar &amp; scheduling", "Business text messaging"],
        "start_sub": "Most clients start with one lead source, such as after-hours calls or the website quote form, and run it side by side with their team before going live.",
        "faq": [
            ("Will callers know they're talking to AI?", "We recommend being upfront. The agent introduces itself as your virtual assistant, and callers can ask for a person at any time. Where required, calls include a recording notice."),
            ("What happens when the AI can't answer a question?", "It does what a good receptionist would: takes a detailed message, transfers the call to a person during business hours, or alerts your team right away by text or email, based on rules you set."),
            ("Do I need a new phone system or CRM?", "Usually not. We connect to the phone system, CRM, website forms and calendar you already use. If something is missing, we recommend an option that fits your size and budget."),
            ("What does it cost?", "After the free consultation, you get a fixed price for the pilot. Ongoing phone and AI usage is billed by those providers to accounts in your name, and we estimate it for you up front, so there are no surprises."),
            ("How quickly can it be running?", "A pilot on one lead source, such as after-hours calls or your website form, typically runs within a few weeks. It runs side by side with your team before it goes live with customers."),
        ],
        "cta_title": "Stop losing leads to voicemail",
        "cta_text": "In a free, no-obligation consultation, we'll look at where your calls and inquiries slip through the cracks and show you what to automate first.",
    },
    {
        "slug": "quote-automation",
        "nav_name": "Quote &amp; Proposal Automation",
        "stage": "Stages 3&ndash;4 &middot; Quote &amp; Close",
        "title": "Quote & Proposal Automation for Small Businesses | Agla Consulting",
        "og_title": "Quote & Proposal Automation | Agla Consulting",
        "description": "Send professional quotes in minutes, built from your own pricing rules, with automatic follow-up, e-signatures and deposits. Agla automates quote-to-close for small businesses.",
        "og_description": "Professional quotes in minutes from your own pricing rules, with follow-ups, e-signatures and deposits that run on their own.",
        "service_name": "Quote & Proposal Automation",
        "service_type": "Quote-to-cash and proposal automation",
        "service_desc": "Automated quotes and proposals generated from the client's own pricing rules, with owner review, automatic follow-up, e-signature, deposit requests and scheduling of accepted work.",
        "eyebrow": "Lead-to-Cash stages 3&ndash;4: Quote &amp; Close",
        "h1": "Quote &amp; proposal automation <span>for small businesses</span>",
        "lead": "Turn qualified leads into professional quotes in minutes, built from your own pricing rules. Follow-ups, e-signatures and deposits run on their own, and accepted work lands on your schedule.",
        "pain_title": "Where deals stall",
        "pain_sub": "The quote is often where a ready-to-buy customer cools off. These are the usual reasons.",
        "pain": [
            ("Quotes take days", "Someone has to look up the job, run the numbers and write it up between everything else."),
            ("Pricing depends on who wrote it", "Two people quote the same job differently, and minimums or add-ons get missed."),
            ("Nobody follows up", "Quotes go out and sit. Without a reminder, customers move on or forget."),
            ("Approved work waits", "A customer says yes, then the job stalls on a signature, a deposit or getting it scheduled."),
        ],
        "cards_title": "What gets automated",
        "cards_sub": "Built on the way you price and sell today, from your price sheets, minimums and packages.",
        "cards": [
            ("calc", "Quotes from your pricing rules", "Per-square-foot, per-item, packages, minimums and add-ons applied the same way every time, so every quote is consistent."),
            ("home", "Job details pulled in automatically", "Details collected at intake, plus property information and photos where available, are added to the quote without retyping."),
            ("doc", "Professional, branded proposals", "Clean proposals with your logo and terms, including good, better and best options when you offer them."),
            ("repeat", "Automatic follow-up", "Friendly reminders go out on a schedule you choose and stop the moment the customer replies or accepts."),
            ("pen", "E-signature and deposits", "Customers approve online and pay a deposit in the same step, with no printing, scanning or phone tag."),
            ("calendar", "Accepted work gets scheduled", "An accepted quote becomes a job in your CRM and on your calendar, ready for your team."),
        ],
        "flow_sub": "From a qualified lead to signed, scheduled work, with you in control of what gets sent.",
        "flow": [
            ("A qualified lead arrives", "With the details collected at intake, from any channel."),
            ("A quote is drafted", "Built from your pricing rules, with options and add-ons."),
            ("You review it", "Approve with one click, adjust it, or let routine quotes go automatically."),
            ("It's sent with follow-ups", "Reminders run until the customer says yes or no."),
            ("Accepted work is booked", "Signed, deposit collected and added to your schedule."),
        ],
        "control": [
            ("You set the pricing rules.", "Your rates, minimums, discounts and limits. The system never invents a price."),
            ("Review before anything is sent.", "Approve every quote at first, then move to reviewing only the exceptions when you're ready."),
            ("Judgment calls go to a person.", "Jobs that need a site visit or a closer look are flagged for your team instead of guessed."),
            ("Every quote is logged.", "Each version, follow-up and approval is recorded in your CRM, so nothing falls through the cracks."),
            ("Your accounts, your data.", "Built on accounts in your name and documented, so you're never locked in."),
        ],
        "tools": ["Your CRM", "Estimating or quoting tool", "Price sheets &amp; spreadsheets", "E-signature", "Payment processor", "Calendar &amp; scheduling", "Email &amp; text messaging"],
        "start_sub": "Most clients start with one service line, using their existing price sheet, and compare automated quotes with the ones their team writes before going live.",
        "faq": [
            ("Can it handle my pricing if it's complicated?", "If your team can price a job from a price sheet and a few details, it can usually be automated. Jobs that need a site visit or a judgment call are flagged for a person instead of guessed."),
            ("Will quotes go out without my approval?", "Not unless you want them to. Most clients start by approving every quote, which takes about a minute, and move to approving only exceptions once they trust the results."),
            ("Do I need new quoting software?", "Usually not. We work with the CRM or estimating tool you use today. If you quote from spreadsheets or paper, we recommend an option that fits your size and budget."),
            ("What does it cost?", "After the free consultation, you get a fixed price for the pilot. Any ongoing software or AI usage is billed by those providers to accounts in your name, and we estimate it for you up front, so there are no surprises."),
            ("How quickly can it be running?", "A pilot on one service line typically runs within a few weeks. It runs side by side with your team, so you can compare automated quotes with yours before it goes live with customers."),
        ],
        "cta_title": "Get quotes out while customers are still interested",
        "cta_text": "In a free, no-obligation consultation, we'll look at how you quote today and show you what could be automated first.",
    },
    {
        "slug": "invoice-automation",
        "nav_name": "Invoicing &amp; Payment Collection",
        "stage": "Stage 5 &middot; Collect",
        "title": "Invoicing & Payment Collection Automation for Small Businesses | Agla Consulting",
        "og_title": "Invoicing & Payment Collection Automation | Agla Consulting",
        "description": "Get paid faster with less chasing. Agla automates invoices, payment links, reminders and accounting sync for small and midsize businesses in St. Louis and nationwide.",
        "og_description": "Invoices, payment links and reminders that run on their own, with payments synced to your accounting.",
        "service_name": "Invoicing & Payment Collection Automation",
        "service_type": "Invoicing, billing and collections automation",
        "service_desc": "Automated invoicing triggered by completed work, payment links by text and email, scheduled reminders, deposits and progress billing, and payment sync to the client's accounting software.",
        "eyebrow": "Lead-to-Cash stage 5: Collect",
        "h1": "Invoicing &amp; payment collection <span>for small businesses</span>",
        "lead": "Get paid faster, with less chasing. Completed work triggers the invoice and a payment link, reminders run on their own, and payments sync to your accounting.",
        "pain_title": "Where cash gets stuck",
        "pain_sub": "The work is done, but the money isn't in the bank yet. These are the usual delays.",
        "pain": [
            ("Invoices go out late", "Billing waits until someone has time at the end of the day or the end of the week."),
            ("Chasing payments", "Someone spends hours calling and emailing customers about open balances."),
            ("Double entry", "Payments get typed into the CRM and the accounting software by hand, and mistakes creep in."),
            ("No clear picture", "It's hard to see who owes what, and how long it's been outstanding."),
        ],
        "cards_title": "What gets automated",
        "cards_sub": "Set up around your billing terms, your payment options and the accounting software you already use.",
        "cards": [
            ("doc", "Invoices when the job is done", "Marking a job complete creates the invoice from the job details, with no retyping."),
            ("card", "Pay-by-link", "Customers get a secure payment link by text and email and can pay by card or bank transfer through your processor."),
            ("bell", "Automatic reminders", "Polite reminders before and after the due date, written in your voice, that stop as soon as payment arrives."),
            ("layers", "Deposits and progress billing", "Deposits, milestone payments and recurring service plans billed on schedule."),
            ("sync", "Accounting sync", "Payments are matched to invoices and recorded in your accounting software automatically."),
            ("chart", "Receivables at a glance", "A simple weekly summary of open invoices and how long they've been outstanding."),
        ],
        "flow_sub": "From finished work to money in the bank, without anyone chasing it.",
        "flow": [
            ("The job is marked complete", "In your CRM or field app, by your team."),
            ("The invoice is created", "From the job details, with your terms and branding."),
            ("It's sent with a payment link", "By email and text, so customers can pay in seconds."),
            ("Reminders run until it's paid", "On the schedule you choose, then they stop."),
            ("The payment is recorded", "Matched and synced to your accounting software."),
        ],
        "control": [
            ("Your terms, your tone.", "You choose due dates, how many reminders go out and exactly what they say."),
            ("Exceptions go to a person.", "Disputes, payment plans and special cases are routed to your team instead of automated."),
            ("Review if you want to.", "Approve invoices before they're sent, or let routine ones go automatically."),
            ("Payment details stay with your processor.", "Customers pay through your processor's secure checkout. Card and bank details never pass through us."),
            ("Your accounts, your data.", "Built on accounts in your name and documented, so you're never locked in."),
        ],
        "tools": ["Your CRM or field-service app", "Accounting software", "Payment processor", "Email &amp; text messaging", "Calendar &amp; scheduling"],
        "start_sub": "Most clients start with invoicing and reminders for one service line, then add deposits, progress billing and accounting sync.",
        "faq": [
            ("Will automatic reminders annoy my customers?", "Reminders are friendly, spaced out and written in your voice. You choose how many go out, and they stop the moment a payment comes in."),
            ("Do you handle or store customer payment details?", "No. Customers pay through your own payment processor's secure checkout. We connect the workflow, and card and bank details never pass through us."),
            ("Do I need new accounting or payment software?", "Usually not. We connect to the accounting software and payment processor you already use. If something is missing, we recommend an option that fits your size and budget."),
            ("What does it cost?", "After the free consultation, you get a fixed price for the pilot. Any ongoing software or processing fees are billed by those providers to accounts in your name, and we estimate them for you up front, so there are no surprises."),
            ("How quickly can it be running?", "A pilot on one service line typically runs within a few weeks. It runs side by side with your current process before it goes live with customers."),
        ],
        "cta_title": "Get paid faster, without the chasing",
        "cta_text": "In a free, no-obligation consultation, we'll look at how you bill and collect today and show you what could be automated first.",
    },
]

RIBBON = ('  <div style="position:fixed;bottom:16px;left:16px;z-index:999;background:#f59e0b;color:#111827;'
          'font:700 13px/1 system-ui;padding:10px 14px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.3)">'
          'DRAFT PREVIEW: not live</div>\n')


def page_file(slug):
    return f"{slug}-preview.html" if PREVIEW else f"{slug}.html"


def icon(name):
    return (f'<svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="{ICONS[name]}"/></svg>')


def text(s):
    """Plain text for JSON-LD and meta (unescape entities, strip span tags)."""
    return html.unescape(s.replace("<span>", "").replace("</span>", ""))


def render(p):
    url = f"{SITE}/{p['slug']}.html"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": f"{url}#service",
                "name": p["service_name"],
                "serviceType": p["service_type"],
                "description": p["service_desc"],
                "url": url,
                "provider": {"@id": f"{SITE}/#business"},
                "areaServed": [
                    {"@type": "AdministrativeArea", "name": "St. Louis, MO"},
                    {"@type": "Country", "name": "United States"},
                ],
                "audience": {"@type": "BusinessAudience", "audienceType": "Small and midsize businesses"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": p["service_name"], "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in p["faq"]
                ],
            },
        ],
    }
    ld_json = json.dumps(ld, indent=2, ensure_ascii=False).replace("</", "<\\/")
    pain = "\n".join(f"          <div><h3>{t}</h3><p>{d}</p></div>" for t, d in p["pain"])
    cards = "\n".join(
        f'          <article class="card">\n            <div class="ico" aria-hidden="true">{icon(i)}</div>\n'
        f"            <h3>{t}</h3>\n            <p>{d}</p>\n          </article>"
        for i, t, d in p["cards"]
    )
    flow = "\n".join(
        f'          <li><p class="n">Step {n}</p><h3>{t}</h3><p>{d}</p></li>'
        for n, (t, d) in enumerate(p["flow"], 1)
    )
    control = "\n".join(f"            <li><strong>{t}</strong> {d}</li>" for t, d in p["control"])
    tools = "".join(f"<li>{t}</li>" for t in p["tools"])
    faq = "\n".join(
        f"          <details>\n            <summary>{html.escape(q, quote=False)}</summary>\n"
        f"            <p>{html.escape(a, quote=False)}</p>\n          </details>"
        for q, a in p["faq"]
    )
    related = []
    for o in PAGES:
        if o["slug"] == p["slug"]:
            related.append(f'          <a class="cur" aria-current="page" href="{page_file(o["slug"])}"><p class="rs">{o["stage"]}</p>'
                           f'<strong>{o["nav_name"]}</strong>You are here</a>')
        else:
            related.append(f'          <a href="{page_file(o["slug"])}"><p class="rs">{o["stage"]}</p>'
                           f'<strong>{o["nav_name"]}</strong>Learn more &rarr;</a>')
    related = "\n".join(related)
    svc_footer = " &middot; ".join(f'<a href="{page_file(o["slug"])}">{o["nav_name"]}</a>' for o in PAGES)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) → Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-FC32SBT1V7"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-FC32SBT1V7');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Generated by tools/build-service-pages.py: edit the copy there, not here. -->
  <title>{html.escape(p['title'])}</title>
  <meta name="description" content="{html.escape(p['description'])}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="favicon.ico?v=2" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png?v=2">
  <link rel="apple-touch-icon" href="apple-touch-icon.png?v=2">
  <meta name="theme-color" content="#0f172a">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{html.escape(p['og_title'])}">
  <meta property="og:description" content="{html.escape(p['og_description'])}">
  <meta property="og:image" content="{SITE}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="legal.css">
  <link rel="stylesheet" href="service.css">
  <script type="application/ld+json">
{ld_json}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <nav aria-label="Main Navigation">
    <div class="nav-container">
      <a href="/" class="brand" aria-label="Agla Consulting home">
        <picture><source srcset="agla-footprint-logo-nav.webp" type="image/webp"><img src="agla-footprint-logo-nav.png" alt="Agla Consulting, LLC" width="155" height="52"></picture>
      </a>
      <a href="/#contact" class="btn-nav">Book a Free Consultation</a>
    </div>
  </nav>

  <main id="main" class="svc">
    <section class="svc-hero">
      <div class="wrap">
        <p class="crumb"><a href="/">Home</a> / {p['service_name'].replace('&', '&amp;')}</p>
        <p class="eyebrow">{p['eyebrow']}</p>
        <h1>{p['h1']}</h1>
        <p class="lead">{p['lead']}</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="/#contact">Book a Free Consultation</a>
          <a class="btn btn-ghost" href="#how">See how it works</a>
        </div>
      </div>
    </section>

    <section class="band" aria-labelledby="pain-title">
      <div class="wrap">
        <h2 id="pain-title">{p['pain_title']}</h2>
        <p class="sub">{p['pain_sub']}</p>
        <div class="pain">
{pain}
        </div>
      </div>
    </section>

    <section class="band gray" aria-labelledby="what-title">
      <div class="wrap">
        <h2 id="what-title">{p['cards_title']}</h2>
        <p class="sub">{p['cards_sub']}</p>
        <div class="cards">
{cards}
        </div>
      </div>
    </section>

    <section class="band" id="how" aria-labelledby="how-title">
      <div class="wrap">
        <h2 id="how-title">How it works</h2>
        <p class="sub">{p['flow_sub']}</p>
        <ol class="flow">
{flow}
        </ol>
      </div>
    </section>

    <section class="band gray" aria-labelledby="control-title">
      <div class="wrap two">
        <div>
          <h2 id="control-title">You stay in control</h2>
          <ul class="checks">
{control}
          </ul>
        </div>
        <div>
          <h2>Works with what you already use</h2>
          <ul class="tools" aria-label="Tools it connects to">
            {tools}
          </ul>
          <h3 style="color:#0f172a;margin-bottom:8px;">A good fit for</h3>
          <p class="who">{GOOD_FIT}</p>
        </div>
      </div>
    </section>

    <section class="band" aria-labelledby="start-title">
      <div class="wrap">
        <h2 id="start-title">Getting started</h2>
        <p class="sub">{p['start_sub']} <a href="/#process">See how engagements work</a>.</p>
        <div class="faq">
{faq}
        </div>
      </div>
    </section>

    <section class="band gray" aria-labelledby="related-title">
      <div class="wrap">
        <h2 id="related-title">Automate the whole Lead-to-Cash lifecycle</h2>
        <p class="sub">Each service works on its own, and they're designed to hand off to each other. <a href="/#l2c">See the full lifecycle</a>.</p>
        <div class="related">
{related}
        </div>
      </div>
    </section>

    <section class="svc-cta" aria-labelledby="cta-title">
      <div class="wrap">
        <h2 id="cta-title">{p['cta_title']}</h2>
        <p>{p['cta_text']}</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="/#contact">Book a Free Consultation</a>
        </div>
        <p style="margin-top:20px;">Or call <a class="text-link" href="tel:+16363294961">(636) 329-4961</a></p>
      </div>
    </section>
  </main>

  <footer>
    <p><a href="/">Home</a> &middot; <a href="/#l2c">Lead-to-Cash</a> &middot; <a href="/#process">How It Works</a> &middot; <a href="/#contact">Contact</a></p>
    <p>{svc_footer}</p>
    <p><a href="privacy.html">Privacy Policy</a> &middot; <a href="terms.html">Terms of Use</a> &middot; <a href="accessibility.html">Accessibility</a></p>
    <p>&copy; 2026 Agla Consulting LLC &middot; St. Louis-based &middot; Remote nationwide</p>
  </footer>

  <script>
    // Analytics: record clicks on phone, email and LinkedIn links (no personal data).
    document.addEventListener('click', function (event) {{
      var link = event.target.closest ? event.target.closest('a[href]') : null;
      if (!link) return;
      var href = link.getAttribute('href'), name = null;
      if (href.indexOf('tel:') === 0) name = 'phone_click';
      else if (href.indexOf('mailto:') === 0) name = 'email_click';
      else if (href.indexOf('linkedin.com') !== -1) name = 'linkedin_click';
      if (name) gtag('event', name, {{ link_location: 'service_page' }});
    }});
  </script>
{RIBBON if PREVIEW else ''}</body>
</html>
"""


if __name__ == "__main__":
    for p in PAGES:
        out = page_file(p["slug"])
        with open(out, "w") as f:
            f.write(render(p))
        print("wrote", out)
