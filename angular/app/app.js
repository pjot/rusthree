'use strict';

// Declare app level module which depends on views, and components
angular.module('rusthree', ['ngRoute', 'rusthree.controllers']).

config(function($routeProvider) {
    $routeProvider
        .when('/song/:id', {
            templateUrl: 'templates/song.html',
            controller: 'SongCtrl',
        })
        .when('/album/:id', {
            templateUrl: 'templates/album.html',
            controller: 'AlbumCtrl',
        })
        .when('/songs', {
            templateUrl: 'templates/songs.html',
            controller: 'SongsCtrl',
        })
        .when('/albums', {
            templateUrl: 'templates/albums.html',
            controller: 'AlbumsCtrl',
        });
});
