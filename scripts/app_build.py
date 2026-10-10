from dataclasses import dataclass


@dataclass(frozen=True)
class BuildVariant:
    all_sources: bool = False
    exclude_hongguo: bool = False

    def __post_init__(self):
        if self.exclude_hongguo and not self.all_sources:
            raise SystemExit('--exclude-hongguo 只能与 --all-sources 一起使用。')

    @property
    def slug(self):
        if not self.all_sources:
            return 'hongguojian'
        return 'zhenguojian-tv' if self.exclude_hongguo else 'zhenguojian'

    @property
    def arguments(self):
        return [
            *(['--all-sources'] if self.all_sources else []),
            *(['--exclude-hongguo'] if self.exclude_hongguo else []),
        ]

    @property
    def flutter_arguments(self):
        return [
            '--dart-define=ALL_SOURCES=' + str(self.all_sources).lower(),
            '--dart-define=EXCLUDE_HONGGUO=' + str(self.exclude_hongguo).lower(),
        ]

    @property
    def linker_flags(self):
        return (
            '-s -w'
            ' -X duanjuapp/native/core.buildAllSources=' + str(self.all_sources).lower()
            + ' -X duanjuapp/native/core.buildExcludeHongguo=' + str(self.exclude_hongguo).lower()
        )


def add_variant_argument(parser):
    parser.add_argument('--all-sources', action='store_true',
                        help='构建包含全部站源的真果鉴；默认构建仅红果的红果鉴')
    parser.add_argument('--exclude-hongguo', action='store_true',
                        help='在全站源基础上排除红果，构建安卓电视端真果鉴')
