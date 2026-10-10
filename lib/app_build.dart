const allSourcesEnabled = bool.fromEnvironment('ALL_SOURCES');
const hongguoExcluded = bool.fromEnvironment('EXCLUDE_HONGGUO');
const appName = allSourcesEnabled ? '真果鉴' : '红果鉴';
const appSlug = !allSourcesEnabled
    ? 'hongguojian'
    : hongguoExcluded
    ? 'zhenguojian-tv'
    : 'zhenguojian';
