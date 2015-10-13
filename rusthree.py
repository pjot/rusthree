import webapp2
import json
import logging
from google.appengine.ext import ndb

class Song(ndb.Model):
    name = ndb.StringProperty()
    chords = ndb.TextProperty()
    albums = ndb.KeyProperty(kind='Album', repeated=True)

    def get_albums(self):
        for key in self.albums:
            yield key.get()

    def as_dict(self):
        song = {
            'id': self.key.urlsafe(),
            'name': self.name,
            'albums': [],
        }

        for album in self.get_albums():
            song['albums'].append({
                'id': album.key.urlsafe(),
                'name': album.name,
                'year': album.year,
            })

        return song


class Album(ndb.Model):
    name = ndb.StringProperty()
    year = ndb.IntegerProperty()

    def get_songs(self):
        return self.songs

    @property
    def songs(self):
        return Song.query().filter(Song.albums == self.key)

    def add_song(self, song):
        song.albums.append(self.key)
        song.put()

    def as_dict(self):
        album = {
            'id': self.key.urlsafe(),
            'name': self.name,
            'year': self.year,
            'songs': [],
        }

        for song in self.get_songs():
            album['songs'].append({
                'id': song.key.urlsafe(),
                'name': song.name,
            })

        return album

class AddSong(webapp2.RequestHandler):
    def get(self):
        a = Album()
        a.name = 'Rust Never Sleeps'
        a.year = 1975
        a.put()

        s = Song()
        s.name = 'Thrasher'
        a.add_song(s)
        s2 = Song()
        s2.name = 'Hey Hey My My'
        a.add_song(s2)

        a2 = Album()
        a2.name = 'Harvest'
        a2.year = 1972
        a2.put()

        s3 = Song()
        s3.name = 'Harvest'
        a2.add_song(s3)

        s4 = Song()
        s4.name = 'Alabama'
        a2.add_song(s4)
        self.response.write('done!')

class SongsPage(webapp2.RequestHandler):
    def get(self):
        songs = Song.query().order(Song.name).fetch()
        final = []
        for song in songs:
            final.append(song.as_dict())
        self.response.write(json.dumps(final))

class SongPage(webapp2.RequestHandler):
    def get(self, song_id):
        key = ndb.Key(urlsafe=song_id)
        song = key.get()
        self.response.write(json.dumps(song.as_dict()))

class AlbumsPage(webapp2.RequestHandler):
    def get(self):
        albums = Album.query().order(Album.name).fetch()
        final = []
        for album in albums:
            final.append(album.as_dict())
        self.response.write(json.dumps(final))

class AlbumPage(webapp2.RequestHandler):
    def get(self, album_id):
        key = ndb.Key(urlsafe=album_id)
        album = key.get()
        self.response.write(json.dumps(album.as_dict()))

def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

app = webapp2.WSGIApplication([
    ('/api/songs', SongsPage),
    ('/api/song/(.*)', SongPage),
    ('/api/albums', AlbumsPage),
    ('/api/album/(.*)', AlbumPage),
    ('/api/populate', AddSong),

], debug=True)

app.error_handlers[404] = handle_404


