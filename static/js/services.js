'use strict';

var skodenServices = angular.module('skodenServices', []);

skodenServices.factory('TitleService', ['$rootScope', function($rootScope) {
	function TitleService() {
		var self = this;

		self.title = null;
		self.setTitle = function(str) {
			self.title = str;
			$rootScope.$broadcast('titleChanged');
		}
	}
	return new TitleService();
}]);


skodenServices.factory('SoundCloudService', ['$http', '$log', function($http, $log) {
	var about,
	    allPlaylists,
	    allTracks,
	    playerHtml,
	    currentPlaylist,
	    promise;
	
	promise = $http.get('/api/get-sc-data').then(function(response) {
		about = response.data.about;
		allPlaylists = response.data.allPlaylists;
		allTracks = response.data.allTracks;
		playerHtml = response.data.playerHtml;
		currentPlaylist = allPlaylists[0];
	});

	function getXMostTrendingFrom(x, playlist) {
		var i, trending = [];
		if (playlist) {
			playlist.sort(function(a, b){ b.playback_count - a.playback_count });
			for (i=0; i<x; i++) {
				trending.push(playlist[i]);
			}
		}
		return trending;
	}

	return {
		promise: promise,
		about: about,
		allPlaylists: allPlaylists,
		allTracks: allTracks,
		playerHtml: playerHtml,
		currentPlaylist: currentPlaylist,
		getXMostTrendingFrom: getXMostTrendingFrom,
	}
}]);