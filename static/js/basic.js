/*
 * SimpleModal Basic Modal Dialog
 * http://www.ericmmartin.com/projects/simplemodal/
 * http://code.google.com/p/simplemodal/
 *
 * Copyright (c) 2009 Eric Martin - http://ericmmartin.com
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Revision: $Id: basic.js 185 2009-02-09 21:51:12Z emartin24 $
 *
 */

$(document).ready(function () {
	$('#basicModal input.basic, #basicModal a.basic').click(function (e) {
		e.preventDefault();
		$('#basicModalContent').modal();
	});
});