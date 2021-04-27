"use strict";

(function(){

window.M = window.M || {};

window.addEventListener('message', (e) =>
{
	if (e.source != window.parent)
	{
		console.log('ignored message from unknown window');
	}
	else if (e.data.m == 'ping')
	{
		window.parent.postMessage({ m:'pong' }, '*');
	}
	else
	{
		M.notifier.dispatchEvent(new CustomEvent(e.data.m, { detail: e.data }));
	}
});

M.notifier = document.createElement('div');		// Safari doesn't support EventTarget() constructor

M.getAppKeys = function(e)
{
	return e.detail.keys.filter(k => !k.includes('__'));
};

M.restartApp = function()
{
	window.parent.postMessage({ m:'restart' }, '*');
};

/**
 * Borrowed from YUI:  Y.Lang.sub
 *
 * Performs `{placeholder}` substitution on a string. The object passed
 * as the second parameter provides values to replace the
 * `{placeholder}`s.  `{placeholder}` token names must match property
 * names of the object. For example,
 *
 * `var greeting = A.Intl.format("Hello, {who}!", { who: "World" });`
 *
 * `{placeholder}` tokens that are undefined on the object map will be left
 * in tact (leaving unsightly `{placeholder}`'s in the output string).
 *
 * @param {string} s String to be modified.
 * @param {object} o Object containing replacement values.
 * @return {string} the substitute result.
 */
M.format = (s, o) =>
{
	/**
	 * Finds the value of `key` in given object.
	 * If the key has a 'dot' notation e.g. 'foo.bar.baz', the function will
	 * try to resolve this path if it doesn't exist as a property
	 * @example
	 *    value({ 'a.b': 1, a: { b: 2 } }, 'a.b'); // 1
	 *    value({ a: { b: 2 } }          , 'a.b'); // 2
	 * @param {Object} obj A key/value pairs object
	 * @param {String} key
	 * @return {Any}
	 */
	function value(obj, key)
	{
		let subkey;

		if (typeof obj[key] !== 'undefined')
		{
			return obj[key];
		}

		key    = key.split('.');         // given 'a.b.c'
		subkey = key.slice(1).join('.'); // 'b.c'
		key    = key[0];                 // 'a'

		// special case for null as typeof returns object and we don't want that.
		if (subkey && typeof obj[key] === 'object' && obj[key] !== null)
		{
			return value(obj[key], subkey);
		}
	}

	return s.replace ? s.replace(/\{\s*([^|}]+?)\s*(?:\|([^}]*))?\s*\}/g, (match, key) =>
	{
		var val = key.indexOf('.')>-1 ? value(o, key) : o[key];
		return typeof val === 'undefined' ? match : val;
	}) : s;
};

})();
