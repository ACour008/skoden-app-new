var loc = 'http://localhost:5000/static/ckeditor/plugins/';

CKEDITOR.plugins.addExternal('button', loc+'/button/', 'plugin.js');
CKEDITOR.plugins.addExternal('clipboard', loc+'/clipboard/', 'plugin.js');
CKEDITOR.plugins.addExternal('dialog', loc+'dialog/', 'plugin.js');
CKEDITOR.plugins.addExternal('dialogui', loc+'/dialogui/', 'plugin.js');
CKEDITOR.plugins.addExternal('embed', loc+'/embed/', 'plugin.js');
CKEDITOR.plugins.addExternal('embedbase', loc+'/embedbase/', 'plugin.js');
CKEDITOR.plugins.addExternal('lineutils', loc+'/lineutils/', 'plugin.js');
CKEDITOR.plugins.addExternal('notification', loc+'/notification/', 'plugin.js');
CKEDITOR.plugins.addExternal('notificationaggregator', loc+'/notificationaggregator/', 'plugin.js');
CKEDITOR.plugins.addExternal('toolbar', loc+'/toolbar/', 'plugin.js');
CKEDITOR.plugins.addExternal('widget', loc+'/widget/', 'plugin.js');
CKEDITOR.plugins.addExternal('widgetselection', loc+'/widgetselection/', 'plugin.js');

CKEDITOR.replace('body', {
    embed_provider: '//ckeditor.iframe.ly/api/oembed?url={url}&callback={callback}',
    extraPlugins: 'button,clipboard,dialog,dialogui,embed,embedbase,lineutils,notification,notificationaggregator,toolbar,widget,widgetselection'
});