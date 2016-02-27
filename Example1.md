# Insert 3 ad show's by admin #

## Ad Show 1 ##

```
name: 'ad 1'
group: 'first-group'
template_body: 'my ad number 1'
url_pattern: None
```

## Ad Show 2 ##

```
name: 'ad 2'
group: 'first-group'
template_body: 'my ad number 2'
url_pattern: '/test/[\w_-]+/'
```

## Ad Show 3 ##

```
name: 'ad 3'
group: 'second-group'
template_body: 'my ad number 3'
url_pattern: ''
```

# Template #

Add this code to your templates for "/" and "/test/some-slug/" url:

```
{% load ads %}

{% ad_by_group "first-group" %}
```

Add this code to your templates for other url:

```
{% load ads %}

{% ad "ad-3" %}
```

# Result #

  1. When you go to "/" url, you will see the result "my ad number 1"
  1. When you go to "/test/some-slug/" url, you will see the result "my ad number 3"
  1. When you go to another url, you will see the result "my ad number 3"