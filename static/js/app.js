'use strict';

var skodenApp = angular.module('skodenApp', [
	'ui.router',
	'skodenControllers',
	'skodenDirectives',
	'skodenServices',
	'skodenFilters',
])
.run(function($rootScope, $state) {
	$rootScope.$state = $state;
});

skodenApp.config(['$stateProvider', '$urlRouterProvider',
	function($stateProvider, $urlRouterProvider) {
		$urlRouterProvider.otherwise('/');
		$stateProvider
			.state('root', {
				url: '',
				template: "<ui-view />",
				abstract:true,
				views: {
					'header': {
						templateUrl:'../static/partials/header.html',
						controller: 'HeaderController',
					},
					'sub-header': {
						templateUrl: '../static/partials/subheader.html',
						controller: 'SubheaderController',
					},
					'featured-episode': {
						templateUrl: '../static/partials/featured-article.html',
						controller: 'FeatureController',
					},
					'player': {
						templateUrl: '../static/partials/player.html',
						controller: 'PlayerController',
					},
					'sidebar': {
						templateUrl: '../static/partials/sidebar.html',
						controller: 'SidebarController'
					},
					'footer': {
						templateUrl: '../static/partials/footer.html'
					},
					'modal': {
						templateUrl: '../static/partials/modal.html',
						controller: 'ModalController'
					},
				},
			})
			.state('root.home', {
				url: '/',
				views: {
					'main@': {
						templateUrl:'../static/partials/home.html',
						controller: 'HomeController',
					},
				},
			})
			.state('root.team', {
				url: '/team',
				views: {
					'main@': {
						templateUrl: '../static/partials/team.html',
						controller: 'TeamController',
					},
				},
			})
			.state('root.contact', {
				url: '/contact',
				views: {
					'main@': {
						templateUrl: '../static/partials/contact.html',
						controller: 'ContactController',
					},
				},
			})
			.state('root.resources', {
				url: '/resources',
				views: {
					'main@': {
						templateUrl: '../static/partials/resources.html',
						controller: 'ResourcesController',
					},
				},
			})
			.state('root.listen-to', {
				url: '/listen-to',
				views: {
					'main@': {
						templateUrl: '../static/partials/listen-to.html',
						controller: 'ListenController',
					},
				},
			})
			.state('root.listen-to.season', {
				url: '/listen-to/:season',
				views: {
					'main@': {
						templateUrl: '../static/partials/listen-to.season.html',
					},
				},
			})
			.state('root.listen-to.season.episode', {
				url: '/listen-to/:season/:episode',
				views: {
					'main@': {
						templateUrl: '../static/partials/listen-to.season.episode.html',
					},
				},
			})
			.state('root.read', {
				url: '/read',
				views: {
					'main@': {
						templateUrl: '../static/partials/read.html',
						controller: 'ReadController',
					},
				},
			})
			.state('root.read.post', {
				url: '/read/:post',
				views: {
					'main@': {
						templateUrl: '../static/partials/read.post.html',
					},
				},
			})
		}
]);