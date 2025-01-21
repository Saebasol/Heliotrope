from typing import Optional

from sanic.blueprints import Blueprint

from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView

from heliotrope.application.sanic import HeliotropeRequest

about_endpoint = Blueprint("about", url_prefix="/about")

html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heliotrope</title>
    <script>
        let isMirroring = false;
        let mirroringProgress = {};
        let intervalId;

        async function fetchProgress() {
            const response = await fetch('/api/progress');
            mirroringProgress = await response.json();
            if (!mirroringProgress.is_mirroring_galleryinfo && !mirroringProgress.is_converting_to_info) {
                isMirroring = false;
                if (intervalId) {
                    clearInterval(intervalId);
                    intervalId = null;
                }
            } else {
                isMirroring = true;
                if (!intervalId) {
                    intervalId = setInterval(fetchProgress, 5000);
                }
            }
            updateStatus();
        }

        function updateStatus() {
            const statusElement = document.getElementById('status');
            const checkedElement = document.getElementById('checked');
            if (mirroringProgress.is_mirroring_galleryinfo) {
                statusElement.innerText = "Currently mirroring Galleryinfo...";
                checkedElement.innerText = `I am mirroring ${mirroringProgress.total} works, and ${mirroringProgress.job_completed} out of ${mirroringProgress.job_total} jobs have been completed.`;
            } else if (mirroringProgress.is_converting_to_info) {
                statusElement.innerText = "Currently converting to info...";
                checkedElement.innerText = `I am converting ${mirroringProgress.total} works, and ${mirroringProgress.job_completed} out of ${mirroringProgress.job_total} jobs have been completed.`;
            } else {
                statusElement.innerText = "Currently I'm idle";
                if (mirroringProgress.mirrored === 0) {
                    checkedElement.innerText = `I last checked on ${mirroringProgress.last_checked} and no works have been mirrored yet. were last mirrored on ${mirroringProgress.last_mirrored}.`
                    return;
                }
                checkedElement.innerText = `I last checked on ${mirroringProgress.last_checked} and ${mirroringProgress.mirrored} works were last mirrored on ${mirroringProgress.last_mirrored}.`
            }
        }

        // Initial fetch
        fetchProgress();
    </script>
</head>

<body style="text-align: center;">
    <h1>Heliotrope</h1>
    <h2 id="status"></h2>
    <h3 id="checked"></h3>
</body>

</html>
"""


class HeliotropeAboutView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest) -> Optional[HTTPResponse]:
        return HTTPResponse(html, content_type="text/html")


about_endpoint.add_route(HeliotropeAboutView.as_view(), "/")
