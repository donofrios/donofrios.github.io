---
layout: page
permalink: /theses/
title: theses
description: bachelor, master, and doctoral theses in reverse chronological order.
nav: true
nav_order: 5
---

<div class="publications">
{% assign theses = site.data.theses | sort: "date" | reverse %}
{% assign current_year = nil %}
{% for t in theses %}
  {% assign year = t.date | date: "%Y" %}
  {% if year != current_year %}
    {% unless forloop.first %}</ol>{% endunless %}
    <h2 class="bibliography">{{ year }}</h2>
    <ol class="bibliography">
    {% assign current_year = year %}
  {% endif %}
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
        <div class="links">{% if t.pdf contains '://' %}{% assign pdf_url = t.pdf %}{% else %}{% assign pdf_url = t.pdf | prepend: '/assets/pdf/' | relative_url %}{% endif %}<a href="{{ pdf_url }}" class="btn btn-sm z-depth-0" role="button" target="_blank">PDF</a>{% if t.record %} <a href="{{ t.record }}" class="btn btn-sm z-depth-0" role="button" target="_blank">TDX</a>{% endif %}</div>
        {% endif %}
      </div>
    </div>
  </li>
{% endfor %}
</ol>
</div>