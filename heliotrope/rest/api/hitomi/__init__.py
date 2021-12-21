"""
MIT License

Copyright (c) 2021 SaidBySolo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from sanic.blueprints import Blueprint

from heliotrope.rest.api.hitomi.galleryinfo import hitomi_galleryinfo
from heliotrope.rest.api.hitomi.info import hitomi_info
from heliotrope.rest.api.hitomi.list import hitomi_list
from heliotrope.rest.api.hitomi.random import hitomi_random
from heliotrope.rest.api.hitomi.search import hitomi_search
from heliotrope.rest.api.hitomi.image import hitomi_image

hitomi_endpoint = Blueprint.group(
    hitomi_search,
    hitomi_galleryinfo,
    hitomi_info,
    hitomi_list,
    hitomi_random,
    hitomi_image,
    url_prefix="/hitomi",
)
