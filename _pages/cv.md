---
layout: page
permalink: /cv/
title: CV
nav: true
nav_order: 5
description: Education, publications, talks, and activities -- generated from the same data as the downloadable PDF.
toc:
  sidebar: left
# common.js auto-tags every ".publications h2" with data-toc-skip so tocbot's sidebar doesn't
# pick up the bibliography's per-year group headers -- see the comment by the first h2.cv-h2
# below for why that means this page's OWN section headers have to live outside .publications,
# styled to match h2.bibliography via this page-scoped stylesheet instead.
_styles: |
  h2.cv-h2 {
    /* The original h2.bibliography uses --global-divider-color for both the border AND the
       text -- fine for a hairline border, but that token is a near-invisible dark grey
       (#424246) in dark mode, meant for subtle dividers, not readable text. Use the theme's
       actual text-color token for the text so it stays high-contrast in both modes. */
    color: var(--global-text-color);
    border-top: 1px solid var(--global-divider-color);
    padding-top: 1rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    text-align: right;
  }

  .cv-downloads {
    margin-bottom: 1.5rem;
  }

  .cv-download-btn {
    display: inline-block;
    padding: 0.75rem 1.75rem;
    margin-right: 1rem;
    margin-bottom: 0.75rem;
    border: 2px solid var(--global-text-color);
    border-radius: 8px;
    color: var(--global-text-color);
    font-size: 1.15rem;
    font-weight: 600;
    text-decoration: none;
  }

  .cv-download-btn:hover {
    color: var(--global-theme-color);
    border-color: var(--global-theme-color);
    text-decoration: none;
  }

  /* Year dividers inside Conferences/Scientific Activities (hand-written, carry class="cv-year"
     directly) and inside Publications (jekyll-scholar emits plain h2.bibliography with no class
     hook of its own, so that one is scoped through the wrapping #cv-publications-years id
     instead). Same look as h2.bibliography on /talks/, /theses/, /publications/, just smaller --
     this page already has its own larger h2.cv-h2 section headers doing the primary wayfinding. */
  h2.cv-year,
  #cv-publications-years h2.bibliography {
    font-size: 1.3rem;
  }
---

{% assign profile = site.data.cv_latex.profile %}

<p class="cv-downloads">
  <a href="{{ '/assets/pdf/CV.pdf' | relative_url }}" class="cv-download-btn" role="button" target="_blank">Download PDF</a>
  <a href="{{ '/assets/pdf/cv_latex.zip' | relative_url }}" class="cv-download-btn" role="button" target="_blank">Download LaTeX project</a>
</p>
{% if profile.label != blank %}<p>{{ profile.label }}</p>{% endif %}
{% if profile.summary != blank %}<p>{{ profile.summary }}</p>{% endif %}

<!--
  Each section header below is deliberately OUTSIDE any .publications div: common.js tags every
  ".publications h2" with data-toc-skip (correct for the bibliography's per-year group headers,
  which would otherwise flood the sidebar TOC with bare year numbers) -- but that rule can't tell
  those apart from a page's own section headers, so ours have to sit outside it to stay in the
  TOC, picking up matching styling from h2.cv-h2 in _styles above instead of h2.bibliography.
  Each section's actual list/entries stay inside their own .publications div for the badge/title/
  author/periodical row styling shared with /talks/, /theses/, and /publications/.
-->

<h2 class="cv-h2">Education</h2>
<div class="publications">
<ol class="bibliography">
{% assign theses_sorted = site.data.theses | sort: "date" | reverse %}
{% for t in theses_sorted %}
  <li>
    <div class="row">
      <div class="col col-sm-2 abbr">
        {% assign v = site.data.venues[t.degree] %}
        <abbr class="badge rounded w-100"{% if v.color %} style="background-color:{{ v.color }}"{% endif %}><div>{{ t.degree }}</div></abbr>
      </div>
      <div class="col-sm-10">
        <div class="title">{{ t.title }}</div>
        <div class="author">{{ t.school }}{% if t.supervisor %}. Supervisor: {{ t.supervisor }}{% endif %}</div>
        <div class="periodical"><em>{{ t.display_date }}{% if t.detail %}. {{ t.detail }}{% endif %}</em></div>
        {% if t.pdf %}
        <div class="links"><a href="{{ t.pdf | prepend: '/assets/pdf/' | relative_url }}" class="btn btn-sm z-depth-0" role="button" target="_blank">PDF</a></div>
        {% endif %}
      </div>
    </div>
  </li>
{% endfor %}
</ol>
</div>

<h2 class="cv-h2">Skills</h2>
<div class="publications">
{% for s in site.data.cv_extra.skills %}
<p><strong>{{ s.label }}:</strong> {{ s.details }}</p>
{% endfor %}
</div>

<h2 class="cv-h2">Publications</h2>
{% comment %}
  Site-wide group_by: year (_config.yml, shared with /publications/) renders each year as its
  own <h2 class="bibliography">YEAR</h2> in here -- same tag+class as this page's own section
  headers, but safely: these ones stay INSIDE .publications, so common.js's own
  ".publications h2 -> data-toc-skip" rule excludes them from the sidebar TOC automatically.
  The id below just scopes the smaller cv-year font size (see _styles) to this section.
{% endcomment %}
<div class="publications" id="cv-publications-years">
{% bibliography %}
</div>

<h2 class="cv-h2">Conferences</h2>
<div class="publications">
{% assign confs = site.data.talks | where_exp: "t", "t.type != 'Seminar'" | sort: "date" | reverse %}
{% assign current_year = nil %}
{% for k in confs %}
  {% assign year = k.date | date: "%Y" %}
  {% if year != current_year %}
    {% unless forloop.first %}</ol>{% endunless %}
    <h2 class="bibliography cv-year">{{ year }}</h2>
    <ol class="bibliography">
    {% assign current_year = year %}
  {% endif %}
  <li>
    <div class="row">
      <div class="col col-sm-2 abbr">
        {% assign v = site.data.venues[k.type] %}
        <abbr class="badge rounded w-100"{% if v.color %} style="background-color:{{ v.color }}"{% endif %}><div>{{ k.type }}</div></abbr>
        {% if k.invited %}{% assign iv = site.data.venues["Invited"] %}
        <abbr class="badge rounded w-100 mt-1"{% if iv.color %} style="background-color:{{ iv.color }}"{% endif %}><div>Invited</div></abbr>
        {% endif %}
      </div>
      <div class="col-sm-10">
        {% if k.title != blank %}<div class="title">{{ k.title }}</div>{% endif %}
        <div class="author">{{ k.event }}{% if k.location %}, {{ k.location }}{% endif %}</div>
        <div class="periodical"><em>{{ k.display_date }}{% if k.note %}. {{ k.note }}{% endif %}</em></div>
      </div>
    </div>
  </li>
{% endfor %}
</ol>
</div>

<h2 class="cv-h2">Scientific Activities</h2>
<div class="publications">
{% assign seminars = site.data.talks | where_exp: "t", "t.type == 'Seminar'" | sort: "date" | reverse %}
{% assign current_year = nil %}
{% for k in seminars %}
  {% assign year = k.date | date: "%Y" %}
  {% if year != current_year %}
    {% unless forloop.first %}</ol>{% endunless %}
    <h2 class="bibliography cv-year">{{ year }}</h2>
    <ol class="bibliography">
    {% assign current_year = year %}
  {% endif %}
  <li>
    <div class="row">
      <div class="col col-sm-2 abbr">
        {% assign v = site.data.venues[k.type] %}
        <abbr class="badge rounded w-100"{% if v.color %} style="background-color:{{ v.color }}"{% endif %}><div>{{ k.type }}</div></abbr>
        {% if k.invited %}{% assign iv = site.data.venues["Invited"] %}
        <abbr class="badge rounded w-100 mt-1"{% if iv.color %} style="background-color:{{ iv.color }}"{% endif %}><div>Invited</div></abbr>
        {% endif %}
      </div>
      <div class="col-sm-10">
        {% if k.title != blank %}<div class="title">{{ k.title }}</div>{% endif %}
        <div class="author">{{ k.event }}{% if k.location %}, {{ k.location }}{% endif %}</div>
        <div class="periodical"><em>{{ k.display_date }}{% if k.note %}. {{ k.note }}{% endif %}</em></div>
      </div>
    </div>
  </li>
{% endfor %}
</ol>
{% if site.data.cv_extra.scientific_activities_extra != empty %}
  <h2 class="bibliography cv-year">Ongoing</h2>
  <ol class="bibliography">
  {% for e in site.data.cv_extra.scientific_activities_extra %}
    <li>
      <div class="row">
        <div class="col col-sm-2 abbr">
          {% assign v = site.data.venues["Ongoing"] %}
          <abbr class="badge rounded w-100"{% if v.color %} style="background-color:{{ v.color }}"{% endif %}><div>Ongoing</div></abbr>
        </div>
        <div class="col-sm-10">
          <div class="title">{{ e.title }}</div>
          <div class="author">{{ e.description }}</div>
        </div>
      </div>
    </li>
  {% endfor %}
  </ol>
{% endif %}
</div>

<h2 class="cv-h2">Visiting Experiences</h2>
<div class="publications">
<ol class="bibliography">
{% for e in site.data.cv_extra.visiting %}
  <li>
    <div class="row">
      <div class="col col-sm-2 abbr">
        {% assign v = site.data.venues["Visit"] %}
        <abbr class="badge rounded w-100"{% if v.color %} style="background-color:{{ v.color }}"{% endif %}><div>Visit</div></abbr>
      </div>
      <div class="col-sm-10">
        <div class="title">{{ e.title }}</div>
        {% if e.description != blank %}<div class="author">{{ e.description }}</div>{% endif %}
        <div class="periodical"><em>{{ e.date_range }}</em></div>
      </div>
    </div>
  </li>
{% endfor %}
</ol>
</div>

<h2 class="cv-h2">Outreach Activities</h2>
<div class="publications">
{% if site.data.cv_extra.outreach.preamble != blank %}<p><em>{{ site.data.cv_extra.outreach.preamble }}</em></p>{% endif %}
<ol class="bibliography">
{% for e in site.data.cv_extra.outreach.entries %}
  <li>
    <div class="row">
      <div class="col col-sm-2 abbr">
        {% assign v = site.data.venues["Outreach"] %}
        <abbr class="badge rounded w-100"{% if v.color %} style="background-color:{{ v.color }}"{% endif %}><div>Outreach</div></abbr>
      </div>
      <div class="col-sm-10">
        <div class="title">{{ e.title }}</div>
        {% if e.description != blank %}<div class="author">{{ e.description }}</div>{% endif %}
        <div class="periodical"><em>{{ e.date_range }}</em></div>
      </div>
    </div>
  </li>
{% endfor %}
</ol>
</div>
