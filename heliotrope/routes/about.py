from sanic import Blueprint
from sanic.response import html, json
from sanic.views import HTTPMethodView

from heliotrope.utils.typed import HeliotropeRequest

heliotrope_about = Blueprint("heliotrope_about", url_prefix="/about")


class HeliotropeAboutView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest):
        manager = request.app.ctx.mirroring_manager
        if (is_json := request.args.get("json")) and (is_json.lower() == "true"):
            return json(
                {
                    "last_checked_time": manager.last_checked_time,
                    "last_mirrored_time": manager.mirroring_time,
                    "new_item": manager.new_item,
                    "server_status": manager.status,
                }
            )

        return html(
            f"""
<!DOCTYPE html>
<html>

<head>
    <title>Heliotrope About</title>
    <meta charset="utf-8" />
</head>

<body style="text-align:center;">
    <h1>About Heliotrope</h1>
    <div>
        <p>Last checked time: {manager.last_checked_time}</p>
        <p>Last mirrored time: {manager.mirroring_time}</p>
        <p>New item: {manager.new_item} item was added</p>
        <p>Server status: {manager.status}</p>
    </div>
    <footer>
        <i><a href="https://github.com/Saebasol/Heliotrope">Saebasol Heliotrope</i>
    </footer>
</body>

</html>
"""
        )


heliotrope_about.add_route(HeliotropeAboutView.as_view(), "")
