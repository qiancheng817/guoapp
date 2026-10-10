import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from app_build import BuildVariant, add_variant_argument

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--abi', action='append', choices=['arm64-v8a', 'armeabi-v7a', 'x86_64'])
parser.add_argument('--universal', action='store_true',
                    help='同时构建包含 arm64-v8a 与 armeabi-v7a 的通用 APK，电视端安装失败时优先使用')
add_variant_argument(parser)
options = parser.parse_args()
variant = BuildVariant(options.all_sources, options.exclude_hongguo)
env = os.environ.copy()
if platform.system() == 'Darwin':
    env['LANG'] = 'en_US.UTF-8'
    env['LC_ALL'] = 'en_US.UTF-8'
env.setdefault('GOPROXY', 'https://goproxy.cn,direct')
env.setdefault('GOSUMDB', 'off')
flutter = shutil.which('flutter')
if not flutter:
    raise SystemExit('请先将 Flutter SDK 的 bin 目录加入 PATH。')
abi_args = [item for abi in options.abi or [] for item in ['--abi', abi]]
subprocess.run([sys.executable, str(root / 'scripts' / 'build_native.py'), '--platform', 'android', *abi_args, *variant.arguments],
               cwd=root, env=env, check=True)
subprocess.run([flutter, 'pub', 'get'], cwd=root, env=env, check=True)
build_args = [flutter, 'build', 'apk', '--release', '--split-per-abi', '--no-pub', *variant.flutter_arguments]
if options.abi:
    targets = {'arm64-v8a': 'android-arm64', 'armeabi-v7a': 'android-arm', 'x86_64': 'android-x64'}
    build_args += ['--target-platform', ','.join(targets[abi] for abi in options.abi)]
subprocess.run(build_args, cwd=root, env=env, check=True)
subprocess.run([sys.executable, str(root / 'scripts' / 'package_release.py'), '--platform', 'android', *abi_args, *variant.arguments],
               cwd=root, env=env, check=True)
if options.universal:
    universal_args = [flutter, 'build', 'apk', '--release', '--no-pub',
                      '--target-platform', 'android-arm,android-arm64', *variant.flutter_arguments]
    subprocess.run(universal_args, cwd=root, env=env, check=True)
    subprocess.run([sys.executable, str(root / 'scripts' / 'package_release.py'), '--platform', 'android',
                    '--universal', *variant.arguments],
                   cwd=root, env=env, check=True)
