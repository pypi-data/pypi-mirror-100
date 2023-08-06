set DOMAIN={{variables['domain']}}
set INSTALLED_APPLIS={% for app in variables['selected_apps_details'] %}{{ app.id }} {% endfor %}
