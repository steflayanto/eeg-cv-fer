'use strict';
var oldImages = [];

function init(config, storage)
{
	config.app_notifier.on('assets-updated', assetsUpdated.bind(null, config));
}

function bind(config, app, storage)
{
	app.get('/', (req, res, next) =>
	{
		try
		{ 
			res.render(`main`,
			{
					test_key: 'key'
			});
		}
		catch (e)
		{
			M.log(e);
			next(e);
		}
	});
};

function assetsUpdated(config, keys, storage, response)
{
	const dataInputRaw = JSON.parse(storage.get(`downloads/key`, 'utf8'));
	for (let oldImageName of oldImages) {
		storage.remove(`/assets/image/${oldImageName}`);
	}
}

module.exports =
{
	init,
	bind
};
