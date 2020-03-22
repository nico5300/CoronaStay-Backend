
# Backend REST Api

## Register

URL: `POST /register/`

```json
{
    "username": "<username>"
}

{
    "api_key": "<api_key>"
}
```

## Create Story

URL: `POST /story/`

```json
{
    "title": "<title>",
    "start_panel": "<base64_img>",
    "api_key": "<api_key>"
}

{
    "story_id": "<story_id>"
}
```

## Get Story

URL: `GET /story/<story_id>/`

```json
{
    "api_key": "<api_key>"
}

{
    "title": "<title>",
    "panels": ["<img_url>", "...", "<img_url>"]
}
```

## Continue Story

URL: `POST /story/<story_id>/`

```json
{
    "panel": "<base64_panel>",
    "finish": "<bool>",
    "api_key": "<api_key>"
}

{
    "title": "<title>",
    "panels": ["<img_url>", "...", "<img_url>"]
}
```

## Browse Stories

URL: `GET /stories/`

```json
{
    "type": "<unfinished/finished>",
    "api_key": "<api_key>"
}

{
    "stories": [
        {
            "title": "<title>",
            "start_panel": "<img_url>"
        },
        {},
        {
            "title": "<title>",
            "start_panel": "<img_url>"
        }
    ]
}
```
