'use strict';

var skodenControllers = angular.module('skodenControllers', []);

skodenControllers.controller('HeaderController', ['$scope',
	function($scope) {
		$scope.respond = function() {
			var header = document.getElementById("header");
			var menu = document.getElementById("bar-top");
			var nav = document.getElementById("nav-list")
			if (header.className === "closed") {
				header.className = "opened";
				menu.className = "no-display";
				nav.style.visibility = "visible";
			} else {
				header.className = "closed";
				menu.className = "nav-bar";
				nav.style.visibility = "hidden"
			}
		}
	}
]);

skodenControllers.controller('SubheaderController', ['$scope', '$log', 'TitleService',
	function($scope, $log, TitleService) {
		$scope.$on('titleChanged', function() {
			$scope.title = TitleService.title;
		});
	}
]);

skodenControllers.controller('FeatureController', ['$scope', '$state', '$log',
	function($scope, $state, $log) {
	}
]);

skodenControllers.controller('PlayerController', ['$scope', '$log', 'SoundCloudService',
	function($scope, $log, SoundCloudService) {
	}
]);

skodenControllers.controller('SidebarController', ['$scope', '$log', 'SoundCloudService',
	function($scope, $log, SoundCloudService) {

}]);

skodenControllers.controller('ModalController', ['$scope', 
	function($scope) {

	}
]);

skodenControllers.controller('HomeController', ['$scope', '$log', 'TitleService',
	function($scope, $log, TitleService) {
		TitleService.setTitle("Season 2 of Skoden Chronicles coming November 1! #Stoodis.")
	}
]);

skodenControllers.controller('TeamController', ['$scope', '$log', 'TitleService',
	function($scope, $log, TitleService) {
		TitleService.setTitle("Our Skoden Team is expanding. Want to help out? Read on...")
	}
]);

skodenControllers.controller('ContactController', ['$scope', '$log', 'TitleService',
	function($scope, $log, TitleService) {
		TitleService.setTitle("You got something to say? #Gwanden. Speak your truth to us.")
	}
]);

skodenControllers.controller('ResourcesController', ['$scope', '$log', 'TitleService',
	function($scope, $log, TitleService) {
		TitleService.setTitle("Want to start your own podcast? We can help you get started.")
	}
]);

skodenControllers.controller('ListenController', ['$scope', '$log', 'TitleService',
	function($scope, $log, TitleService) {
		TitleService.setTitle("Listen to or download all our podcasts you could ever wish for!")
	}
]);

skodenControllers.controller('ReadController', ['$scope', '$log', 'TitleService',
	function($scope, $log, TitleService) {
		TitleService.setTitle("Stay up to date on everything Team Skoden is doing on the daily.")
	}
]);