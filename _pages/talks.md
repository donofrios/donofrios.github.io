---
layout: page
permalink: /talks/
title: talks
description: conference talks and seminars in reverse chronological order.
nav: true
nav_order: 3
---

<div class="publications">
<ol class="bibliography">
{% assign talks = site.data.talks | sort: "date" | reverse %}
{% for k in talks %}
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