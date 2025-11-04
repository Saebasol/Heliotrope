from yggdrasil.infrastructure.sqlalchemy.entities.artist import ArtistSchema


def test_artist_schema_creation():
    artist = ArtistSchema(artist="test artist", url="http://example.com/artist")
    assert artist.artist == "test artist"
    assert artist.url == "http://example.com/artist"


def test_artist_schema_serialization():
    artist = ArtistSchema(artist="test artist", url="http://example.com/artist")
    serialized = artist.to_dict()

    assert "artist" in serialized
    assert "url" in serialized
    assert serialized["artist"] == "test artist"
    assert serialized["url"] == "http://example.com/artist"


def test_artist_schema_deserialization():
    data = {"artist": "test artist", "url": "http://example.com/artist"}
    artist = ArtistSchema.from_dict(data)

    assert artist.artist == "test artist"
    assert artist.url == "http://example.com/artist"


def test_artist_schema_equality():
    artist1 = ArtistSchema(artist="test artist", url="http://example.com/artist")
    artist2 = ArtistSchema(artist="test artist", url="http://example.com/artist")
    artist3 = ArtistSchema(artist="different artist", url="http://example.com/artist")

    assert artist1 == artist2
    assert artist1 != artist3
