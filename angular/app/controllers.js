angular.module('rusthree.controllers', [])

.controller('SongCtrl', function ($scope, $http, $routeParams) {
    $http.get('api/song/' + $routeParams.id).success(function (data) {
        $scope.song = data;
    });
})

.controller('AlbumCtrl', function ($scope, $http, $routeParams) {
    $http.get('api/album/' + $routeParams.id).success(function (data) {
        $scope.album = data;
    });
})

.controller('SongsCtrl', function ($scope, $http) {
    $http.get('api/songs').success(function (data) {
        $scope.songs = data;
    });
})

.controller('AlbumsCtrl', function ($scope, $http) {
    $http.get('api/albums').success(function (data) {
        $scope.albums = data;
    });
})

.controller('NavbarCtrl', function ($scope, $location) {
    $scope.isActive = function (route) {
        return route == $location.path();
    };
});
;
