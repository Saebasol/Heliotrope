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
from heliotrope.database.orm.table.artist import artist_table
from heliotrope.database.orm.table.character import character_table
from heliotrope.database.orm.table.file import file_table
from heliotrope.database.orm.table.gallleryinfo import galleryinfo_table
from heliotrope.database.orm.table.group import group_table
from heliotrope.database.orm.table.language import language_table
from heliotrope.database.orm.table.parody import parody_table
from heliotrope.database.orm.table.related import related_table
from heliotrope.database.orm.table.scene_index import scene_index_table
from heliotrope.database.orm.table.tag import tag_table

__all__ = [
    "artist_table",
    "character_table",
    "file_table",
    "galleryinfo_table",
    "group_table",
    "language_table",
    "parody_table",
    "related_table",
    "scene_index_table",
    "tag_table",
]
